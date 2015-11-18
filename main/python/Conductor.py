import glob

from SonicApi import SonicApi
from AubioWrapper import AubioWrapper
from Writer import Writer

from aubio import source, pitch, freqtomidi

class Conductor:
  def __init__(self):
    pass

  def extractMetadata(self, beatDict, melodyDict):
    meta = dict()

    meta["clicks_per_bar"] = beatDict["clicks_per_bar"]
    meta["overall_tempo"] = beatDict["overall_tempo"]
    meta["overall_tempo_straight"] = beatDict["overall_tempo_straight"]

    meta["key"] = melodyDict["key"]
    meta["key_index"] = melodyDict["key_index"]
    meta["tuning_frequency"] = melodyDict["tuning_frequency"]

    return meta

  def analyze(self, audioFilename):
    sonic = SonicApi(audioFilename)
    writer = Writer(audioFilename)

    # Analyze Melody SonicApi
    melody = sonic.analyzeMelody()

    # Analyze Beat SonicApi
    beat = sonic.analyzeBeat()

    # Extract metadata (BPM, key, etc.)
    meta = self.extractMetadata(beat, melody)

    # AnalyzeNotes Aubio
    # AnalyzePitch Aubio
    # AnalyzeOnset Aubio
    # AnalyzeTSS Aubio
    # AnalyzeTSS Aubio

    # write output:
    writer.writeTable(beat['click_marks'], 'beat')
    writer.writeTable(melody['melody_result'], 'melody')
    writer.writeTable(meta, 'meta')




for filename in glob.glob("data/process/*.mp3"):
  conductor = Conductor(filename)

  conductor.analyze(filename)

