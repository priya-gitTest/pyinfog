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

from pyinfog.infogs.somplot.somplot import SOMPlot

class Section(DiagramElement):
    """
    Define a diagram section to hold one or more Self Organizing Map (SOM) plots
    """

    def __init__(self, palette,labels):
        DiagramElement.__init__(self)
        self.palette = palette
        self.labels = labels
        self.plots = []

    def getWidth(self):
        return max([p.getWidth() for p in self.plots])

    def getHeight(self):
        return sum([p.getHeight() for p in self.plots])

    def build(self,w):
        for plot in self.plots:
            plot.train()

    def addSOMPlot(self, data, width, rows, cols, iters):
        """
        Add a SOM Plot to the section (the SOM is actually trained when the build method is invoked)

        :param data: data in the form of a list of (label,float_list) pairs where float_list is a list of floats
        :param width: the width of the plot in pixels
        :param rows: the number of rows in the SOM plot
        :param cols: the number of columns in the SOM plot
        :param iters: the number of training iterations to use when training the SOM
        :return: a SOMPlot object
        """
        p = SOMPlot(data, width, rows, cols, iters, self.palette, self.labels)
        self.plots.append(p)
        return self

    def draw(self,d,ox,oy):
        py = oy
        for plot in self.plots:
            plot.draw(d,ox,py)
            py += plot.getHeight()

