# Copyright 2017 Niall McCarroll
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

from pyinfog.narrative import Narrative
from pyinfog.svg.pysvg import svgdoc,javascript_snippet


class Diagram:
    """
    Represent a diagram contining one or more infographics
    """

    def __init__(self,hmargin=100,vmargin=100,narrative_spacing=800):
        """

        :param narrative_spacing: spacing between narratives


        :Example:


          d = Diagram() # create a diagram
          n1 = d.addNarrative()

        """
        self.hmargin = hmargin
        self.vmargin = vmargin
        self.narrative_spacing = narrative_spacing
        self.narratives = []


    def addNarrative(self,min_width=0):
        n = Narrative(min_width)
        self.narratives.append(n)
        return n


    def draw(self):
        """
        Draw the diagram to create an SVG document

        :return: string containing the SVG document
        """

        w = sum([n.getWidth() for n in self.narratives])
        if len(self.narratives)>1:
            w += self.narrative_spacing * (len(self.narratives)-1)
        h = max([n.getHeight() for n in self.narratives])

        w += self.hmargin*2
        h += self.vmargin*2

        d = svgdoc(w, h)
        d.add(javascript_snippet('function bringToFront(evt) { var p = evt.target.parentNode.parentNode; var c = evt.target.parentNode; p.removeChild(c); p.appendChild(c); }'))

        off_x = self.hmargin
        off_y = self.vmargin

        for n in self.narratives:
            n.draw(d, off_x+n.getWidth()/2, off_y)
            off_x += n.getWidth() + self.narrative_spacing

        return d.render()

