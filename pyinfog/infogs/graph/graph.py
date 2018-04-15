# -*- coding: utf-8 -*-
# Copyright 2017-2018 Niall McCarroll
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


from pyinfog.common.diagram_element import DiagramElement

import random
from math import radians,sin,cos,pi,sqrt,log

from pyinfog.svg.pysvg import circle, line, text

class Graph(DiagramElement):

    """
    Force directed layout based vaguely on http://cs.brown.edu/~rt/gdhandbook/chapters/force-directed.pdf
    """

    def __init__(self, data, width, height, palette, labels, text_attributes={}):
        """
        Create a Graph

        :param data: data describing a tree in the form of a tuple (nodes,links), where nodes is a list of (node-id,category,value) tuples and links is a list of (node-id1,node-id2,weight) tuples
        :param width: the width of the plot in pixels
        :param height: the height of the plot in pixels
        :param palette: a list of (category, colour) pairs
        :param labels: dict associating each category with a longer string label
        :param text_attributes: dict containing attributes to a apply to SVG text elements
        """

        self.data = data
        self.width = width
        self.height = height
        self.labels = labels
        self.palette_lookup = { cat:col for (cat,col) in palette }
        (self.sumtotal,self.weightmax) = self.total()
        self.text_attributes = text_attributes

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def draw(self,diagram,ox,oy):
        xc = ox - self.width/2
        yc = oy

        coords = {}

        nodes = self.data[0]
        links = self.data[1]

        node_links = {}

        distance = lambda x1,y1,x2,y2: sqrt((x1-x2)**2+(y1-y2)**2)

        def clip(coords):
            (x,y,r) = coords
            if x<xc+r:
                x = xc+r
            if y<yc+r:
                y = yc+r
            if x >xc+self.width-r:
                x = xc+self.width-r
            if y >yc+self.height-r:
                y = yc+self.height-r
            return (x,y,r)

        for (nodeid0,nodeid1,weight) in links:
            if nodeid0 not in node_links:
                node_links[nodeid0] = []
            if nodeid1 not in node_links:
                node_links[nodeid1] = []
            node_links[nodeid0].append(nodeid1)
            node_links[nodeid1].append(nodeid0)

        for (nodeid,cat,value) in nodes:
            frac = value/self.sumtotal
            area = self.width*self.height*0.25*frac
            r = sqrt(area/pi)
            cx = xc + r + (self.width-2*r)*random.random()
            cy = yc + r + (self.height-2*r)*random.random()
            coords[nodeid] = (cx,cy,r)



        c1 = 2
        c3 = 1
        c4 = 0.1
        c5 = 100
        iters = 50000


        for iter in range(iters):
            forces = {}
            for (nodeid,cat,value) in nodes:
                forces[nodeid] = (0,0)
                (nx,ny,nr) = coords[nodeid]
                if nodeid in node_links:
                    for adjid in node_links[nodeid]:
                        (ax,ay,adjr) = coords[adjid]
                        c2 = (nr+adjr) * 2
                        d = distance(nx,ny,ax,ay)
                        f = c1*log(d/c2)
                        fx = ((ax-nx)/d)*f*c4
                        fy = ((ay-ny)/d)*f*c4
                        forces[nodeid] = (forces[nodeid][0]+fx,forces[nodeid][1]+fy)
                for otherid in coords:
                    if otherid != nodeid:
                        (ox,oy,otherr) = coords[otherid]
                        d =  distance(nx,ny,ox,oy)
                        f = c3/(d**2)
                        fx = ((nx-ox)/d)*f*c5
                        fy = ((ny-oy)/d)*f*c5
                        forces[nodeid] = (forces[nodeid][0]+fx,forces[nodeid][1]+fy)

            for nodeid in coords:
                coords[nodeid] = (coords[nodeid][0]+forces[nodeid][0],coords[nodeid][1]+forces[nodeid][1],coords[nodeid][2])
                coords[nodeid] = clip(coords[nodeid])

        for (nodeid0,nodeid1,weight) in links:
            (x1,y1,r1) = coords[nodeid0]
            (x2,y2,r2) = coords[nodeid1]
            l = line(x1,y1,x2,y2,self.getLinkColour(weight),3)
            diagram.add(l)

        for (nodeid,cat,value) in nodes:
            (cx,cy,r) = coords[nodeid]
            col = self.palette_lookup[cat]
            circ = circle(cx,cy,r,col)
            circ.addAttr("stroke","#EEE")
            circ.addAttr("stroke-width",4)

            diagram.add(circ)
            if nodeid in self.labels:
                label = self.labels[nodeid]
                length = len(label)
                t = text(cx,cy,label)
                font_height = 2*r*0.8/length
                text_length = font_height*length
                t.addAttr("textLength",text_length)
                t.addAttr("font-size",font_height)
                t.addAttrs(self.text_attributes)
                diagram.add(t)

    def getLinkColour(self,weight):
        shade = int(255-255*(weight/self.weightmax))
        return "#%02X%02X%02X"%(shade,shade,shade)

    def total(self):
        nodes = self.data[0]
        sumtotal = sum([value for (nodeid,cat,value) in nodes])
        links = self.data[1]
        weightmax = max([weight for (_,_,weight) in links])
        return (sumtotal,weightmax)
