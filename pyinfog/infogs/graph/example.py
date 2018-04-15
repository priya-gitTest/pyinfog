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

from pyinfog.diagram import Diagram
from pyinfog.infogs.graph.graph import Graph

import os.path
import sys

if __name__ == "__main__":

    palette = [("A","green"),("B","blue"),("C","red"),("D","yellow")]
    labels = { "A": "The A Party", "B":"The B Party", "C":"C Party", "D":"D Party","id0":"Node 0","id3":"Node 3" }

    nodes = [("id0","A",20),("id1","B",30),("id2","C",40),("id3","D",50)]
    links = [("id0","id1",10),("id1","id2",20),("id2","id3",30)]

    data = (nodes,links)

    p = Diagram()
    n = p.addNarrative()
    n.addText("Graph Example",font_size=50,font_style={"stroke":"purple"})
    n.addSpace(20,20)
    n.add(Graph(data, 400, 400, palette,labels))
    n.addSpace(20,20)
    n.addLegend(palette,labels,400,legend_columns=2)

    svg = p.draw()

    folder = os.path.split(sys.argv[0])[0]
    outputpath=os.path.join(folder,"example.svg")
    f = open(outputpath, "wb")
    f.write(svg)
    f.close()

