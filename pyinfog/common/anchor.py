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

from pyinfog.svg.pysvg import anchor
from pyinfog.common.diagram_element import DiagramElement

class Anchor(DiagramElement):

    def __init__(self,name):
        DiagramElement.__init__(self)
        self.name = name

    def getHeight(self):
        return 0

    def getWidth(self):
        return 0

    def draw(self,d,ox,oy):
        t = anchor(ox,oy,self.name)
        d.add(t)
