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

"""Generates a map of route numbers to route names.

To run:
  generate_routes.py xmlfile1 xmlfile2 xmlfile3 ...
"""

__author__ = "bslatkin@gmail.com (Brett Slatkin)"

import sys
from xml.etree import cElementTree as ElementTree


def main(argv):
  for filename in argv[1:]:
    doc = ElementTree.parse(open(filename))
    route = doc.find("//route")
    assert route is not None, "Could not find <route> for %s" % filename
    route_number = route.get("tag")
    route_title = route.get("title")
    print '  "%s": "%s",' % (route_number, route_title)


if __name__ == "__main__":
  main(sys.argv)
