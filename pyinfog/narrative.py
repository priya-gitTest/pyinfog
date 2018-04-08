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

from pyinfog.common.legend import Legend
from pyinfog.common.space import VerticalSpace
from pyinfog.common.textinsert import TextInsert
from pyinfog.infogs.cosmograph.section import Section as CosmoSection
from pyinfog.infogs.hemicycle.section import Section as HemiSection
from pyinfog.infogs.somplot.section import Section as SOMPlotSection
from pyinfog.svg.pysvg import svgdoc,javascript_snippet


class Narrative:
    """
    Represent a diagram-narrative contining one or more infographics or other elements
    """

    def __init__(self,hmargin=100,vmargin=50,min_width=0):
        """

        :param hmargin: horizontal margin for the diagram (pixels)
        :param vmargin: vertical margin for the diagram (pixels)
        :param min_width: minimum width for the diagram (pixels)

        :Example:


          d = Diagram() # create a diagram
          n = d.addNarrative()
          n.addText("Here is some text")

        """
        self.hmargin = hmargin
        self.vmargin = vmargin
        self.min_width = min_width
        self.elements = []

    def getWidth(self):
        return 2*self.hmargin+max([self.min_width]+[e.getWidth() for e in self.elements])

    def getHeight(self):
        return 2*self.vmargin+sum([e.getHeight() for e in self.elements])

    def addVerticalSpace(self,pixels):
        """
        Add vertical whitespace to the diagram

        :param pixels: height of the whitespace in pixels
        :return: VerticalSpace object
        """
        e = VerticalSpace(pixels)
        self.elements.append(e)
        return e

    def addText(self,text,font_size,font_style={},url=None):
        """
        Add text to the diagram

        :param text: the text to add
        :param font_size: font size in pixeks
        :param font_style: (optional) a dict containing style name/value pairs
        :param url: (optional) url to link to from the text
        :return: TextInsert object
        """
        e = TextInsert(text,font_size,font_style,url)
        self.elements.append(e)
        return e

    def addInfographic(self,type,palette,labels):
        """
        Add an infographic section to the diagram.

        :param type: the type of the infographic (ie "somplot"|"hemicycle"|"cosmograph")
        :param palette: a list of (category, colour) pairs
        :param labels: a dict mapping category values to a descriptive label for that category
        :return: a HemiSection object
        """
        e = None
        if type == "hemicycle":
            e = HemiSection(palette,labels)
        if type == "somplot":
            e = SOMPlotSection(palette,labels)
        if type == "cosmograph":
            e = CosmoSection(palette,labels)
        self.elements.append(e)
        return e

    def addCosmographSection(self,palette,labels):
        """
        Add a cosmograph section to the diagram.

        :param palette: a list of (category, colour) pairs
        :param labels: a dict mapping category values to a descriptive label for that category
        :return: a CosmoSection object
        """
        e = CosmoSection(palette,labels)
        self.elements.append(e)
        return e

    def addSomplotSection(self,palette,labels):
        """
        Add a Self Organising Map to the diagram.

        :param palette: a list of (category, colour) pairs
        :param labels: a dict mapping category values to a descriptive label for that category
        :return: a SOMPlot object
        """
        e = SOMPlotSection(palette,labels)
        self.elements.append(e)
        return e

    def addLegend(self,palette,labels,legend_columns=1,legend_font_size=24,legend_text_style={}):
        """
        Add a legend section to the diagram

        :param palette: a list of (category, colour) pairs
        :param labels: dict associating each category with a longer string label
        :param legend_columns: the number of columns to split the legend into (optional, defaults to 1)
        :param legend_font_size: the font size for the legend (optional, defaults to 24)
        :param legend_text_style: a dict containing style name/value pairs
        :return: a Legend object
        """
        e = Legend(palette,labels,legend_columns,legend_font_size,legend_text_style)
        self.elements.append(e)
        return e


    def draw(self,doc,ox,oy):
        """

        Draw the narrative to write graphics into an SVG document


        :param doc: the SVG document to draw into
        :param ox: the x-coordinate to start drawing the narrative (narrative should be centered on this coordinate)
        :param oy: the y-coordinate to start drawing the narrative
        :return:
        """
        for e in self.elements:
            e.build(self.getWidth())

        w = self.getWidth()

        off_y = oy
        off_x = ox

        for e in self.elements:
            e.draw(doc, off_x, off_y)
            off_y += e.getHeight()



