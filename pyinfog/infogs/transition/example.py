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
import os
import sys
from pyinfog.infogs.transition.transition import Transition


if __name__ == "__main__":

    palette = [("A", "green"), ("B", "blue"), ("C", "red")]
    labels = {"A": "The A Party", "B": "The B Party", "C": "C Party"}

    seat_changes = {
        "AnyTown": ("A","B"),
        "SmallTown": ("A","B"),
        "BigTown": ("B","C"),
        "SeaTown": ("B", "A"),
        "HillTown": ("A","C"),
        "StrangeTown": ("A","B"),
        "NowhereTown": ("B","C"),
        "FunnyTown": ("A","B")
    }

    d = Diagram()
    p = d.addNarrative()
    p.addText("Election Results",font_size=32,font_style={"stroke":"purple"})
    p.addText("Seats changing party, %s election - %s election"%("2009","2011"), font_size=28, font_style={"font-weight": "bold"})
    p.add(Transition(1024, 512, seat_changes,palette,labels,axis_labels=["2009", "2011"]))
    p.addSpace(20,20)
    p.addLegend(palette,labels,1024, legend_columns=3)
    svg = d.draw()

    folder = os.path.split(sys.argv[0])[0]
    outputpath = os.path.join(folder,"example.svg")
    f = open(outputpath, "wb")
    f.write(svg)
    f.close()

