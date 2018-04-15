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
from pyinfog.infogs.hemicycle.hemicycle import HemiCycle
import os.path
import sys

if __name__ == "__main__":

    palette = [("A","green"),("B","blue"),("C","red")]
    labels = { "A": "The A Party", "B":"The B Party", "C":"C Party" }

    seats = {
        "A": 25,
        "B": 21,
        "C": 8
    }

    votes = {
        "A": 2012311,
        "B": 1900000,
        "C": 1500000
    }

    p = Diagram()
    n = p.addNarrative()
    n.addText("Hemicycle Example",font_size=50,font_style={"stroke":"purple"})
    n.addText("Election Results",font_size=28,font_style={"font-weight":"bold"})
    n.addSpace(20,20)
    h = HemiCycle(palette,labels)
    h.addContinuousPlot("Election Votes", 200, 300, votes)
    h.addDiscretePlot("Parliamentary Seats", 50, 150, seats)
    n.add(h)
    n.addSpace(20,20)
    n.addLegend(palette,labels,700,legend_columns=3)

    svg = p.draw()

    folder = os.path.split(sys.argv[0])[0]
    outputpath = os.path.join(folder,"example.svg")
    f = open(outputpath, "wb")
    f.write(svg)
    f.close()

