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

from math import pi,sin,cos

from pyinfog.svg.pysvg import circle,curvedtext
from pyinfog.common.diagram_element import DiagramElement

class DiscretePlot(DiagramElement):

    class Seat:

        def __init__(self,row,theta,distance):
            self.row = row
            self.theta = theta
            self.distance = distance
            self.category = ""

        def __repr__(self):
            return "Seat(row=%d,theta=%f)"%(self.row,self.theta)

        def getCoordinates(self):
            return (-self.distance*cos(self.theta),-self.distance*sin(self.theta))


    def __init__(self, title, title_height, title_style, innerR, outerR, data, labels):
        DiagramElement.__init__(self)
        self.title = title
        self.originalInnerR = innerR
        self.originalOuterR = outerR
        self.innerR = innerR
        self.outerR = outerR
        self.count_party_list = sorted([(data[key], key) for key in data], reverse=True)
        self.seatcount = sum([cc[0] for cc in self.count_party_list])
        self.palette = None
        self.title_font_height = title_height
        self.title_font_style = title_style
        self.data = data
        self.labels = labels

    def computeRadii(self, forRows):
        if forRows == 1:
            return ([(self.innerR + self.outerR) / 2.0], self.innerR + self.outerR)
        else:
            spacing = (self.outerR - self.innerR) / (forRows - 1)
            radii = [self.innerR]
            for row in range(1, forRows):
                radii.append(self.innerR + spacing * row)
            return (radii, spacing)

    def computeRowCount(self):
        # work out how many rows
        rows = 1
        while True:
            (radii, spacing) = self.computeRadii(rows)
            length = sum([pi * r for r in radii])
            rowspacing = length / self.seatcount
            if rowspacing > spacing:
                if rows == 1:
                    return 1
                return rows - 1
            rows += 1

    def computeSeats(self):
        rows = self.computeRowCount()
        radii = self.computeRadii(rows)[0]
        tracksizes = [pi * r for r in radii]
        totallen = sum(tracksizes)
        rowspacing = totallen / self.seatcount
        if len(radii) > 1:
            r_est = rowspacing * 0.4
            self.innerR = self.originalInnerR + r_est
            self.outerR = self.originalOuterR - r_est
            rows = self.computeRowCount()
            radii = self.computeRadii(rows)[0]
            tracksizes = [pi * r - 2*r_est for r in radii]
            totallen = sum(tracksizes)
            rowspacing = totallen / self.seatcount
            r = rowspacing * 0.4
        else:
            r = rowspacing * 0.4
            rlimit = (self.outerR-self.innerR)/2
            r = min([r,rlimit])

        # allocate seat count for all bt outermost row
        seat_allocation = [round(tracksizes[row] / rowspacing) for row in range(0, rows-1)]
        # allocate remaining seats to the outermost row
        seat_allocation.append(self.seatcount-sum(seat_allocation))
        seats = []
        for row in range(0, rows):
            colcount = seat_allocation[row]
            row_offset = r/radii[row]
            for col in range(0, colcount):
                seats.append(DiscretePlot.Seat(row, row_offset+ (pi-2*row_offset)*(col /(colcount-1)), radii[row]))

        return (r, sorted(seats, key=lambda s: (s.theta, s.row)))

    def allocatePartiesToSeats(self):
        (r, seats) = self.computeSeats()
        idx = 0
        for (count, party) in self.count_party_list:
            for c in range(0, count):
                seats[idx].party = party
                idx += 1

        return (r, seats)

    def getWidth(self):
        return self.outerR*2

    def getHeight(self):
        h = self.outerR
        return h

    def buildPalette(self,palette):
        self.palette = {k: col for (k, col) in palette}

    def getTooltip(self,category):
        c = self.data[category]
        return self.getLabel(category)+": "+str("%d, %0.1f"%(c,100*(c/self.seatcount))+"% seats")

    def getLabel(self,category):
        if category in self.labels:
            return self.labels[category]
        else:
            return category

    def draw(self,d,ox,oy):

        (r, seats) = self.allocatePartiesToSeats()

        for s in seats:
            (x, y) = s.getCoordinates()
            circ = circle(ox + x, oy + y, r, self.palette[s.party], self.getTooltip(s.party))
            circ.addStyle("stroke-width",r/10)
            circ.addStyle("stroke","black")
            d.add(circ)

        if self.title:
            ct = curvedtext(ox, oy, self.originalOuterR+5, self.title)
            ct.addStyle("font-size",self.title_font_height)
            ct.addStyles(self.title_font_style)
            d.add(ct)
