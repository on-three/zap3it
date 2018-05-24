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
import time

from urllib import urlopen
import json

"""

  # this is what we want, probably
  https://tvlistings.zap2it.com/api/grid?lineupId=DFLTE&timespan=2&headendId=DFLTE&country=USA&device=-&postalCode=10001&isOverride=false&time=1527109200&pref=-&userId=-&aid=zap2it

"""
"""
We may need to translate between maws names and callsigns in the zap3it data
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
"""

# get a value from our json dictionary with some safety
def get_value(obj, key, default):
  try:
    v = obj[key]
    return str(v)
  except:
    return default


def dump_program(e):
  # debug
  #print str(e)
  print "******************"
  start_time = e['startTime']
  end_time = e['endTime']
  duration = e['duration']
  program = e['program']
  title = program['title']
  episode_title = get_value(program, 'episodeTitle', "No episode title")
  desc = get_value(program, 'shortDesc', "No Description available.")
  season = get_value(program, 'season', "No Season available.")
  episode = get_value(program, 'episode', "No episode number available")
  print title + " : season: " + season + " episode: " + episode
  print "Description: " + desc
  print "Start Time: " + start_time
  print "End time: " + end_time
  print "Duration: " + duration + " minutes"

def get_channel_info(channel, zip_code, slot = 0):
  """
  Just simply print current channel info for given channel.
  """

  url = 'http://tvlistings.zap2it.com/api/grid?lineupId=DFLTE&timespan=2&headendId=DFLTE&country=USA&device=-&postalCode={zip}&isOverride=false&time={t}&pref=-&userId=-&aid=zap2it'.format(zip=zip_code, t=int(time.time()))
  print url

  # fetch the json info for this url and extract what we want.
  json_url = urlopen(url)
  data = json.loads(json_url.read())

  for c in data['channels']:
    # DEBUG: dump all channel names
    #print "callsign: " + c['callSign']
    if c['callSign'] == channel:
      print("Found data entry for channel " + channel)
      #print str(c)
      events = c['events']
      #for e in events:
      current_program = events[0]
      next_program = events[1]
      print "***** current program *****"
      dump_program(current_program)
      print "***** next program ********"
      dump_program(next_program)
      break

  # debug
  # uncomment the following line to see all data available
  #print data

  # extract data we want
  # It seems sometimes elements can be missing so we probably want
  # to extract them more safely
  #date = data['results']['schedules'][slot]['date']
  #time = data['results']['schedules'][slot]['time']
  #endtime = data['results']['schedules'][slot]['endTime']
  #duration = data['results']['schedules'][slot]['duration']
  #title = data['results']['schedules'][slot]['title']
  # desc can be missing so rather than read it directly we do so with a fallback
  #desc = data['results']['schedules'][0]['description']
  #desc = get_value(data, slot, 'description', 'No program description available.')

  #print "Date: " + date
  #print "Start time: " + time
  #print "End time: " + endtime
  #print "Duration: " + str(duration) + " minutes."
  #print "Program Title: " + title
  #print "Description: " + desc

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
  
  # should now work for all channels by string name
  #if not channel in channels:
  #  print("Channel {c} not supported.".format(c=channel))
  #  sys.exit(-1)

  # dump current program info
  #print("CURRENT PROGRAM:")
  get_channel_info(channel, zip, 0)
  # dump NEXT program info
  #print("NEXT PROGRAM:")
  #get_channel_info(channel, zip, 1)

  sys.exit(0)

if __name__ == "__main__":
  main()

