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
  # DEBUG
  #print str(e)
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
      # DEBUG
      #print str(c)
      events = c['events']
      current_program = events[0]
      next_program = events[1]
      print "***** current program *****"
      dump_program(current_program)
      print "***** next program ********"
      dump_program(next_program)
      # We can bail as we've found our channel of interest
      return True

  print("ERROR: no channel by name: " + channel + " found in data.")
  return False

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

  get_channel_info(channel, zip, 0)

  sys.exit(0)

if __name__ == "__main__":
  main()

