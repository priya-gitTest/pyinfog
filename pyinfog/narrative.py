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
from pyinfog.common.anchor import Anchor
from pyinfog.common.space import Space
from pyinfog.common.textinsert import TextInsert, Button
from pyinfog.common.image import Image
from pyinfog.common.diagram_element import DiagramElement
from pyinfog.common.embedded_svg import EmbeddedSvg
from pyinfog.common.grid import Grid

from pyinfog.svg.pysvg import svgdoc,javascript_snippet, rectangle

class Narrative(DiagramElement):
    """
    Represent a diagram-narrative contining one or more infographics or other elements
    """

    def __init__(self,hmargin=100,vmargin=50,min_width=0,min_height=0,debug=False):
        """

        :param hmargin: horizontal margin for the diagram (pixels)
        :param vmargin: vertical margin for the diagram (pixels)
        :param min_width: minimum width for the diagram (pixels)
        :param min_height: minimum height for the diagram (pixels)

        :Example:


          d = Diagram() # create a diagram
          n = d.addNarrative()
          n.addText("Here is some text")

        """
        DiagramElement.__init__(self)
        self.hmargin = hmargin
        self.vmargin = vmargin
        self.min_width = min_width
        self.min_height = min_height
        self.grid = Grid()
        self.debug = debug

        self.row = 0
        self.col = 0

        self.grid.setColumnWidth(0,min_width)

    def setColumnWidth(self,col,width):
        self.grid.setColumnWidth(col,width)

    def __setPosition(self,row,col):
        self.row = row
        self.col = col
        return self

    def __call__(self,row,col):
        return self.__setPosition(row,col)

    def getWidth(self):
        return self.grid.getWidth()

    def getHeight(self):
        return self.grid.getHeight()

    def build(self):
        self.grid.build()

    def addNarrative(self,hmargin=100,vmargin=50,min_width=0,debug=False):
        n = Narrative(hmargin,vmargin,min_width,debug)
        self.add(n)
        return n

    def add(self,element):
        self.grid.addCell(self.row,self.col,element)
        self.row += 1
        return self

    def addSpace(self,width,height):
        """
        Add whitespace to the diagram

        :param width: width of the whitespace in pixels
        :param height: height of the whitespace in pixels

        :return: Space object
        """
        e = Space(width,height)
        self.add(e)
        return e

    def addAnchor(self,name):
        e = Anchor(name)
        self.add(e)
        return e

    def addText(self,text,font_size=18,font_style={},url=None):
        """
        Add text to the diagram

        :param text: the text to add
        :param font_size: font size in pixeks
        :param font_style: (optional) a dict containing style name/value pairs
        :param url: (optional) url to link to from the text
        :return: TextInsert object
        """
        e = TextInsert(text,font_size,font_style,url)
        self.add(e)
        return e

    def addButton(self,text,font_size=18,font_style={},url=None,fill="grey",stroke="darkgrey", stroke_width=10, r=3):
        """
        Add button to the diagram

        :param text: the text to add
        :param font_size: font size in pixeks
        :param font_style: (optional) a dict containing style name/value pairs
        :param url: (optional) url to link to from the text
        :param fill: (optional) the background colour
        :param stroke: (optional) the stroke colour
        :param stroke_width: (optional) the stroke width
        :param r the button corner radius
        :return: Button object
        """
        b = Button(text,font_size,font_style,url,fill,stroke,stroke_width,r)
        self.add(b)
        return b

    def addEmbeddedSvg(self,width,height,content):
        """
        Add an embedded SVG to the diagram

        :param width: width of the embedded SVG
        :param height: height of the embedded SVG
        :param content: the SVG content as a string
        """
        e = EmbeddedSvg(width,height,content)
        self.add(e)
        return e


    def addImage(self,mimeType,content_bytes,width,height,tooltip=""):
        i=Image(mimeType,content_bytes,width,height,tooltip)
        self.add(i)
        return i

    def addLegend(self,palette,labels,width,legend_columns=1,legend_font_size=24,legend_text_style={}):
        """
        Add a legend section to the diagram

        :param palette: a list of (category, colour) pairs
        :param labels: dict associating each category with a longer string label
        :param width: width of the legend area
        :param legend_columns: the number of columns to split the legend into (optional, defaults to 1)
        :param legend_font_size: the font size for the legend (optional, defaults to 24)
        :param legend_text_style: a dict containing style name/value pairs
        :return: a Legend object
        """
        e = Legend(palette,labels,width,legend_columns,legend_font_size,legend_text_style)
        self.add(e)
        return e

    def build(self):
        self.grid.build()

    def draw(self,doc,ox,oy):
        """

        Draw the narrative to write graphics into an SVG document


        :param doc: the SVG document to draw into
        :param ox: the x-coordinate to start drawing the narrative (narrative should be centered on this coordinate)
        :param oy: the y-coordinate to start drawing the narrative
        :return:
        """
        self.grid.draw(doc,ox,oy)


