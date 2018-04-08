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

from pyinfog.infogs.hemicycle.continuousplot import ContinuousPlot

from pyinfog.common.diagram_element import DiagramElement
from pyinfog.infogs.hemicycle.discreteplot import DiscretePlot


class Section(DiagramElement):

    def __init__(self, palette, labels):
        DiagramElement.__init__(self)
        self.palette = palette
        self.labels = labels
        self.plots = []

    def getWidth(self):
        return max([p.getWidth() for p in self.plots])

    def getHeight(self):
        return max([p.getHeight() for p in self.plots])

    def build(self,w):
        for p in self.plots:
            p.buildPalette(self.palette)

    def addDiscretePlot(self, title, innerR, outerR, data, title_font_size=24,title_font_style={}):
        p = DiscretePlot(title, title_font_size, title_font_style, innerR, outerR, data, self.labels)
        self.plots.append(p)
        return self

    def addContinuousPlot(self, title, innerR, outerR, data, title_font_size=24,title_font_style={}):
        p = ContinuousPlot(title, title_font_size, title_font_style, innerR, outerR, data, self.labels)
        self.plots.append(p)
        return self

    def draw(self,d,ox,oy):
        ph = max([p.getHeight() for p in self.plots])
        for p in self.plots:
            p.draw(d,ox,oy+ph)

