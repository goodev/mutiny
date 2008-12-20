#!/usr/bin/env python
#
# Copyright 2008 Brett Slatkin
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Generates a map of stops to titles, locations, and routes.

To run:
  generate_stops.py xmlfile1 xmlfile2 xmlfile3 ...
"""

__author__ = "bslatkin@gmail.com (Brett Slatkin)"

import pprint
import sys
from xml.etree import cElementTree as ElementTree


def main(argv):
  # Maps stop numbers to stop tuple (number, title, lat, lon, inbound, outbound)
  stop_table = {}
  
  for filename in argv[1:]:
    doc = ElementTree.parse(open(filename))
    route = doc.find("//route")
    assert route is not None, "Could not find <route> for " + filename
    route_number = route.get("tag")

    # Find all the stops, their names, and their coordinates.
    all_stops = doc.findall("//route/stop")
    assert all_stops, "Could not find any stops in " + filename    
    for stop_element in all_stops:
      stop_number = int(stop_element.get("tag"))
      stop = stop_table.get(stop_number)
      if stop is None:
        stop = (stop_element.get("title"), float(stop_element.get("lat")),
                float(stop_element.get("lon")), [], [])
        stop_table[stop_number] = stop

    # Find all of the directions, and record routes based on these.
    all_directions = doc.findall("//route/direction")
    assert all_directions, "Could not find any directions in " + filename
    for direction in all_directions:
      name = direction.get("name")
      if "outbound" in name.lower():
        inbound = False;
      elif "inbound" in name.lower():
        inbound = True
      else:
        assert False, ("Tag should contain inbound or outbound specifier. "
            "Found %s in file %s for direction.tag=%s" %
            (name, filename, direction.get("tag")))

      all_stops = direction.findall("stop")
      assert all_stops, "Could not find any stops for direction in " + filename
      for stop in all_stops:
        stop_number = int(stop.get("tag"))
        if inbound:
          target_list = stop_table[stop_number][3]
        else:
          target_list = stop_table[stop_number][4]
        if route_number not in target_list:
          target_list.append(route_number)
  
  pprint.pprint(stop_table, width=250)


if __name__ == "__main__":
  main(sys.argv)
