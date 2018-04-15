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
from pyinfog.infogs.transition.discreteplot import DiscretePlot

class Transition(DiagramElement):

    def __init__(self, width, height, data, palette, labels, axis_labels=[], axis_label_height=16):
        """
        Add a Transition plot to the section

        :param width: the width of the plot in pixels
        :param height: the height of the plot in pixels
        :param data: data describing a set of transitions in the form of a dictionary mapping an item id to a tuple(category0,category1) denoting a transition between categories
        :param palette: a list of (category, colour) pairs
        :param labels: dict associating each category with a longer string label
        :param axis_labels: list containing the labels for each of the two axes
        :param axis_label_height: height of the axis label text
        """

        DiagramElement.__init__(self)
        self.palette = palette
        self.labels = labels
        self.plot = DiscretePlot(width, height, data, self.labels, axis_labels,axis_label_height)
        self.plot.buildPalette(self.palette)

    def getWidth(self):
        return self.plot.getWidth()

    def getHeight(self):
        return self.plot.getHeight()

    def draw(self,d,ox,oy):
        self.plot.draw(d,ox,oy)
