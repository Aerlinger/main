import json
import os
import time

import pandas as pd

class Writer:
  def __init__(self,
               destinationPath = os.path.join(os.path.dirname(__file__), "../data/")):
    self.destinationPath = destinationPath
    self.timestamp = Writer.timestamp()
    self.destinationFolder = destinationPath + self.timestamp

    os.makedirs(self.destinationFolder)

  @staticmethod
  def timestamp():
    return str(int(time.time()))

  def writeTable(self, jsonData, filename):
    df = pd.DataFrame(jsonData)

    df.to_csv(self.destinationFolder + "/" + filename + ".csv")
