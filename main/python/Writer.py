import json
import os
import time
from csvkit.convert import *

class Writer:
  def __init__(self,
               audioFilename,
               destinationPath = os.path.join(os.path.dirname(__file__), "../data/")):
    self.destinationPath = destinationPath
    self.timestamp = Writer.timestamp()
    self.destinationFolder = destinationPath + self.timestamp + "/" + audioFilename + "/"

    os.makedirs(self.destinationFolder)

  @staticmethod
  def timestamp():
    return str(int(time.time()))

  def writeTable(self, jsonData, filename):
    with open(self.destinationFolder + "/" + filename + ".csv", "w") as f:
      f.write(json2csv(jsonData))

    with open(self.destinationPath + "/" + filename + ".json", "w") as f:
      f.write(json.dumps(jsonData))
