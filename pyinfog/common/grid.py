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

from pyinfog.common.diagram_element import DiagramElement
import base64

class Grid(DiagramElement):

    def __init__(self):
        DiagramElement.__init__(self)
        self.height = 0
        self.width = 0
        self.cells = {}
        self.col_widths = {}
        self.row_heights = {}
        self.max_row = 0
        self.max_col = 0

    def setColumnWidth(self,col,width):
        self.col_widths[col] = width

    def addCell(self,row,col,element):
        self.cells[(row,col)] = element

    def build(self):

        for (row,col) in self.cells:
            cell = self.cells[(row,col)]
            cell.build()
            if col not in self.col_widths:
                self.col_widths[col] = 0
            self.col_widths[col] = max(self.col_widths[col],cell.getWidth())
            if row not in self.row_heights:
                self.row_heights[row] = 0
            self.row_heights[row] = max(self.row_heights[row],cell.getHeight())

        self.max_row = max([row for (row,col) in self.cells])
        self.max_col = max([col for (row,col) in self.cells])
        for col in range(self.max_col+1):
            for row in range(self.max_row+1):
                col_width = 0
                row_height = 0
                if col in self.col_widths:
                    col_width = self.col_widths[col]

                if row in self.row_heights:
                    row_height = self.row_heights[row]

                if (row,col) in self.cells:
                    cell = self.cells[(row,col)]
                    cw = cell.getWidth()
                    ch = cell.getHeight()
                    col_width = max(col_width,cw)
                    row_height = max(row_height,ch)
                    self.col_widths[col] = col_width
                    self.row_heights[row] = row_height

        self.width = sum([w for w in self.col_widths.values()])
        self.height = sum([h for h in self.row_heights.values()])
        print("Grid width="+str(self.width)+",height="+str(self.height))

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def draw(self,d,ox,oy):
        ry = oy
        for row in range(self.max_row+1):
            rx = ox - self.width/2

            for col in range(self.max_col+1):
                if col in self.col_widths:
                    cw = self.col_widths[col]
                    if (row,col) in self.cells:
                        self.cells[(row,col)].draw(d,rx+cw/2,ry)
                    rx += cw
            if row in self.row_heights:
                ry += self.row_heights[row]