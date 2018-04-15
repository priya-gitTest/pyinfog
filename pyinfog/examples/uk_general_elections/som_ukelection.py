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
import random
import json
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--inputdatapath", help="path to read input JSON", default="uk_election_results.json")
    parser.add_argument("--inputmetadatapath", help="path to read input metadata JSON",
                        default="uk_party_metadata.json")
    parser.add_argument("--outputpath", help="path to write output svg to", default="som_ukelection.svg")
    parser.add_argument("--year", help="chart results from general election in this year", default="2017")
    args = parser.parse_args()

    inputdata = json.loads(open(args.inputdatapath).read())

    metadata = json.loads(open(args.inputmetadatapath).read())
    parties = metadata["parties"]
    aliases = metadata["aliases"]

    palette = []
    labels = {}
    for party_name in parties:
        party = parties[party_name]
        palette.append((party_name, party["colour"]))
        labels[party_name] = party["name"]

    seats = {}

    for d in inputdata:
        seat = d["constituency"]["label"]["_value"]
        election = d["election"]["label"]["_value"]

        if election == args.year+" General Election":
            result = d["resultOfElection"].split(" ")[0].upper()
            party = result
            if result not in parties:
                party = "OTHER"

            seats[seat] = {}

            for candidate in d["candidate"]:
                candidate_party = candidate["party"]["_value"].upper()
                if candidate_party not in parties:
                    candidate_party = "OTHER"
                seats[seat][candidate_party] = candidate["numberOfVotes"]

    data = []

    for seat in seats.keys():
        sd = seats[seat]
        totalVotes = 0
        for party in sd.keys():
            totalVotes += sd[party]

        vec = []
        for (party,col) in palette:
            if party in sd:
                vec.append(sd[party]/totalVotes)
            else:
                vec.append(0.0)
        data.append((seat,vec))


    d = Diagram()
    p = d.addNarrative()
    p.addText("SOM TEST",font_size=32,font_style={"stroke":"purple"})
    p.add(SOMPlot(data,800,10,10,100,palette,labels))
    p.addText("SOM TEST", font_size=32, font_style={"stroke": "purple"})

    svg = d.draw()

    f = open(args.outputpath, "wb")
    f.write(svg)
    f.close()
