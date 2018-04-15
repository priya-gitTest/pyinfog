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
from pyinfog.infogs.somplot.somplot import SOMPlot
import os
import sys


if __name__ == "__main__":
    palette = [("A", "green"), ("B", "blue"), ("C", "red")]
    labels = {"A": "The A Party", "B": "The B Party", "C": "C Party"}

    voting_data = [
        ("AnyTown",[0.7,0.2,0.1]),
        ("SmallTown",[0.55,0.45,0.0]),
        ("BigTown",[0.49,0.51,0.0]),
        ("SeaTown",[0.1,0.7,0.2]),
        ("HillTown",[0.6,0.0,0.4]),
        ("StrangeTown",[0.55,0.40,0.05]),
        ("NowhereTown",[0.1,0.8,0.1]),
        ("FunnyTown",[0.9,0.05,0.05])
    ]

    d = Diagram()
    n = d.addNarrative()
    n.add(SOMPlot(voting_data,500,4,4,100,palette,labels))
    n.addSpace(20,20)
    n.addLegend(palette,labels,500,legend_columns=2)

    svg = d.draw()

    folder = os.path.split(sys.argv[0])[0]
    outputpath = os.path.join(folder, "example.svg")
    f = open(outputpath, "wb")
    f.write(svg)
    f.close()
