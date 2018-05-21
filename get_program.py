#!/usr/bin/env python
# vim: set ts=2 expandtab:
"""
Module: get_program.py
Desc: get simple program info from 'zap3it'
Author: on-three
Email: on.three.email@gmail.com
DATE: Sunday May 20th 2018
"""

import os
import errno
import sys
import argparse
import traceback

from urllib import urlopen
import json

"""

{"results": {
  "locale": "en",
  "totalPrograms": 2,
  "tvlistingsURL": "http://tvlistings.zap2it.com/tvlistings/ZCGrid.do?aid=zap2it",
  "matrixStartDate": "2018-05-19",
  "matrixEndDate": "2018-06-03",
  "schedules": [
  {
    "programId": "EP019847850019",
    "parentProgramId": "SH019847850000",
    "station": {
    "affiliate": "Independent",
    "callSign": "WDSCDT",
    "logoUrl": "//a248.e.akamai.net/f/1985/45814/1d/images.zap2it.com/station_logo/wdscdt.gif",
    "name": "WDSCDT (WDSC-DT)",
    "stationNum": 43718
  },
  "date": "2018-05-20",
  "time": "9:00 PM ET",
  "endTime": "10:00 PM ET",
  "season": 3,
  "episode": "3",
  "duration": 60,
  "stereo": true,
  "isHD": false,
  "availableInHdtv": false,

  Research:
  url: http://api.zap2it.com/tvlistings/zcConnector.jsp?ap=wo&md=getWhatsOn&v=2&aid=WBAL&zip=21211&stnlt=21231&random=1349602906090
  results in response:
  var validRequest = true; var server = "http://api.zap2it.com"; var requestParams = "ap=wo&md=getWhatsOn&v=2&aid=WBAL&zip=21211&stnlt=21231&random=1349602906090"; var action; action = "/tvlistings/ZCShowtimeAction.do?"; if(requestParams!="" && validRequest) { document.write(""); document.write(""); } else { function buildXHTML() {} }

# this url also works (uses 'aid' whatever that is)
http://api.zap2it.com/tvlistings/webservices/whatson?stnlt=70248&aid=antennatv


"""

channels = {
  "TBS" : 43718,
  "AETV" : 10035, # A&E
  "TOON" : 12131,
  "CNN" : 10142,
  "COMEDY" : 10149,
  "WDSCDT" : 43718,
  "TCM" : 12852,
  "HBO" : 10240,
  "FX" : 14321,
}

# get a value from our json dictionary with some safety
def get_value(data, key, default_value):
  try:
    v = data['results']['schedules'][0][key]
    return v
  except:
    return default_value


def get_channel_info(channel, zip_code):
  """
  Just simply print current channel info for given channel.
  """
  global channels

  id = channels[channel]
  url = 'http://api.zap2it.com/tvlistings/webservices/whatson?stnlt={id}&zip={zip}'.format(id=id, zip=zip_code)

  #debug
  print url

  # fetch the json info for this url and extract what we want.
  json_url = urlopen(url)
  data = json.loads(json_url.read())

  # debug
  # uncomment the following line to see all data available
  #print data

  # extract data we want
  # It seems sometimes elements can be missing so we probably want
  # to extract them more safely
  date = data['results']['schedules'][0]['date']
  time = data['results']['schedules'][0]['time']
  endtime = data['results']['schedules'][0]['endTime']
  duration = data['results']['schedules'][0]['duration']
  title = data['results']['schedules'][0]['title']
  # desc can be missing so rather than read it directly we do so with a fallback
  #desc = data['results']['schedules'][0]['description']
  desc = get_value(data, 'description', 'No program description available.')

  print "Date: " + date
  print "Start time: " + time
  print "End time: " + endtime
  print "Duration: " + str(duration) + " minutes."
  print "Program Title: " + title
  print "Description: " + desc

def main():

  global channels
  
  parser = argparse.ArgumentParser(
    description='Fetch current program info')
  parser.add_argument('channel', help='Station name (e.g. TBS) case insensitive.', type=str)
  parser.add_argument('-z','--zip', help='Zip code of query', type=int, default=10012)
  args = parser.parse_args()
  
  # force all uppercase for channel names
  channel = args.channel.upper()
  zip = args.zip
  if not channel in channels:
    print("Channel {c} not supported.".format(c=channel))
    sys.exit(-1)

  get_channel_info(channel, zip)

  sys.exit(0)

if __name__ == "__main__":
  main()

