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

import urllib.request
import json
import os.path

page=0
results = []

while True:
    response = urllib.request.urlopen(" http://lda.data.parliament.uk/electionresults.json?_view=basic&_properties=electorate,turnout,resultOfElection,election.label,candidate.fullName,candidate.party,candidate.numberOfVotes,constituency.label&_pageSize=100&_page="+str(page))
    data = json.loads(str(response.read(),"utf-8"))
    items = data["result"]["items"]
    if len(items) == 0:
        break
    for item in items:
        results.append(item)
    page += 1

output_path = os.path.join(os.path.split(__file__)[0],"uk_election_results.json")
open(output_path,"w").write(json.dumps(results))

