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

from pyinfog.svg.pysvg import text,polygon,linear_gradient,group

class DiscretePlot:

    def __init__(self, width, height, data, labels, axis_labels=[], axis_label_height=16):
        self.width = width
        self.height = height
        self.palette = None
        self.data = data
        self.labels = labels
        self.axis_labels = axis_labels
        self.axis_label_height = axis_label_height
        self.category_counts = []
        self.categories = set()
        self.gradients = {}
        for key in self.data:
            cats = self.data[key]
            for i in range(0,len(cats)):
                while i >= len(self.category_counts):
                    self.category_counts.append({})
                cat = cats[i]
                self.categories.add(cat)
                if cat not in self.category_counts[i]:
                    self.category_counts[i][cat] = 0
                self.category_counts[i][cat] += 1

        self.keys = sorted([key for key in self.data])
        self.axis_pair_count = len(self.category_counts)-1

        # work out the global order of categories based on the last axis, put the most frequently occuring categories first
        self.category_order = [c for (c,count) in sorted([ (cat,self.category_counts[self.axis_pair_count][cat]) for cat in self.category_counts[self.axis_pair_count]],key=lambda x:x[1],reverse=False)]

        # for any categories not featured in the last axis, add them to the global order
        for c in self.categories:
            if c not in self.category_order:
                self.category_order.append(c)

        # construct the axes
        self.axes = []

        for axis in range(0,self.axis_pair_count):
            self.axes.append(([],[]))
            for side in [0, 1]:
                otherside = 1 - side
                for cat0 in self.category_order:
                    for cat1 in self.category_order:
                        for key in self.keys:
                            catA = self.data[key][axis+side]
                            catB = self.data[key][axis+otherside]
                            if catA == cat0 and catB == cat1:
                                self.axes[axis][side].append(key)

    def getLabel(self, category):
        if category in self.labels:
            return self.labels[category]
        else:
            return category

    def getWidth(self):
        return self.width

    def getHeight(self):
        h = self.height
        if len(self.axis_labels):
            h += self.axis_label_height
        return h

    def buildPalette(self,palette):
        self.palette = {k: col for (k, col) in palette}

    def defineGradient(self,d,cat0,cat1):
        if (cat0,cat1) in self.gradients:
            return self.gradients[(cat0,cat1)]
        lg = linear_gradient(self.palette[cat0],self.palette[cat1])
        d.add(lg)
        lgid = lg.getId()
        self.gradients[(cat0,cat1)] = lgid
        return lgid

    def draw(self, d,ox,oy):
        height = self.height / len(self.keys)

        ay = 0

        plot_width = self.width / len(self.axes)

        if len(self.axis_labels):
            ay = self.axis_label_height
            for axis in range(0,len(self.axes)+1):
                axis_label_x = (ox - self.width / 2) + axis * plot_width
                axis_label_y = oy
                t = text(axis_label_x, axis_label_y, self.axis_labels[axis])
                t.addStyle("font-size", self.axis_label_height)
                if axis == 0:
                    pos = "start"
                elif axis == len(self.axes):
                    pos = "end"
                else:
                    pos = "middle"
                t.addStyle("text-anchor", pos)
                d.add(t)

        grp = group()
        d.add(grp)

        for axis in range(0,len(self.axes)):
            axis_x0 = (ox-self.width/2)+axis*plot_width
            axis_x1 = (ox-self.width/2)+(axis+1)*plot_width

            points0 = self.axes[axis][0]
            points1 = self.axes[axis][1]

            state = None
            for idx in range(0,len(points0)):
                key = points0[idx]
                cat0 = self.data[key][axis]
                cat1 = self.data[key][axis+1]
                oidx = points1.index(key)
                if state == None:
                    state = (cat0,cat1,(idx,idx),(oidx,oidx))
                else:
                    (pcat0,pcat1,(pidx_min,pidx_max),(poidx_min,poidx_max)) = state
                    if cat0 == pcat0 and cat1 == pcat1:
                        state = (cat0,cat1,(pidx_min,idx),(min(oidx,poidx_min),max(oidx,poidx_max)))
                    else:
                        count = 1 + pidx_max - pidx_min
                        self.drawConnection(d,grp,axis_x0,axis_x1,ay+oy,100,height,state,self.getLabel(pcat0)+"=>"+self.getLabel(pcat1)+"(%d seats)"%(count))
                        state = (cat0, cat1, (idx, idx), (oidx, oidx))
            if state != None:
                (pcat0, pcat1, (pidx_min, pidx_max), (poidx_min, poidx_max)) = state
                count = 1 + pidx_max - pidx_min
                self.drawConnection(d,grp,axis_x0, axis_x1, ay+oy, 100,height, state, pcat0 + "=>" + pcat1+"(%d seats)"%(count))

    def drawConnection(self,diagram,group,axis_x0,axis_x1,oy,width,height,state,tooltip):
        (pcat0, pcat1, (pidx_min, pidx_max), (poidx_min, poidx_max)) = state
        if pcat0 == pcat1:
            fill = self.palette[pcat0]
        else:
            fill = "url(#"+self.defineGradient(diagram,pcat0,pcat1)+")"
        p = polygon([(axis_x0, oy + pidx_min * height),("C"),(axis_x0 + width, oy + pidx_min * height),(axis_x1 - width, oy + poidx_min * height),
                     (axis_x1, oy + poidx_min * height),("L"),
                     (axis_x1, oy + poidx_max * height + height),("C"), (axis_x1 - width, oy + poidx_max * height + height),(axis_x0 + width, oy + pidx_max * height + height),
                     (axis_x0, oy + pidx_max * height + height)], "grey", "", 0, tooltip)
        p.addStyle("fill",fill)
        p.addHandler("click","bringToFront")
        group.add(p)