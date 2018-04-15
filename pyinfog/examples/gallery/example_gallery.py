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


if __name__ == "__main__":

    folder = os.path.split(sys.argv[0])[0]

    d = Diagram()
    n0 = d.addNarrative()
    n0.addImage("image/jpeg",open(os.path.join(folder,"..","..","..","pyinfog.jpg"),"rb").read(),290,82,"python logo")
    n0.addText("Infographic Gallery",font_size=48)

    n1 = n0.addNarrative()

    infogs_folder=os.path.join(folder, "..","..","infogs")
    row = 0
    for infog_folder in os.listdir(infogs_folder):

        if os.path.exists(os.path.join(infogs_folder,infog_folder,"example.svg")):
            svg_path=os.path.join(infogs_folder,infog_folder,"example.svg")
            svg = open(svg_path).read()
            n1(row,0).addButton(infog_folder,url="#"+infog_folder,stroke="black",fill="#EEE")
            n1(row,1).addEmbeddedSvg(400, 400, svg)
            row += 1
            n = d.addNarrative()
            n.addAnchor(infog_folder)
            n.addEmbeddedSvg(800, 800, svg)

    svg = d.draw()

    outputpath = os.path.join(folder, "example_gallery.svg")
    f = open(outputpath, "wb")
    f.write(svg)
    f.close()
