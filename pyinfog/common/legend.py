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

from pyinfog.svg.pysvg import text, polygon
from pyinfog.common.diagram_element import DiagramElement

class Legend(DiagramElement):
    """
    Manage a diagram legend associating category values with colours
    """

    def __init__(self,palette,labels,legend_columns=1,legend_font_height=24,legend_text_style={}):
        """
        Create a Legend

        :param palette:
        :param labels:
        :param legend_columns:
        :param legend_font_height:
        :param legend_text_style:
        """
        DiagramElement.__init__(self)
        self.palette = palette
        self.labels = labels
        self.legend_gap = 20
        self.legend_columns = legend_columns
        self.legend_font_height = legend_font_height
        self.legend_text_style = legend_text_style

    def build(self,w):
        self.width = w

    def getHeight(self):
        return (self.legend_font_height*len(self.palette)*2) // self.legend_columns

    def getWidth(self):
        return 0

    def draw(self,d,ox,oy):

        legend_column_width = self.width / self.legend_columns
        legend_y = oy + self.legend_gap + self.legend_font_height
        legend_x = ox - (self.width/2)
        col = 0
        for (category, colour) in self.palette:
            g = self.legend_font_height
            points = [(legend_x, legend_y), (legend_x + g, legend_y), (legend_x + g, legend_y + g),
                      (legend_x, legend_y + g)]
            d.add(polygon(points, colour, "black", 2))
            t = text(legend_x+1.5*g, legend_y+g/2, self.labels[category])
            t.addStyle("font-size", self.legend_font_height)
            t.addStyle("text-anchor", "start")
            t.addStyle("alignment-baseline", "middle")
            t.addStyles(self.legend_text_style)
            d.add(t)
            col += 1
            if col >= self.legend_columns:
                legend_y += 2 * g
                legend_x = ox - (self.width/2)
                col = 0
            else:
                legend_x += legend_column_width
