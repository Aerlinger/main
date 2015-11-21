import requests
import os

class SonicApi:
  accessId = '01ff3792-3f80-4ed6-ac51-2add16e0db68'
  baseUrl = 'https://api.sonicAPI.com/'

  def __init__(self, audioFilename,
               accessId='01ff3792-3f80-4ed6-ac51-2add16e0db68',
               baseFolder = os.path.join(os.path.dirname(__file__), "../data/"),
               baseUrl='https://api.sonicAPI.com/'):
    self.audioFilename = audioFilename
    self.accessId = accessId
    self.baseUrl = baseUrl
    self.baseFolder = baseFolder

  def requestParams(self):
    return {
      'access_id': SonicApi.accessId,
      'format': 'json',
      'input_file': self.audioFilename
    }

  # def audioPath(self):
  #   return os.path.join(self.baseFolder, self.audioFilename)

  def analyzeChords(self):
    print "Analyzing chords: " + self.audioFilename

    response = requests.post(SonicApi.baseUrl + 'analyze/chords',
                             data=self.requestParams(),
                             files={'input_file': open(self.audioFilename, 'rb')})

    if response.status_code == 200:
      return response.json()['chords_result']
    else:
      print "Analyze chords SonicAPI request failed: " + response.text


  def analyzeMelody(self, detailed=False):
    print "Analyzing melody " + self.audioFilename + " " + str(detailed)

    params = self.requestParams()
    params["detailed_result"] = "true" if detailed else "false"

    response = requests.post(SonicApi.baseUrl + 'analyze/melody',
                             data=params,
                             files={'input_file': open(self.audioFilename, 'rb')})

    if response.status_code == 200:
      return response.json()['melody_result']
    else:
      print "Analyze melody SonicAPI request failed: " + response.text


  def analyzeBeat(self):
    print "Analyzing beat: " + self.audioFilename

    response = requests.post(SonicApi.baseUrl + 'analyze/tempo',
                             data=self.requestParams(),
                             files={'input_file': open(self.audioFilename, 'rb')})

    if response.status_code == 200:
      return response.json()['auftakt_result']
    else:
      print "Analyze beat SonicAPI request failed: " + response.text
