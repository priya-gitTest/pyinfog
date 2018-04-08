# Copyright 2017 Niall McCarroll
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from xml.dom.minidom import *
from math import cos,sin,pi

# base class for SVG objects, holding style information and handing rendering
class svgstyled(object):

    def __init__(self,tag,tooltip=""):
        self.tag = tag
        self.style = {}
        self.attrs = {}
        self.tooltip = tooltip
        self.content = ''
        self.handlers = {}

    # add a style
    def addStyle(self,name,value):
        self.style[name] = value
        return self

    # add a style
    def addStyles(self, styles):
        if styles:
            for k in styles:
                self.addStyle(k,styles[k])
        return self

    # add an SVG attribute
    def addAttr(self,name,value):
        self.attrs[name] = value
        return self

    # add a handler
    def addHandler(self,evt,fname):
        self.handlers[evt] = fname

    # set the XML content of the element
    def setContent(self,content):
        self.content = content
        return self

    # construct the style attribute
    def getStyleAttr(self):
        keys = self.style.keys()
        s = ''
        if len(keys):
            for k in keys:
                s += k + ":" + str(self.style[k])+";"
        return s

    def render(self,svgdoc,parent):
        doc = svgdoc.doc
        if self.tooltip:
            g = doc.createElement("g")
            title = doc.createElement("title")
            title.appendChild(doc.createTextNode(self.tooltip))
            g.appendChild(title)
            parent.appendChild(g)
            parent = g

        e = doc.createElement(self.tag)
        for name in self.attrs:
            e.setAttribute(name,str(self.attrs[name]))

        for evt in self.handlers:
            fname = self.handlers[evt]
            e.setAttribute("on"+evt,fname+"(evt);")

        style = self.getStyleAttr()
        if style:
            e.setAttribute("style",style)

        parent.appendChild(e)

        if self.content != '':
            e.appendChild(doc.createTextNode(self.content))

        return e


class group(svgstyled):

    def __init__(self):
        self.children = []

    def add(self,child):
        self.children.append(child)

    def render(self,svgdoc,parent):
        g = svgdoc.doc.createElement("g")
        for t in self.children:
            t.render(svgdoc,g)
        parent.appendChild(g)
        return g

# represent a section of text as an SVG object
class text(svgstyled):

    def __init__(self,x,y,txt,tooltip=""):
        svgstyled.__init__(self,"text",tooltip)
        self.x = x
        self.y = y
        self.addAttr("x",x).addAttr("y",y).setContent(txt)
        self.url = ""
        self.addStyle("text-anchor", "middle")
        self.rotation = None

    def setUrl(self,url):
        self.url = url
        self.addStyle("text-decoration","underline")
        self.addStyle("stroke", "blue")

    def setRotation(self,radians):
        self.rotation = 360*radians/(2*pi)
        self.addAttr("transform","rotate(%f,%f,%f)"%(self.rotation,self.x,self.y))

    def render(self,svgdoc,parent):
        if not self.url:
            return super(text, self).render(svgdoc, parent)

        doc = svgdoc.doc
        p = doc.createElement("a")
        parent.appendChild(p)
        p.setAttribute("href",self.url)
        p.setAttribute("target","_new")
        t = super(text, self).render(svgdoc, p)
        return p

# represent a circle as an SVG object
class circle(svgstyled):

    def __init__(self,x,y,r,col,tooltip=""):
        svgstyled.__init__(self,'circle',tooltip)
        self.addAttr("cx",x).addAttr("cy",y).addAttr("r",r).addAttr("fill",col)

class sector(svgstyled):

    def __init__(self,ox,oy,r1,r2,theta1,theta2,tooltip=""):
        svgstyled.__init__(self,"path",tooltip)
        s = "M"+str(ox+-r2*cos(theta1))+","+str(oy+r2*-sin(theta1))+" "
        x = 0
        if (theta2-theta1) > pi:
            x = 1
        s += "A"+str(r2)+","+str(r2)+","+"0,"+str(x)+",1,"+str(ox+-r2*cos(theta2))+","+str(oy+-r2*sin(theta2))+" "
        s += "L"+str(ox+-r1*cos(theta2))+","+str(oy+-r1*sin(theta2))+" "
        if r1:
            s += "A"+str(r1)+","+str(r1)+","+"0,0,0,"+str(ox+-r1*cos(theta1))+","+str(oy+-r1*sin(theta1))+" "
        s += "z"
        self.addAttr("d",s)

