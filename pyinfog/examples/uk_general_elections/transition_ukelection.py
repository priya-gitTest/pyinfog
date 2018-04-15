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
from pyinfog.infogs.transition.transition import Transition
import json
import argparse

# data uk_election_results_2010_2015.json collected from http://lda.data.parliament.uk/
# see pyinfog/examples/download_uk_election_data.py

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--inputdatapath", help="path to read input JSON", default="uk_election_results.json")
    parser.add_argument("--inputmetadatapath", help="path to read input metadata JSON", default="uk_party_metadata.json")
    parser.add_argument("--outputpath", help="path to write output svg to",default="cosmograph_ukelection.svg")
    parser.add_argument("--years",help="chart changes from general election in this year",default="2010,2015")
    args = parser.parse_args()

    years = args.years.split(",")
    from_year = years[0]
    to_year = years[1]

    data = json.loads(open(args.inputdatapath).read())

    metadata = json.loads(open(args.inputmetadatapath).read())
    parties = metadata["parties"]
    aliases = metadata["aliases"]

    palette = []
    labels = {}
    for party_name in parties:
        party = parties[party_name]
        palette.append((party_name, party["colour"]))
        labels[party_name] = party["name"]

    election_from = {}
    election_to = {}

    for d in data:
        seat = d["constituency"]["label"]["_value"]
        election = d["election"]["label"]["_value"]
        result = d["resultOfElection"].split(" ")[0].upper()
        if result in aliases:
            result = aliases[result]
        if election == from_year+" General Election":
            election_from[seat] = result
        if election == to_year+" General Election":
            election_to[seat] = result

    seats = {}
    seat_changes = {}
    for seat in election_from:
        if seat in election_to:
            seats[seat] = (election_from[seat],election_to[seat])
            if election_from[seat] != election_to[seat]:
                seat_changes[seat] = (election_from[seat],election_to[seat])

    d = Diagram()
    p = d.addNarrative()
    p.addText("UK General Election",font_size=32,font_style={"stroke":"purple"})
    p.addText("Seats changing party, %s election - %s election"%(from_year,to_year), font_size=28, font_style={"font-weight": "bold"})
    p.add(Transition(1024, 512, seat_changes, palette, labels, axis_labels=[from_year, to_year]))
    p.addSpace(20,20)
    p.addText("source: http://explore.data.parliament.uk/?learnmore=Election Results", font_size=20,
              url="http://explore.data.parliament.uk/?learnmore=Election%20Results")
    p.addLegend(palette,labels,512,legend_columns=3)

    svg = d.draw()

    f = open(args.outputpath, "wb")
    f.write(svg)
    f.close()

