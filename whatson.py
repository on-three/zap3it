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

# this url gives a json response for specific local provider (so you have local stations like fox etc."
https://tvlistings.zap2it.com/api/grid?lineupId=USA-NV27420-DEFAULT&timespan=2&headendId=NV27420&country=USA&device=-&postalCode=89135&isOverride=true&time=1527550200&pref=-&userId=-&aid=gapzap

"""

DEFAULT_ZIP = 89135
DEFAULT_PROVIDER = 'NV27420'

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

def get_channel_info(channel, zip_code, provider):
  """
  Just simply print current channel info for given channel.
  """

  url = 'https://tvlistings.zap2it.com/api/grid?lineupId=USA-{p}-DEFAULT&timespan=2&headendId={p}&country=USA&device=-&postalCode={z}&isOverride=true&time={t}&pref=-&userId=-&aid=gapzap'.format(p=provider, z=zip_code, t=int(time.time()))

  #url = 'http://tvlistings.zap2it.com/api/grid?lineupId=DFLTE&timespan=2&headendId=DFLTE&country=USA&device=-&postalCode={zip}&isOverride=false&time={t}&pref=-&userId=-&aid=zap2it'.format(zip=zip_code, t=int(time.time()))
  print url

  # fetch the json info for this url and extract what we want.
  json_url = urlopen(url)
  data = json.loads(json_url.read())

  if channel == "LIST":
    for c in data['channels']:
      print c['callSign'] + ','
    return True
  
  for c in data['channels']:
    if c['callSign'] == channel:
      print("Found data entry for channel " + channel)
      # DEBUG
      #print str(c)
      events = c['events']
      if len(events) == 0:
        return False
      current_program = events[0]
      print "***** current program *****"
      dump_program(current_program)
      if len(events) < 2:
        return False
      next_program = events[1]
      print "***** next program ********"
      dump_program(next_program)
      # We can bail as we've found our channel of interest
      return True

  return False

def main():

  global DEFAULT_ZIP
  global DEFAULT_PROVIDER

  parser = argparse.ArgumentParser(
    description='Fetch current program info')
  parser.add_argument('channel', help='Station name (e.g. TBS) case insensitive, or LIST to list available channels', type=str)
  parser.add_argument('-z','--zip', help='Zip code of query', type=int, default=DEFAULT_ZIP)
  parser.add_argument('-p', '--provider', help='provider id', type=str, default=DEFAULT_PROVIDER)
  args = parser.parse_args()
  
  # force all uppercase for channel names
  channel = args.channel.upper()
  provider = args.provider.upper()
  zip = args.zip
 
  if not get_channel_info(channel, zip, provider):
    print("ERROR:  no channel data found for channel : " + channel)
    sys.exit(-1)

  sys.exit(0)

if __name__ == "__main__":
  main()

