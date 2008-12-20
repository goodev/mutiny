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

"""Request handlers."""

__author__ = "bslatkin@gmail.com (Brett Slatkin)"

import cgi
import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.runtime import apiproxy_errors

import route_data
import models

################################################################################

MAPS_KEY = ("ABQIAAAAEhPt6lniI7PtNdH5EOTtfRT8Hg1DhyUDIGz"
            "Bx8TriLCFmc-S6xRTVvJMUhONCEdk7D_jdspn_9xiSA")

################################################################################

class PopulateHandler(webapp.RequestHandler):
  def get(self):
    start_index = int(self.request.get("index", 0))
    end = int(self.request.get("end", len(route_data.ALL_STOPS)))
    if start_index >= end:
      return self.response.out.write("Done!")

    stop_entities = []
    for index in xrange(start_index, start_index + 10):
      if index >= end:
        break
      stop_id = route_data.ALL_STOPS[index]
      (title, lat, lon, in_routes, out_routes) = route_data.STOP_BY_ID[stop_id]
      stop_entities.append(models.MuniStop.create(
          system="sf-muni", stop_id=stop_id,
          in_routes=sorted(in_routes), out_routes=sorted(out_routes),
          lat=lat, lon=lon))
    
    text = "Putting %d entities for start_index %d of %d" % (
        len(stop_entities), start_index, end)

    refresh_time = 0
    try:
      db.put(stop_entities)
    except (apiproxy_errors.Error, db.Error), e:
      text += ". Error: " + str(e)
      refresh_time = 5

    self.response.out.write(
      '<html><head><meta http-equiv="refresh" '
      'content="%d;url=/populate?index=%d&end=%d"></head><body>%s'
      '</body></html>' % (refresh_time, index + 1, end, text))


class DeleteHandler(webapp.RequestHandler):
  def get(self):
    text = ""
    refresh_time = 5
    try:
      stops = models.MuniStop.all().fetch(50)
      if not stops:
        return self.response.out.write("Done!")
      text = "Deleting %s" % len(stops)
      db.delete(stops)
      refresh_time = 0
    except (apiproxy_errors.Error, db.Error), e:
      text += "Error: %s" % e

    self.response.out.write(
      '<html><head><meta http-equiv="refresh" '
      'content="%d;url=/delete"></head><body>%s'
      '</body></html>' % (refresh_time, text))


class MainHandler(webapp.RequestHandler):
  def get(self):
    lat = self.request.get("lat", "")
    lon = self.request.get("lon", "")
    num = int(self.request.get("num", 10))
    direction = self.request.get("dir", "in").lower()
    inbound = direction == "in"

    if lat and lon:
      lat, lon = float(lat), float(lon)
      results = models.MuniStop.query("sf-muni", lat, lon, inbound, num, (2, 0))
    else:
      return self.redirect("/m")
    
    stops = []
    for result in results:
      stop = result[1]
      if inbound:
        routes = stop.in_routes
      else:
        routes = stop.out_routes

      route_dicts = []
      for route in routes:
        next_route = {
          "route": route,
          "title": route_data.ROUTE_BY_NUMBER[route],
        }
        route_dicts.append(next_route)

      next_stop = {
        "distance": result[0],
        "stop_id": stop.stop_id,
        "title": stop.title,
        "location": stop.location,
        "routes": route_dicts,
        "system": stop.system,
      }
      stops.append(next_stop)

    # Roughly 1/4 miles
    offset = 0.005

    context = {
      "dir": direction,
      "inbound": inbound,
      "lat": lat,
      "lon": lon,
      "mapurl": self.get_map_url(lat, lon, results),
      "num":  num,
      "results": stops,
      "up": self.get_offset_url(lat, lon, offset, 0, num, direction),
      "left": self.get_offset_url(lat, lon, 0, -offset, num, direction),
      "right": self.get_offset_url(lat, lon, 0, offset, num, direction),
      "down": self.get_offset_url(lat, lon, -offset, 0, num, direction),
    }
    self.response.out.write(template.render("main.html", context))
  
  @staticmethod
  def get_offset_url(lat, lon, lat_offset, lon_offset, num, direction):
    return "/?lat=%lf&lon=%lf&num=%d&dir=%s" % (
        lat + lat_offset, lon + lon_offset, num, direction)

  @staticmethod
  def get_map_url(lat, lon, results):
    config = {
      "lat": lat,
      "lon": lon,
      "width": 300,
      "height": 200,
      "maptype": "mobile",
      "mapskey": MAPS_KEY,
      "zoom": 15,
    }
    urlbase = "http://maps.google.com/staticmap?"
    params = [
      "key=%(mapskey)s"
      "&size=%(width)sx%(height)s"
      "&zoom=%(zoom)s"
      "&maptype=%(maptype)s"
      "&format=png"
      "&sensor=false" % config
    ]
    markers = [
      "&markers=%s,%s,red" % (lat, lon),
    ]
    for i, (distance, stop) in enumerate(results[:9]):
      markers.append("|%f,%f,midblue%d" %
          (stop.location.lat, stop.location.lon, i + 1))
    return urlbase + "".join(params + markers)

################################################################################

application = webapp.WSGIApplication([
  (r'/', MainHandler),
  (r'/delete', DeleteHandler),
  (r'/populate', PopulateHandler),
], debug=True)


def main():
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
