#!/usr/bin/env python
# vim: set ts=2 expandtab:
"""
Module: get_program.py
Desc: Extract ARIB CCs from an MPEG transport stream and produce an .ass subtitle file off them.
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

"""

channels = {
  "TBS" : 43718,
  "AETV" : 10035, # A&E
  "WDSCDT" : 43718,
}


def get_channel_info(channel):
  """
  Just simply print current channel info for given channel.
  """
  global channels

  id = channels[channel]
  url = 'http://api.zap2it.com/tvlistings/webservices/whatson?stnlt={id}'.format(id=id)

  # fetch the json info for this url and extract what we want.
  json_url = urlopen(url)
  data = json.loads(json_url.read())

  # debug
  #print data
  date = data['results']['schedules'][0]['date']
  time = data['results']['schedules'][0]['time']
  endtime = data['results']['schedules'][0]['endTime']
  duration = data['results']['schedules'][0]['duration']
  title = data['results']['schedules'][0]['title']
 
  print date
  print time
  print endtime
  print duration
  print title

def main():

  global channels
  
  parser = argparse.ArgumentParser(
    description='Fetch current program info')
  parser.add_argument('channel', help='Station name (e.g. TBS) case insensitive.', type=str)
  args = parser.parse_args()
  
  # force all uppercase for channel names
  channel = args.channel.upper()

  if not channel in channels:
    print("Channel {c} not supported.".format(c=channel))
    sys.exit(-1)

  get_channel_info(channel)

  sys.exit(0)

if __name__ == "__main__":
  main()

