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

from pyinfog.svg.pysvg import text, rectangle
from pyinfog.common.diagram_element import DiagramElement

class TextInsert(DiagramElement):

    def __init__(self,textstr,fontheight,fontstyle,url=None):
        DiagramElement.__init__(self)
        self.textstr = textstr
        self.fontheight = fontheight
        self.fontstyle = fontstyle
        self.url = url
        self.width = 0
        self.height = 0

    def getHeight(self):
        return 2*self.fontheight

    def getWidth(self):
        return len(self.textstr)*self.fontheight

    def draw(self,d,ox,oy):
        t = text(ox,oy+self.getHeight()/2,self.textstr)
        if self.fontstyle:
            for k in self.fontstyle:
                t.addStyle(k,self.fontstyle[k])
        if self.url:
            t.setUrl(self.url)
        t.addAttr("font-size",self.fontheight)
        t.addStyle("text-anchor", "middle")
        d.add(t)


class Button(TextInsert):

    def __init__(self,textstr,fontheight,fontstyle,url,fill,stroke,stroke_width,r):
        TextInsert.__init__(self,textstr,fontheight,fontstyle,url)
        self.fill = fill
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.r = r

    def draw(self,d,ox,oy):
        button_width = self.getWidth()
        button_height = self.fontheight * 1.5
        r = rectangle(ox-button_width/2,oy,button_width,button_height,self.fill,self.stroke,self.stroke_width,self.r,self.r)
        d.add(r)
        TextInsert.draw(self,d,ox,oy)

    def getWidth(self):
        return len(self.textstr) * self.fontheight + 10