class curvedtext(svgstyled):

    counter = 0

    def __init__(self, ox, oy, r, text, tooltip=""):
        self.id = "ct"+str(curvedtext.counter)
        curvedtext.counter += 1
        svgstyled.__init__(self, "text", tooltip)
        theta1 = 0
        theta2 = pi
        self.path = "M" + str(ox + -r * cos(theta1)) + "," + str(oy + r * -sin(theta1)) + " "
        self.path += "A" + str(r) + "," + str(r) + "," + "0,0,1," + str(ox + -r * cos(theta2)) + "," + str(
            oy + -r * sin(theta2)) + " "
        self.text = text
        self.addStyle("alignment-baseline","baseline")
        self.addStyle("text-anchor","middle")

    def render(self,svgdoc,parent):
        t = super(curvedtext,self).render(svgdoc,parent)
        doc = svgdoc.doc
        p = doc.createElement("path")
        p.setAttribute("id",self.id)
        p.setAttribute("d",self.path)
        svgdoc.defs.appendChild(p)
        tp = doc.createElement("textPath")
        tp.setAttribute("xlink:href","#"+self.id)
        tp.setAttribute("startOffset","50%")
        t.appendChild(tp)
        tp.appendChild(doc.createTextNode(self.text))
        return tp

# represent a polygon as an SVG object
class polygon(svgstyled):

    def __init__(self,points,fill,stroke,stroke_width,tooltip=""):
        svgstyled.__init__(self,"path",tooltip)
        s = 'M'
        sep = ''
        for p in points:
            if len(p) == 1:
                s += " "+p[0]
                continue
            (x,y) = p
            s += sep
            sep = ' '
            s += str(x)+" "+str(y)
        s += 'Z'
        self.addAttr("d",s).addAttr("fill",fill)
        if stroke and stroke_width:
            self.addAttr("stroke-width",stroke_width).addAttr("stroke",stroke)


class svgdefinition(object):

    def __init__(self,id):
        self.id = id

    def getId(self):
        return self.id

# represent embedded javascript

class javascript_snippet(svgdefinition):

    counter = 0

    def __init__(self,code):
        svgdefinition.__init__(self,"script_"+str(javascript_snippet.counter))
        self.code = code

    def getCode(self):
        return self.code

    def render(self,svgdoc):
        doc = svgdoc.doc
        s = doc.createElement("script")
        s.setAttribute("id", self.getId())
        s.setAttribute("type","text/ecmascript")
        tn = doc.createTextNode(self.code)
        s.appendChild(tn)
        svgdoc.root.appendChild(s)
        return s


class linear_gradient(svgdefinition):

    counter = 0

    def __init__(self, startCol, stopCol):
        svgdefinition.__init__(self,"lg_"+str(linear_gradient.counter))
        linear_gradient.counter += 1
        self.startCol = startCol
        self.stopCol = stopCol

    def render(self,svgdoc):
        doc = svgdoc.doc
        lg = doc.createElement("linearGradient")
        lg.setAttribute("id",self.getId())
        stop0 = doc.createElement("stop")
        stop0.setAttribute("offset","0%")
        stop0.setAttribute("stop-color",self.startCol)
        stop100 = doc.createElement("stop")
        stop100.setAttribute("offset", "100%")
        stop100.setAttribute("stop-color", self.stopCol)
        lg.appendChild(stop0)
        lg.appendChild(stop100)
        svgdoc.defs.appendChild(lg)
        return lg

class svgdoc(object):

    # construct a document with a given width and height
    def __init__(self,width,height):
        self.definitions = []
        self.objects = []
        self.width = width
        self.height = height

    # add an object to the document (obj inherits from svgstyled)
    def add(self,obj):
        if isinstance(obj,svgdefinition):
            self.definitions.append(obj)
        else:
            self.objects.append(obj)
        return self

    # render the document as SVG and return as string
    def render(self):

        self.doc = Document()

        self.root = self.doc.createElement("svg")
        self.root.setAttribute("xmlns","http://www.w3.org/2000/svg")
        self.root.setAttribute("xmlns:xlink","http://www.w3.org/1999/xlink")
        self.doc.appendChild(self.root)
        self.defs = self.doc.createElement("defs")
        self.root.appendChild(self.defs)
        self.root.setAttribute("xmlns:svg","http://www.w3.org/2000/svg")
        self.root.setAttribute("xmlns","http://www.w3.org/2000/svg")
        self.root.setAttribute("width","%d"%(self.width))
        self.root.setAttribute("height", "%d" % (self.height))
        self.root.setAttribute("version", "1.1")

        # add the definitions
        for o in self.definitions:
            o.render(self)

        # add the objects
        for o in self.objects:
            o.render(self,self.root)

        return self.doc.toprettyxml(encoding="utf-8")


