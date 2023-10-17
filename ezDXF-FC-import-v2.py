# some code from https://forum.freecad.org/viewtopic.php?p=276092#p276092
import os
import ezdxf
import Draft
from FreeCAD import Vector
import Part
import PySide
from PySide import QtGui, QtCore

show=True
make_compound=True


### 
def open_dxf(filename,show=None,make_compound=None):
    FreeCAD.newDocument()
    doc=FreeCAD.ActiveDocument
    filePath, fileName = os.path.split(__file__)
    if 0: 
        drawing = ezdxf.readfile(filePath+os.sep+"ezdxf_spline.dxf")
    drawing = ezdxf.readfile(filename)
    
    modelspace = drawing.modelspace()
    
    lines = modelspace.query('LINE')
    Msg('l=%d\n'% len(lines))
    lns =[]
    i=0
    if len(lines)>0:
        for line in lines:    
            s = Vector(line.dxf.start)
            e = Vector(line.dxf.end)
            # ln = Draft.makeWire([s,e],closed=False,face=False,support=None)
            try: #(e - s).Length > 0.000001: # e != s:
                ln = Part.makeLine(s,e)
                lns.append(ln)
            except:
                print('error',i, str(s),str(e))
            i+=1            
                # if i<500:            
                #     Part.show(ln)
                #     i=i+1
    
        print("i=",i)
        print("len(lns)",len(lns))
        if len(lns)>0:
            if make_compound:
                cmp=Part.makeCompound(lns)
                if show:
                    Part.show(cmp)
            elif show:
                for l in lns:
                    Part.show(l)
    # circ =Part.makeCircle(140, App.Vector(0,60,0),App.Vector(0,0,1), -90, 90)
    
    circles = modelspace.query('CIRCLE')
    Msg('c=%d\n'% len(circles))
    crcls = []
    for c in circles:
        cntr = c.dxf.center
        rad = c.dxf.radius
        crcl = Part.makeCircle (rad, Vector(cntr), Vector(0,0,1),)
        crcls.append(crcl)    
        #crcl = Draft.make_circle(rad, face=False, support=None)
        #crcl.Placement = FreeCAD.Placement(FreeCAD.Vector(cntr), FreeCAD.Rotation(0, 0, 0), FreeCAD.Vector(0, 0, 1),)
        ##crl = Draft.make_circle(radius=rad, placement=pl, face=False, support=None)
    if len(crcls)>0:
        if make_compound:
            cmpc=Part.makeCompound(crcls)
            if show:
                Part.show(cmpc)
        elif show:
            for c in crcls:
                Part.show(c)
            
    arcs = modelspace.query('ARC')
    Msg('a=%d\n'% len(arcs))
    arcs_ = []
    for a in arcs:
        cntr = a.dxf.center
        rad = a.dxf.radius
        arc = Part.makeCircle (rad, Vector(cntr), Vector(0,0,1),a.dxf.start_angle, a.dxf.end_angle)
        arcs_.append(arc)    
    if len(arcs_)>0:
        if make_compound:
            cmpa=Part.makeCompound(arcs_)
            if show:
                Part.show(cmpa)
        elif show:
            for a in arcs_:
                Part.show(a)

    plines = modelspace.query('LWPOLYLINE')
    Msg('pl=%d\n'% len(plines))
    pls = []
    for flag_ref in plines:
        for entity in flag_ref.virtual_entities():
            if entity.dxftype() == 'LINE':
                # print( str(entity.dxf.start)+ "\n")
                # print( str(entity.dxf.end)+ "\n")
                s = Vector(entity.dxf.start)
                e = Vector(entity.dxf.end)
                # ln = Draft.makeWire([s,e],closed=False,face=False,support=None)
                if e != s:
                    ln = Part.makeLine(s,e)
                    pls.append(ln)
    if len(pls)>0:
        if make_compound:
            cmppl=Part.makeCompound(pls)
            if show:
                Part.show(cmppl)
        elif show:
            for pl in pls:
                Part.show(pl)

    splines = modelspace.query('SPLINE')
    Msg('n=%d\n'% len(splines))
    if len(splines)>0:
        try:
            print("get_fit_points is deprecated, we need a method to use control_points()") 
            points=splines[0].fit_points # get_fit_points deprecated, we need a method to use control_points() 
            points2 = []
            for i in points:
                points2.append(Vector(i))
            spline = Draft.makeBSpline(points2,closed=False,face=False,support=None)
            # bez = Draft.makeBezCurve(points2,closed=False,support=None)
        except:
            print("error in spline drawing")

    
    Msg('Done!\n\n')
    FreeCAD.ActiveDocument.recompute()
    FreeCADGui.SendMsgToActiveView("ViewFit")
    FreeCADGui.activeDocument().activeView().viewTop()
# end open_dxf

test=False
Filter=""
if test:
    fname="D:/Temp/ezdxf_spline.dxf"
else:
    fname, Filter = PySide.QtGui.QFileDialog.getOpenFileName(None, "Open File...","*.dxf")

path, name = os.path.split(fname)
filename=os.path.splitext(name)[0]
if len(fname) > 0:
    open_dxf(fname,show,make_compound)