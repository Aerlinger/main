import glob
import os

from python.AubioWrapper import AubioWrapper
from python.Writer import Writer
from python.SonicApi import SonicApi

writer = Writer()

for path in glob.glob("data/*.mp3"):
  if os.path.isfile(path):
    print "processing " + path

    filename = os.path.splitext(os.path.split(path)[1])[0]

    aubio = AubioWrapper(path)
    sonicApi = SonicApi(path)

    os.mkdir(writer.destinationFolder + "/" + filename)

    # Aubio processing functions
    print "Processing notes"
    writer.writeTable(aubio.notes(), filename + "/notes")

    print "Processing pitch"
    writer.writeTable(aubio.pitch(), filename + "/pitch")

    print "Processing onsets"
    writer.writeTable(aubio.onset(), filename + "/onset")

    print "Processing MFCCs"
    writer.writeTable(aubio.mfcc(), filename + "/mfcc")


    # SonicAPI
    print "Processing melody"

    sonicMelody = sonicApi.analyzeMelody(True)
    writer.writeTable(sonicMelody["notes"], filename + "_sonic_notes")
    writer.writeTable(sonicMelody["pitch_curve"], filename + "/sonic_pitch_curve")

    print "Processing beat"

    sonicBeat = sonicApi.analyzeBeat()
    writer.writeTable(sonicBeat["click_marks"], filename + "/sonic_beat")

    print "writing meta..."
    meta = dict()

    meta["clicks_per_bar"] = [sonicBeat["clicks_per_bar"]]
    meta["overall_tempo"] = [sonicBeat["overall_tempo"]]
    meta["overall_tempo_straight"] = [sonicBeat["overall_tempo_straight"]]

    meta["key"] = [sonicMelody["key"]]
    meta["key_index"] = [sonicMelody["key_index"]]
    meta["tuning_frequency"] = [sonicMelody["tuning_frequency"]]

    writer.writeTable(meta, filename + "/sonic_beat")
