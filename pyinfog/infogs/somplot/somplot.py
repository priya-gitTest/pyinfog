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

import random
from math import radians,sin,cos

from pyinfog.common.diagram_element import DiagramElement
from pyinfog.infogs.somplot.hexgrid import HexGrid

class SOMPlot(DiagramElement):

    def __init__(self,data, width, rows, cols, iters, palette, labels):
        """
        Create a SOM Plot (the SOM is actually trained when the draw method is invoked)

        :param data: data in the form of a list of (label,float_list) pairs where float_list is a list of floats
        :param width: the width of the plot in pixels
        :param rows: the number of rows in the SOM plot
        :param cols: the number of columns in the SOM plot
        :param iters: the number of training iterations to use when training the SOM
        :param palette: a list of (category, colour) pairs
        :param labels: dict associating each category with a longer string label
        """
        self.metadata = None
        self.width = width
        self.gridheight = cols
        self.gridwidth = rows

        self.off_lg = width/(2*cols+1)
        self.dlength = self.off_lg/cos(radians(30))
        self.off_sm = self.dlength * sin(radians(30))
        self.height = rows*(self.dlength+self.off_sm)+self.off_sm

        self.palette = palette
        self.labels = labels

        self.iters = iters
        self.trained = False
        self.learnRate_initial = 0.5
        self.learnRate_final = 0.05
        self.rng = random.Random()
        self.weights = []
        self.oactivations = []

        self.neighbour_limit = 0
        self.learnRate = 0
        self.nrWeights = 0

        self.initial_neighbourhood = 4
        self.instances = data
        self.scores = {}

        seed = 0
        self.rng.seed(seed)

        self.nrInputs = len(self.instances[0][1])
        self.nrOutputs = self.gridwidth * self.gridheight
        self.hexgrid = HexGrid(self.gridwidth, self.gridheight, self.initial_neighbourhood,self)
        self.nrWeights = self.nrOutputs * self.nrInputs

        for w in range(0,self.nrWeights):
            self.weights.append((self.rng.random()/5.0)+0.4)

        for oa in range(0,self.nrOutputs):
            self.oactivations.append(0.0)

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getWeights(self,outputIndex):
        return self.weights[(self.nrInputs * outputIndex):(self.nrInputs * (outputIndex + 1))]

    def train(self):
        iteration = 0
        while iteration < self.iters:
            self.learnRate = (1.0 - float(iteration) / float(self.iters)) * (self.learnRate_initial - self.learnRate_final) + self.learnRate_final
            self.neighbour_limit = self.initial_neighbourhood - int(
                (float(iteration) / float((self.iters + 1))) * self.initial_neighbourhood)
            print("iter=%d (of %d) / learning-rate=%f / neighbourhood=%d"%(iteration,self.iters,self.learnRate,self.neighbour_limit))
            for (label,instance) in self.instances:
                winner = self.computeActivations(instance)
                self.updateNetwork(winner,instance)
            iteration += 1

    def computeActivations(self,iactivations):
        mindistance = None
        winner = -1
        # inarr = numpy.array(iactivations)
        for idx in range(0,self.nrOutputs):
            self.oactivations[idx] = self.distance(iactivations,self.weights[(self.nrInputs*idx):(self.nrInputs*(idx+1))])
            # self.oactivations[idx] = numpy.linalg.norm(inarr-numpy.array(self.getWeights(idx)))
            if winner == -1:
                mindistance = self.oactivations[idx]
                winner = idx
            else:
                if mindistance > self.oactivations[idx]:
                    mindistance = self.oactivations[idx]
                    winner = idx
        return winner

    def updateNetwork(self,winner,iactivations):
        for idx in range(0,self.nrOutputs):
            if self.isNeighbour(idx,winner):
                self.adjustWeights(idx,iactivations)

    def isNeighbour(self,output,winner):
        (ox,oy) = self.coords(output)
        (wx,wy) = self.coords(winner)
        neighbour_distance = self.hexgrid.getDistance(ox,oy,wx,wy)
        return neighbour_distance and neighbour_distance <= self.neighbour_limit

    def coords(self,output):
        return (output % self.gridwidth, output // self.gridwidth)

    def getOutput(self,x,y):
        return x + (y*self.gridwidth)

    def getAssignment(self,activations):
        mx = None
        mx_idx = 0
        for idx in range(0,len(activations)):
            a = activations[idx]
            if  mx == None or a > mx:
                mx = a
                mx_idx = idx
        return self.palette[mx_idx]

    def distance(self,array1,array2):
        total = 0.0
        for idx in range(0,len(array1)):
            dist = array1[idx]-array2[idx]
            total += (dist*dist)
        return total

    def adjustWeights(self,output,iactivations):
        for idx in range(0,self.nrInputs):
            wpos = (output*self.nrInputs)+idx
            w = self.weights[wpos]
            i = iactivations[idx]
            w = w + (self.learnRate * (i - w))
            self.weights[wpos] = w

    def draw(self,diagram,ox,oy):
        self.train()
        ox -= self.getWidth()/2
        ox += self.off_lg
        oy = oy+self.dlength + self.off_sm
        scores = {(xc, yc): [] for xc in range(0, self.gridwidth) for yc in range(0, self.gridheight)}
        for (label, instance) in self.instances:
            winner_coords = self.coords(self.computeActivations(instance))
            (party,colour) = self.getAssignment(instance)
            scores[winner_coords].append((label+" ("+party+")",colour))
        self.hexgrid.render(diagram,ox,oy,self.dlength,scores)


