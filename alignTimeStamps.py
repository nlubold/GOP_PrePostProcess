import sys
import re
import tgt
from SegmentSoundTextFiles import textgrid as tg

'''
File takes in a text transcript from REV and creates a new textgrid with the utterances from the transcript

Loop through transcript line by line
Extract speaker (if there is a speaker listed)
Then check to see if there is a new time stamp in this line
If there is a new time stamp, take the current number of utterances in the last 30 seconds and map them to the time stamps 
identified in the manual turn-by-turn encoding


IMPORTANT:  Before running, make sure that in transcript, speaker 1 corresponds to 'Control' or left channel and
speaker 2 corresponds to 'Dysarthric' or right channel

'''


def newTextGrid(transcript, output, origTG):
    speakers = {1: [], 2: []}
    patternMatch = re.compile(r'\[*\]')
    patternRemove = re.compile(r'\[[a-z].*?\]')

    # Create new text grid
    newTG = tgt.TextGrid()
    tier_speaker1 = tgt.IntervalTier(name="speaker1")
    newTG.add_tier(tier_speaker1)
    tier_speaker2 = tgt.IntervalTier(name="speaker2")
    newTG.add_tier(tier_speaker2)

    grid = tg.TextGrid.load(origTG)

    speech = {1: [], 2: []}

    for i, tier in enumerate(grid):
        x = str(tier).split('\n')
        for y in x:
            z = y.split()
            for w in z:
                if w == 'S':
                    speakingturn = [float(z[0]), float(z[1])]
                    speech[i+1].append(speakingturn)

    with open(transcript, 'r') as f:
        speaker = 1
        currentXmin = 0.0
        thisset = []

        for line in f:
            #print line
            line = re.sub(patternRemove, "", line)
            if len(line.split(":")) > 1 and "speaker " in line:
                speaker = int( (line.split(":")[0]).split()[1])
                text = (line.split(":", 1)[1]).lstrip()
            elif line == "" or line == "\n":
                continue
            else:
                text = line.lstrip()
            if patternMatch.findall(line):
                    print(line)
                    print(currentXmin)
                    speakers[speaker].append(text)

                    for key, value in speakers.iteritems():
                        if len(value) > 0:

                            # get the corresponding speaking times for the speaker from original textgrid
                            numturns = 0
                            for i in range(0, len(speech[key])):
                                if currentXmin + 30.0 > grid.xmax:
                                    currentXmax = grid.xmax
                                else: currentXmax = currentXmin + 30.0

                                if (speech[key][i][0] > currentXmin) and (speech[key][i][0] <  currentXmax ):
                                    thisset.append(speech[key][i])
                                    numturns += 1

                            # loop through transcripts and using values of speaking turns from original textgrid
                            # create new annotations
                            for i in range(0, len(value)):
                                if thisset == []:
                                        xmin = currentXmin + (.1*(i - numturns) + .01)
                                        xmax = currentXmin + (.1*(i - numturns) + .02)
                                        print("hit empty set: ", currentXmin)
                                elif i >= numturns:
                                        xmin = thisset[numturns-1][1] + (.1*(i - numturns) + .01)
                                        xmax = thisset[numturns-1][1] + (.1*(i - numturns) + .02)
                                else:
                                    xmin = thisset[i][0]
                                    xmax = thisset[i][1]

                                # print "speaker: ", key, "i: ", i, " xmin: ", xmin, " xmax: ", xmax

                                anno = tgt.Interval(xmin, xmax, value[i])
                                if key == 1: tier_speaker1.add_annotation(anno)
                                else: tier_speaker2.add_annotation(anno)

                        speakers[key] = []
                        del thisset[:]

                    currentXmin = currentXmin + 30

            else:
                speakers[speaker].append(text)


    tgt.write_to_file(newTG, output)



# usage: python wavtest.py filename.wav
def main():
    if len(sys.argv) != 4:
        print('usage: ./readfile2.py transcript nameNewTG originalTG')
        sys.exit(1)

    transcript = sys.argv[1]
    nameOutput = sys.argv[2]
    originalTG = sys.argv[3]

    newTextGrid(transcript, nameOutput, originalTG)



if __name__ == '__main__': main()