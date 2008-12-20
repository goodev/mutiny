#!/usr/bin/env python
#
# All data copyright NextBus 2008.
# Allowed use is for noncommercial purposes only. 


ROUTE_BY_NUMBER = {
  "1": "1-California",
  "10": "10-Townsend",
  "108": "108-Treasure Island",
  "12": "12-Folsom / Pacific",
  "14": "14-Mission",
  "14L": "14L-Mission Limited",
  # There's more data than this, but it's copyrighted.
}


# Stops IDs in order.
ALL_STOPS = [
  390, 392, 913, 3002, 3003, 3004, 3005, 3006, 3007, 3008, 3009, 3010, 3011,
  # There's more data than this, but it's copyrighted.
]


# Maps stops to (title, latitude, longitude, inbound routes, outbound routes)
STOP_BY_ID = {
 390: ('19th Ave & Holloway Ave', 37.72119, -122.4751, ['17', '28', '28L', '29', 'M OWL'], ['91']),
 392: ('19th Ave & Lincoln Way', 37.765160000000002, -122.47721, ['28', '28L'], []),
 913: ('Dublin St & Lagrande Ave', 37.719189999999998, -122.4258, ['52'], []),
 3002: ('1st St & Mission St', 37.789399899999999, -122.3972199, ['76'], []),
 3003: ('2nd St & Brannan St', 37.781829999999999, -122.39194000000001, ['10'], []),
 3004: ('2nd St & Brannan St', 37.781849999999999, -122.39223, [], ['10']),
 3005: ('2nd St & Bryant St', 37.7832899, -122.3937799, ['10'], []),
 3006: ('2nd St & Bryant St', 37.782850000000003, -122.39346999999999, [], ['10']),
 # There's more data than this, but it's copyrighted.
}
