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

from math import pi
from pyinfog.svg.pysvg import sector,curvedtext
from pyinfog.common.diagram_element import DiagramElement

class ContinuousPlot(DiagramElement):

    def __init__(self, title, title_height, title_style, innerR, outerR, data, labels):
        DiagramElement.__init__(self)
        self.title = title
        self.innerR = innerR
        self.outerR = outerR
        self.ordered_list = sorted([(data[key], key) for key in data], reverse=True)
        self.palette = None
        self.title_font_height = title_height
        self.data = data
        self.labels = labels
        self.totald = sum([d for (d,cat) in self.ordered_list])
        self.title_font_style = title_style

    def getWidth(self):
        return self.outerR*2

    def getHeight(self):
        h = self.outerR
        return h

    def buildPalette(self,palette):
        self.palette = {k: col for (k, col) in palette}

    def getLabel(self, category):
        if category in self.labels:
            return self.labels[category]
        else:
            return category

    def getTooltip(self, category):
        c = self.data[category]
        return self.getLabel(category) + ": " + str("%d, %0.1f" % (c, 100 * (c / self.totald)) + "% votes")

    def draw(self, d,ox,oy):

        theta = 0
        for (v,cat) in self.ordered_list:
            angle = pi*v/self.totald
            s = sector(ox, oy, self.innerR, self.outerR, theta, theta+angle, self.getTooltip(cat))
            s.addStyle("fill", self.palette[cat])
            d.add(s)
            theta += angle

        if self.title:
            ct = curvedtext(ox, oy, self.outerR+5, self.title)
            ct.addStyle("font-size",self.title_font_height)
            ct.addStyles(self.title_font_style)
            d.add(ct)
