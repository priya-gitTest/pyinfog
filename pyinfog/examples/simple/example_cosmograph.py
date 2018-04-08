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

# data uk_election_results_2010_2015.json collected from http://lda.data.parliament.uk/
# see pyinfog/examples/download_uk_election_data.py

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
    p.addInfographic("cosmograph",palette,labels) \
        .addDiscretePlot(1024, 512, seat_changes, axis_labels=["2009", "2011"])
    p.addVerticalSpace(20)
    p.addLegend(palette,labels,legend_columns=3)
    svg = d.draw()

    folder = os.path.split(sys.argv[0])[0]
    outputpath = os.path.join(folder,"example_cosmograph.svg")
    f = open(outputpath, "wb")
    f.write(svg)
    f.close()

