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
from math import radians,sin,cos

from pyinfog.svg.pysvg import text, rectangle

class TreeMap(DiagramElement):

    def __init__(self, data, width, height, palette, labels, text_attributes={}):
        """
        Create a TreeMap

        :param data: data describing a tree in the form of a list of items, where each item may be a list (denoting a subtree) or a (category,value) pair denoting a leaf node
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
        self.sumtotal = self.total(self.data)
        self.text_attributes = text_attributes

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def draw(self,diagram,ox,oy):
        xc = ox - self.width/2
        yc = oy
        self.draw_subtree(diagram,self.data,xc,yc,self.width,self.height)

    def total(self,data):
        """
        Add a WordCloud to the section

        :param data: data describing a tree in the form of a list of items, where each item is a tuple (word,category,value)
        :param width: the width of the plot in pixels
        :param height: the height of the plot in pixels
        :param palette: a list of (category, colour) pairs
        :param labels: dict associating each category with a longer string label
        :param text_attributes: dict containing attributes to a apply to SVG text elements

        :return: a WordCloud object
        """
        if isinstance(data,tuple):
            return data[1]
        else:
            return sum(map(lambda d:self.total(d),data))

    def draw_subtree(self,diagram,data,xc,yc,w,h):
        if isinstance(data,tuple):
            r = rectangle(xc,yc,w,h,fill=self.palette_lookup[data[0]],tooltip=self.labels[data[0]])
            diagram.add(r)
            fraction = data[1]/self.sumtotal
            t = text(xc+w*0.02,yc+h*0.02,"%.2f"%(100*fraction)+"%")
            t.addStyle("text-anchor","start")
            t.addAttr("dominant-baseline","hanging")
            t.addAttrs(self.text_attributes)
            diagram.add(t)
        else:
            totals = []
            for d in data:
                totals.append(self.total(d))
            sumtotal=sum(totals)
            if w < h:
                # divide vertically
                y = yc
                for idx in range(len(data)):
                    sh = h*(totals[idx]/sumtotal)
                    self.draw_subtree(diagram,data[idx],xc,y,w,sh)
                    y += sh
            else:
                x = xc
                for idx in range(len(data)):
                    sw = h*(totals[idx]/sumtotal)
                    self.draw_subtree(diagram,data[idx],x,yc,sw,h)
                    x += sw
            r = rectangle(xc,yc,w,h,stroke="black",stroke_width=4)
            diagram.add(r)
