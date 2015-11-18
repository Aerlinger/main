import sys, os
from aubio import source, freqtomidi
from aubio import pitch as aubio_pitch
from aubio import onset as aubio_onset
from aubio import level_detection as aubio_level_detection
import numpy as np
import math

class AubioWrapper:
  def __init__(self, audioFilename, baseFolder = os.path.join(os.path.dirname(__file__), "../data/")):
    self.baseFolder = baseFolder
    self.audioFilename = audioFilename

    self.fftWindowSize = 512                 # fft size
    self.hopSize = 256           # hop size
    self.samplerate = 44100

  def audioPath(self):
    return os.path.join(self.baseFolder, self.audioFilename)

  def mfcc(self):
    nFilters = 40              # must be 40 for mfcc
    nCoeffs = 13

    s = source(self.audioPath(), self.samplerate, self.hopSize)

    samplerate = s.samplerate

    p = pvoc(self.fftWindowSize, self.hopSize)
    m = mfcc(self.fftWindowSize, nFilters, nCoeffs, samplerate)

    mfccs = zeros([nCoeffs,])
    frames_read = 0

    while True:
        samples, read = s()
        spec = p(samples)
        mfcc_out = m(spec)
        mfccs = vstack((mfccs, mfcc_out))
        frames_read += read
        if read < hop_s: break

    return { "mfccs": mfccs }


  def onset(self):
    sourceBuffer = source(self.audioPath(), self.samplerate, self.hopSize)

    onsetSampler = aubio_onset("default", self.fftWindowSize, self.hopSize, self.samplerate)
    # onsetSampler = aubio_level_detection(-70)

    # list of onsets, in samples
    onsets = []

    # total number of frames read
    totalFrames = 0
    while True:
      samples, read = sourceBuffer()

      if onsetSampler(samples):
        print "%f" % onsetSampler.get_last_s()
        onsets.append(onsetSampler.get_last())

      totalFrames += read

      if read < self.hopSize: break

    return { "onsets": onsets }

  def printNoteOn(self, pitch, frames):
    print "ON: " + str(pitch) + " " + str(frames / 44100.0)

  def printNoteOff(self, frames):
    print "OFF: " + str(frames / 44100.0)

  def pseudo_median(self, arr):
    arrLen = len(arr)

    return np.sort(arr)[(arrLen-1)/2]

  def notes(self):
    sourceBuffer = source(self.audioPath(), self.samplerate, self.hopSize)

    print self.fftWindowSize, self.hopSize

    onsetSampler = aubio_onset("default", self.fftWindowSize, self.hopSize, self.samplerate)
    pitchSampler = aubio_pitch("yinfft", self.fftWindowSize * 4, self.hopSize, self.samplerate)
    # pitchSampler.set_unit("midi")
    pitchSampler.set_tolerance(1.0)

    median = 6
    isReady = 0

    note_buffer = []

    note_output = []
    start_time = []
    start_time = []

    # total number of frames read
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


          # self.printNoteOff(totalFrames)

        else:
          isReady = 1

      else:
        if isReady > 0:
          isReady += 1
        if isReady == median:
          # New Note

          # Send noteoff
          self.printNoteOff(totalFrames)

          new_note = self.pseudo_median(note_buffer)
          curNote = new_note

          # print curNote
          # print note_buffer
          if curNote > 45:
            self.printNoteOn(round(freqtomidi(curNote)), totalFrames)

      totalFrames += read
      if read < self.hopSize: break


  def pitch(self, baseSampleRate=44100):
    tolerance = 0.8

    sourceBuffer = source(self.audioPath(), self.samplerate, self.hopSize)
    samplerate = sourceBuffer.samplerate

    pitchSampler = aubio_pitch("yin", self.fftWindowSize, self.hopSize, self.samplerate)

    pitchSampler.set_unit("midi")
    pitchSampler.set_tolerance(tolerance)

    pitches = []
    confidences = []

    # total number of frames read
    totalFrames = 0
    while True:
      samples, read = sourceBuffer()
      pitchSample = pitchSampler(samples)[0]
      #pitch = int(round(pitch))
      confidence = pitchSampler.get_confidence()
      #if confidence < 0.8: pitch = 0.
      #print "%f %f %f" % (total_frames / float(samplerate), pitch, confidence)
      pitches += [pitchSample]
      confidences += [confidence]
      totalFrames += read

      if read < self.hopSize: break

    return { "pitches": pitches, "confidences": confidences }
