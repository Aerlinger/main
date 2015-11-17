import requests
import time
import os
import json
import glob

from csvkit.convert import *
from StringIO import StringIO

accessId = '01ff3792-3f80-4ed6-ac51-2add16e0db68'
baseUrl = 'https://api.sonicAPI.com/'

class ProcessAubio:

def requestParams(audioFilename):
  return {
    'access_id': accessId,
    'format': 'json',
    'input_file': audioFilename
  }


def createTimestampedFolder(audioFilename, timestamp):
  pathname = "data/" + timestamp + "/" + audioFilename + "/"
  os.makedirs(pathname)

  return pathname


def analyzeChords(audioFilename, destinationPath):
  print "Analyzing chords: " + audioFilename

  response = requests.post(baseUrl + 'analyze/chords',
                           data=requestParams(audioFilename),
                           files={'input_file': open(audioFilename, 'rb')})

  if response.status_code == 200:
    chordsBody = response.json()['chords_result']['chords']

    chordStrings = StringIO(json.dumps(chordsBody))
    rawCsv = json2csv(chordStrings)

    with open(destinationPath + "/chords.csv", "w") as f:
      f.write(rawCsv)

    with open(destinationPath + "/chords.json", "w") as f:
      f.write(json.dumps(response.json()['chords_result']))

    return response.json()['chords_result']
  else:
    print "Analyze chords request failed: " + response.text


def analyzeMelody(audioFilename, destinationPath, detailed=False):
  print "Analyzing melody " + audioFilename + " " + str(detailed)

  params = requestParams(audioFilename)
  params["detailed_result"] = "true" if detailed else "false"

  response = requests.post(baseUrl + 'analyze/melody',
                           data=params,
                           files={'input_file': open(audioFilename, 'rb')})

  suffix = "_detailed" if detailed else ""

  if response.status_code == 200:
    melodyBody = response.json()['melody_result']['notes']

    rawCsv = json2csv(StringIO(json.dumps(melodyBody)))

    with open(destinationPath + "/melody" + suffix + ".csv", "w") as f:
      f.write(rawCsv)

    with open(destinationPath + "/melody" + suffix + ".json", "w") as f:
      f.write(json.dumps(response.json()['melody_result']))

    return response.json()['melody_result']
  else:
    print "Analyze melody request failed: " + response.text


def analyzeBeat(audioFilename, destinationPath):
  print "Analyzing beat: " + audioFilename

  response = requests.post(baseUrl + 'analyze/tempo',
                           data=requestParams(audioFilename),
                           files={'input_file': open(audioFilename, 'rb')})

  if response.status_code == 200:
    responseBody = response.json()['auftakt_result']['click_marks']

    clickMarks = StringIO(json.dumps(responseBody))
    rawCsv = json2csv(clickMarks)

    with open(destinationPath + "/beat.csv", "w") as f:
      f.write(rawCsv)

    with open(destinationPath + "/beat.json", "w") as f:
      f.write(json.dumps(response.json()['auftakt_result']))

    return response.json()['auftakt_result']




def processFile(filename, destinationPath):
  chordsJson = analyzeChords(filename, destinationPath)
  melodyJson = analyzeMelody(filename, destinationPath)
  detailedMelodyJson = analyzeMelody(filename, destinationPath, True)
  beatJson = analyzeBeat(filename, destinationPath)

  meta = dict()

  meta["clicks_per_bar"] = beatJson["clicks_per_bar"]
  meta["overall_tempo"] = beatJson["overall_tempo"]
  meta["overall_tempo_straight"] = beatJson["overall_tempo_straight"]

  meta["key"] = melodyJson["key"]
  meta["key_index"] = melodyJson["key_index"]
  meta["tuning_frequency"] = melodyJson["tuning_frequency"]

  with open(destinationPath + "/meta.json", "w") as f:
        f.write(json.dumps(meta, indent=2))


timestamp = str(int(time.time()))

print("Creating destination path " + timestamp)

for filename in glob.glob("data/process/*.mp3"):
  processFile(filename, createTimestampedFolder(filename, timestamp))

