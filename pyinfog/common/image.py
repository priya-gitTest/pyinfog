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

from pyinfog.svg.pysvg import image
from pyinfog.common.diagram_element import DiagramElement
import base64

class Image(DiagramElement):

    def __init__(self,mimeType,content_bytes,width,height,tooltip=""):
        DiagramElement.__init__(self)
        self.mimeType=mimeType
        self.contentBytes=content_bytes
        self.width=width
        self.height=height
        self.tooltip=tooltip

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def draw(self,d,ox,oy):
        uri="data:"+self.mimeType+";charset=US-ASCII;base64,"+str(base64.b64encode(self.contentBytes),"utf-8")
        i = image(ox-self.width/2,oy,self.width,self.height,uri,tooltip=self.tooltip)
        d.add(i)
