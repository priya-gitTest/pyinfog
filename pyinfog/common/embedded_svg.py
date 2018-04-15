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

from pyinfog.svg.pysvg import embedded_svg
from pyinfog.common.diagram_element import DiagramElement

class EmbeddedSvg(DiagramElement):

    def __init__(self,width,height,content):
        DiagramElement.__init__(self)
        self.width = width
        self.height = height
        self.content = content

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def draw(self,d,ox,oy):
        es = embedded_svg(self.width,self.height,ox-self.width/2,oy,self.content)
        d.add(es)
