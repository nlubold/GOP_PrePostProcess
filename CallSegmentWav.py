__author__ = 'Nikki'

from SegmentSoundTextFiles import segmentWav
import sys

# given a directory, builds argument list to call segment wav; segment wav needs individuals file names so can loop through list
#
# NOTE:  skip list needs to be manually edited as does waveFileNaming (1,2 or control, D)
#
# directory should be something like: E:\Nikki\Dropbox\misc\Research\Post-doc\Data\Healthy_New\
# takes as input directory, the number of items to create arguments for and the prepend associated with that directory (i.e. HS_D)
# Creates arguments within that directory for each individual wave file under "Splitfiles", TextGrids and then output directory

def buildArgList(dirname, num, prepend):
    skipList = [4, 16]
    waveFileNaming = ["Control", "D"]
    argList = {}

    for i in range(1,int(num)+1):
        if i in skipList:
            continue
        else:
            if i < 10:
                speaker1 = dirname + "SoundFiles\\Splitfiles\\" + prepend + "0" + str(i) + "_" + waveFileNaming[0] + ".wav"
                speaker2 = dirname + "SoundFiles\\Splitfiles\\" + prepend + "0" + str(i) + "_" + waveFileNaming[1] + ".wav"
                textgrid = dirname + "TextGrids\\" + prepend + "0" + str(i) + ".TextGrid"
                outputdir = dirname + "SoundFiles\\ChunkedFiles\\" + prepend + "0" + str(i) + "\\"
            else:
                speaker1 = dirname + "SoundFiles\\Splitfiles\\" + prepend + str(i) + "_" + waveFileNaming[0] + ".wav"
                speaker2 = dirname + "SoundFiles\\Splitfiles\\" + prepend + str(i) + "_" + waveFileNaming[1] + ".wav"
                textgrid = dirname + "TextGrids\\" + prepend + str(i) + ".TextGrid"
                outputdir = dirname + "SoundFiles\\ChunkedFiles\\" + prepend + str(i) + "\\"

            argList[i] = [speaker1, speaker2, textgrid, outputdir]

    return argList

# usage: python wavtest.py filename.wav
def main():
    if len(sys.argv) != 4:
        print('usage: ./readfile2.py dirname numfiles prepend')
        sys.exit(1)

    dirname = sys.argv[1]
    num = sys.argv[2]
    prepend = sys.argv[3]

    argList = buildArgList(dirname, num, prepend)

    for key, value in argList.iteritems():
        waves = [value[0], value[1]]
        segmentWav.segment(waves, value[2], value[3])
        print("Just did file: ", str(key))


if __name__ == '__main__': main()