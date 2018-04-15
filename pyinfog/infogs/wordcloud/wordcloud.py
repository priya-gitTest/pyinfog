# -*- coding: utf-8 -*-
# Copyright 2017-2018 Niall McCarroll
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless require)d by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import random
from math import radians,sin,cos,pi,sqrt

# import numpy

from pyinfog.svg.pysvg import text, rectangle

class WordCloud(object):

    def __init__(self, data, width, height, palette, labels, text_attributes={}):
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
        self.data = data
        self.width = width
        self.height = height
        self.labels = labels
        self.palette_lookup = { cat:col for (cat,col) in palette }
        self.total = sum([v for (word,cat,v) in data])
        self.plots = []
        self.text_attributes = text_attributes

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def draw(self,diagram,ox,oy):
        xc = ox - self.width/2
        yc = oy
        for (word,cat,v) in sorted(self.data,key=lambda x:x[2],reverse=True):
            frac = v/self.total
            a = self.width * self.height * frac * 0.5
            l = len(word)
            h = sqrt(a/l)
            w = h*l
            pos = 0
            sa = random.random()*pi
            sx = xc+self.width/2 # +sin(sa)*self.width/8
            sy = yc+self.height/2 # +cos(sa)*self.height/8

            flip = False # random.random()>0.9

            if flip:
                oldw = w
                w = h
                h = oldw

            while True:
                pos += 1
                coords = self.spiral(pos,sx,sy)
                if not coords:
                    break
                (x,y) = coords

                x = x-w/2
                y = y-h/2
                if not self.intersects(x,y,w,h):
                    self.plotWord(diagram,word,w,h,self.getColour(cat),x,y,flip)
                    break

    def getColour(self,cat):
        if cat in self.palette_lookup:
            return self.palette_lookup[cat]
        else:
            return random.choice([col for col in self.palette_lookup.values()])

    def plotWord(self,diagram,word,w,h,col,x,y,flip):
        self.plots.append((x,y,w,h))
        r = rectangle(x,y,w,h,fill="#FFF")
        diagram.add(r)
        fs = h*0.8
        tl = w*0.8
        if flip:
            fs = w*0.8
            tl = h*0.8
        t = text(x+w*0.1,y+h*0.1,word)
        t.addStyle("text-anchor","start")
        t.addAttr("dominant-baseline","hanging")
        t.addAttr("font-size",fs)
        t.addAttr("textLength",tl)
        t.addAttr("fill",col)
        t.addAttrs(self.text_attributes)
        if flip:
            t.addAttr("writing-mode","tb")
        diagram.add(t)

    def spiral(self,pos,cx,cy):
        angle = (pos/100)*pi
        r = pos/50
        if r > self.width/2 or r >self.height/2:
            return None
        return (cx+r*sin(angle),cy+r*cos(angle))

    def intersects(self,x1,y1,w1,h1):
        for area in self.plots:
            (x2,y2,w2,h2) = area
            if not (x1 > x2+w2 or x1+w1 < x2 or y1 > y2+h2 or y1+h1 < y2):
                return True
        return False

