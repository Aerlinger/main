import sys, os
from aubio import source, freqtomidi, pvoc, mfcc
from aubio import pitch as aubio_pitch
from aubio import onset as aubio_onset
from aubio import level_detection as aubio_level_detection
import numpy as np


class AubioWrapper:
  def __init__(self, audioFilename, baseFolder=os.path.join(os.path.dirname(__file__), "../data/")):
    self.baseFolder = baseFolder
    self.audioFilename = audioFilename

    self.fftWindowSize = 512  # fft size
    self.hopSize = 256  # hop size
    self.samplerate = 44100

  def audioPath(self):
    return os.path.join(self.baseFolder, self.audioFilename)

  def mfcc(self, **options):
    nFilters = options.get("nFilters") or 40  # must be 40 for mfcc
    nCoeffs = options.get("nCoefs") or 13

    sourceBuffer = source(self.audioPath(), self.samplerate, self.hopSize)

    pvocBuffer = pvoc(self.fftWindowSize, self.hopSize)
    mfccBuffer = mfcc(self.fftWindowSize, nFilters, nCoeffs, self.samplerate)

    mfccs = np.zeros([nCoeffs, ])

    timings = []
    frames = []

    totalFrames = 0
    while True:
      samples, read = sourceBuffer()
      spec = pvocBuffer(samples)
      mfcc_out = mfccBuffer(spec)
      mfccs = np.vstack((mfccs, mfcc_out))

      totalFrames += read
      timings += [float(totalFrames) / self.samplerate]
      frames += [totalFrames]

      if read < self.hopSize: break

    return {
      "mfccs": mfccs,
      "timings": timings,
      "frames": frames
    }

  def onset(self, **options):
    onsetAlgorithm = options.get("onsetAlgorithm") or "default"
    onsetThreshold = options.get("onsetThreshold") or -90

    sourceBuffer = source(self.audioPath(), self.samplerate, self.hopSize)

    onsetSampler = aubio_onset(onsetAlgorithm, self.fftWindowSize, self.hopSize, self.samplerate)
    # onsetSampler = aubio_level_detection(-70)

    # list of onsets, in samples
    onsets = []
    timings = []
    frames = []

    # total number of frames read
    totalFrames = 0
    while True:
      samples, read = sourceBuffer()

      if onsetSampler(samples):
        print "%f" % onsetSampler.get_last_s()
        onsets.append(onsetSampler.get_last())

      timings += [float(totalFrames) / self.samplerate]
      frames += [totalFrames]
      totalFrames += read

      if read < self.hopSize: break

    return {
      "timings": timings,
      "frames": frames,
      "onsets": onsets
    }

  def printNoteOn(self, pitch, frames):
    print "ON: " + str(pitch) + " " + str(frames / 44100.0)

  def printNoteOff(self, frames):
    print "OFF: " + str(frames / 44100.0)

  def pseudo_median(self, arr):
    arrLen = len(arr)

    return np.sort(arr)[(arrLen - 1) / 2]

  def notes(self, **options):
    onsetAlgorithm = options.get("onsetAlgorithm") or "default"
    algorithm = options.get("algorithm") or "yinfft"
    pitchUnit = options.get("pitchUnit") or "freq"
    tolerance = options.get("tolerance") or 0.85

    sourceBuffer = source(self.audioPath(), self.samplerate, self.hopSize)

    onsetSampler = aubio_onset(onsetAlgorithm, self.fftWindowSize, self.hopSize, self.samplerate)
    pitchSampler = aubio_pitch(algorithm, self.fftWindowSize * 4, self.hopSize, self.samplerate)
    pitchSampler.set_unit(pitchUnit)
    pitchSampler.set_tolerance(tolerance)

    median = 6
    isReady = 0

    note_buffer = []

    timeStarts = []
    timeStops = []
    frameStarts = []
    frameStops = []
    pitches = []
    confidences = []

    isOn = False

    totalFrames = 0
    while True:
      samples, read = sourceBuffer()

      new_pitch = pitchSampler(samples)[0]
      curlevel = aubio_level_detection(samples, -90)

      note_buffer.insert(0, new_pitch)

      if len(note_buffer) > median:
        note_buffer.pop()

      if onsetSampler(samples):
        if curlevel == 1.:
          isReady = 0
        else:
          isReady = 1

      else:
        if isReady > 0:
          isReady += 1
        if isReady == median:
          new_note = self.pseudo_median(note_buffer)

          if isOn:
            timeStops += [float(totalFrames) / self.samplerate]
            frameStops += [totalFrames]
            isOn = False

          if new_note > 45:
            confidence = pitchSampler.get_confidence()

            timeStarts += [float(totalFrames) / self.samplerate]
            frameStarts += [totalFrames]
            pitches += [new_note]
            confidences += [confidence]

            isOn = True

      totalFrames += read
      if read < self.hopSize: break

    frameStops += [totalFrames]
    timeStops += [timeStops]

    return {
      "timeStarts": timeStarts,
      "timeStops": timeStops,
      "frameStarts": frameStarts,
      "frameStops": frameStops,
      "pitches": pitches,
      "confidences": confidences
    }


  def pitch(self, **options):
    algorithm = options.get("algorithm") or "yin"
    pitchUnit = options.get("pitchUnit") or "freq"
    tolerance = options.get("tolerance") or 0.85

    sourceBuffer = source(self.audioPath(), self.samplerate, self.hopSize)
    samplerate = sourceBuffer.samplerate

    pitchSampler = aubio_pitch(algorithm, self.fftWindowSize, self.hopSize, self.samplerate)

    pitchSampler.set_unit(pitchUnit)
    pitchSampler.set_tolerance(tolerance)

    timings = []
    frames = []
    pitches = []
    confidences = []

    # total number of frames read
    totalFrames = 0
    while True:
      samples, read = sourceBuffer()
      pitchSample = pitchSampler(samples)[0]
      confidence = pitchSampler.get_confidence()

      print pitchSample

      timings += [float(totalFrames) / samplerate]
      frames += [totalFrames]
      pitches += [pitchSample]
      confidences += [confidence]

      totalFrames += read
      if read < self.hopSize: break

    return {
      "timings": timings,
      "frames": frames,
      "pitches": pitches,
      "confidences": confidences
    }
