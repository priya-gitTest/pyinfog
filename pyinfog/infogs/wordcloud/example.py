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
from pyinfog.infogs.wordcloud.wordcloud import WordCloud
import os.path
import sys

if __name__ == "__main__":

    palette = [("A","green"),("B","blue"),("C","red"),("D","yellow")]
    labels = {}
    folder = os.path.split(sys.argv[0])[0]

    txtdata = os.path.join(folder,"huxleya-bravenewworld-00-t.txt")

    brave_new_world = open(txtdata,"r",encoding="cp852").read()

    words = brave_new_world.replace(","," ").split(" ")
    freqs = {}
    isValid = lambda x: len(x)>5
    for word in words:
        word = word.lower()
        if isValid(word):
            if word not in freqs:
                freqs[word] = 1
            else:
                freqs[word] += 1

    data = sorted([(word,"",freqs[word]) for word in freqs],key=lambda x:x[2],reverse=True)[:100]
    p = Diagram()
    n = p.addNarrative()
    n.addText("WordCloud Example - Brave New World",font_size=50,font_style={"stroke":"purple"})
    n.addSpace(20,20)
    n.add(WordCloud(data, 600, 600, palette, labels))

    svg = p.draw()

    outputpath=os.path.join(folder,"example.svg")
    f = open(outputpath, "wb")
    f.write(svg)
    f.close()

