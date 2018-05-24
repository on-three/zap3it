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

  # this is what we want, probably
  https://tvlistings.zap2it.com/api/grid?lineupId=DFLTE&timespan=2&headendId=DFLTE&country=USA&device=-&postalCode=10001&isOverride=false&time=1527109200&pref=-&userId=-&aid=zap2it


# good info
  https://www.scribd.com/doc/133056264/TV-Listings-Guide-and-TV-Schedule-Where-to-Watch-TV-Shows-Zap2i://www.scribd.com/doc/133056264/TV-Listings-Guide-and-TV-Schedule-Where-to-Watch-TV-Shows-Zap2it

  # was able to get the next json block by adding a "schd" param (no does not work)
  http://api.zap2it.com/tvlistings/webservices/whatson?stnlt=12131&zip=10012&schd=32503139599

  Research:
  url: http://api.zap2it.com/tvlistings/zcConnector.jsp?ap=wo&md=getWhatsOn&v=2&aid=WBAL&zip=21211&stnlt=21231&random=1349602906090
  results in response:
  var validRequest = true; var server = "http://api.zap2it.com"; var requestParams = "ap=wo&md=getWhatsOn&v=2&aid=WBAL&zip=21211&stnlt=21231&random=1349602906090"; var action; action = "/tvlistings/ZCShowtimeAction.do?"; if(requestParams!="" && validRequest) { document.write(""); document.write(""); } else { function buildXHTML() {} }

# this url also works (uses 'aid' whatever that is)
http://api.zap2it.com/tvlistings/webservices/whatson?stnlt=70248&aid=antennatv

# these urls also have some possibly usable settings
https://tvlistings.zap2it.com/?fromTimeInMillis=1526922000000&aid=zap2it
http://api-origin.zap2it.com/tvlistings/ZCGrid.do?method=decideFwdForLineup&zipcode=85016&setMyPreference=false&lineupId=DITV:-
http://api-origin.zap2it.com/tvlistings/ZBChooseProvider.do?method=getProviders
http://api-origin.zap2it.com/tvlistings/zcgrid.do?setmypreference=false&zipcode=78746&method=decidefwdforlineup&lineupid=dish635%3A

# Got this url when looking ahead at approx unix time (seconds from epoch) : 1526919453
http://api.zap2it.com/tvlistings/ZCGrid.do?fromTimeInMillis=1513969200000

# this works. Got schedule info from the future
http://api.zap2it.com/tvlistings/webservices/whatson?fromTimeInMillis=1527005834848&stnlt=10149

# this looks like a complete dump of their supported URL parameters
http://api.zap2it.com/tvlistings/zcConnector.jsp?ap=cf&v=1
var validRequest = true; var server = "http://api.zap2it.com"; var requestParams = "ap=cf&v=1"; var action; var qsParm = new Array(); var query = window.location.search.substring(1); //alert("in query =================== "+query); var parms = query.split("&"); for (var i=0; i 0) { var key = parms[i].substring(0,pos); var val = parms[i].substring(pos+1); qsParm[key] = val; //alert(key+" ======= "+ qsParm[key]); } } var aid = qsParm["aid"]; var version = qsParm["v"]; var zipcode = qsParm["zip"]; var lineupId = qsParm["lid"]; var stnlt = qsParm["stnlt"]; var nstnlt = qsParm["nstnlt"]; var rType = qsParm["rty"]; var fType = qsParm["fmt"]; //alert(" version from query ======= "+ version+" zip = "+zipcode+" aid = "+aid + " stn list = "+stnlt); if(version != undefined && version != null && version!="" && version!="null") { version = "&v="+version; } else { version = ""; } //alert("zcConnector version =================== " + version); //alert("zcConnector aid =================== "+aid); if(aid != undefined && aid != null && aid!="" && aid!="undefined" && aid!="null") { aid = "&aid="+aid; //alert("zcConnector aid =================== "+aid); } else { //alert("zcConnector else NO aid !!!!!!!!"); aid = ""; } if(zipcode!= undefined && zipcode!=null && zipcode!="" && zipcode!="undefined" && zipcode!="null") { zipcode = "&zip="+zipcode; //alert("zcConnector zip =================== " + zipcode ); } else { //alert("zcConnector NO ZIP !!!!!!!!!!!!!!! " ); zipcode =""; } if(lineupId!= undefined && lineupId!=null && lineupId!="" && lineupId!="undefined" && lineupId!="null") { lineupId = "&lid="+lineupId; //alert("zcConnector zip =================== " + lineupId ); } else { //alert("zcConnector NO LineupIDs !!!!!!!!!!!!!!! " ); lineupId = ""; //alert("zcConnector else lineupId =================== " + lineupId ); } if(stnlt != undefined && stnlt != null && stnlt!="" && stnlt!="undefined" && stnlt!="null") { stnlt = "&stnlt="+stnlt; } else { stnlt = ""; } if(nstnlt != undefined && nstnlt != null && nstnlt!="" && nstnlt!="undefined" && nstnlt!="null") { nstnlt = "&nstnlt="+nstnlt; } else { nstnlt = ""; } if(rType != undefined && rType != null && rType!="" && rType!="undefined" && rType!="null") { rType = "&rty="+rType; } else { rType = ""; } if(fType != undefined && fType != null && fType!="" && fType!="undefined" && fType!="null") { fType = "&fmt="+fType; } else { fType = ""; } requestParams = version + aid + zipcode + lineupId + stnlt + nstnlt + rType + fType; if(zipcode=="" || stnlt=="") { validRequest = false; } action = "/tvlistings/ZCChannelFinder.do?"; if(requestParams!="" && validRequest) { document.write(""); document.write(""); } else { function buildXHTML() {} }

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
  global channels

  id = channels[channel]
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

