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
from pyinfog.infogs.hemicycle.hemicycle import HemiCycle

import argparse
import json



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputdatapath", help="path to read input JSON", default="uk_election_results.json")
    parser.add_argument("--inputmetadatapath", help="path to read input metadata JSON", default="uk_party_metadata.json")
    parser.add_argument("--outputpath", help="path to write output svg to",default="hemicycle_ukelection.svg")
    parser.add_argument("--year", default="2017", help="year of general election to display")

    args = parser.parse_args()

    metadata = json.loads(open(args.inputmetadatapath).read())
    parties = metadata["parties"]

    palette = []
    labels = {}
    for party_name in parties:
        party = parties[party_name]
        palette.append((party_name,party["colour"]))
        labels[party_name] = party["name"]

    data = json.loads(open(args.inputdatapath).read())

    seats = {
    }

    votes = {
    }

    for d in data:
        seat = d["constituency"]["label"]["_value"]
        election = d["election"]["label"]["_value"]

        if election == args.year+" General Election":
            result = d["resultOfElection"].split(" ")[0].upper()
            party = result
            if result not in parties:
                party = "OTHER"
            if party not in seats:
                seats[party] = 0
            seats[party] += 1
            for candidate in d["candidate"]:
                candidate_party = candidate["party"]["_value"].upper()
                if candidate_party not in parties:
                    candidate_party = "OTHER"
                if candidate_party not in votes:
                    votes[candidate_party] = 0
                votes[candidate_party] += candidate["numberOfVotes"]

    d = Diagram()
    p = d.addNarrative()
    p.addText("UK General Election "+args.year,font_size=32,font_style={"stroke":"purple"})
    p.addText("Results",font_size=28,font_style={"font-weight":"bold"})
    p.addSpace(20,20)
    h = HemiCycle(palette,labels)
    h.addContinuousPlot("Votes", 500, 600, votes)
    h.addDiscretePlot("Parliamentary Seats", 150, 450, seats)
    p.addSpace(20,20)
    p.addText("source: http://explore.data.parliament.uk/?learnmore=Election Results",font_size=20,url="http://explore.data.parliament.uk/?learnmore=Election%20Results")
    p.addLegend(palette,labels,500,legend_columns=3)

    svg = d.draw()

    f = open(args.outputpath, "wb")
    f.write(svg)
    f.close()

