import sys
import string
import os
import itertools
import re


'''Given a text doc, parse transcript.
    Name after wav files in directory; should correspond. If more files in directory than lines in file, exit.
'''




def parseTranscript(transcript, wavdir, speaker):

    turns = []

    outputdir = wavdir

    spaces = ""
    for x in string.punctuation:
        spaces = spaces + " "

    trantable = string.maketrans(string.punctuation, spaces)
    firstime = True


    patternRemove = re.compile(r'\[[a-z].*?\]')

    with open(transcript, 'r') as f:

        for line in f:
            if firstime and ":" in line:
                line = line.split(":", 1)[1]
                firstime = False

            line = line.strip()
            line = re.sub(patternRemove, "", line)

            if line == "" or line == "\n" or "[beep]" in line:
                continue
            elif "[End of Audio]" in line or "END OF AUDIO" in line:
                continue
            else:
                line = line.translate(trantable)
                line = " ".join(line.split())
                turns.append(line)

    f.close()

    filenames = []

    for file in sorted(os.listdir(wavdir)):
        if file.endswith(".wav"):
            filenames.append(file)

    index = 0
    if len(filenames) != len(turns):
        print("Issue with mismatch between files and turns for ", transcript, ": ", str(len(filenames)), ", ", str(len(turns)))
    else:
        for f in filenames:
            name = f.split(".wav")[0]
            print("Name of file is " + str(name))



            outfile = outputdir + '\\' + name + ".lab"
            out = open(outfile, 'w')
            out.write(turns[index])
            out.close()

            index += 1


def processFiles(dirTrans, dirWavDir, listSpeakers):

    with open(dirTrans,'r') as transcripts, \
     open(dirWavDir,'r') as wavDirs, \
     open(listSpeakers,'r') as speakers:

        transcriptLines = transcripts.readlines()
        wavfileLines = wavDirs.readlines()
        speakerLines = speakers.readlines()

        for i in range(len(transcriptLines)):
            parseTranscript(transcriptLines[i].strip("\n"), wavfileLines[i].strip("\n"), speakerLines[i].strip("\n"))

    transcripts.close()
    wavDirs.close()
    speakers.close()

# usage: python wavtest.py filename.wav
def main():
    if len(sys.argv) != 4:
        print('usage: ./readfile2.py fileOfAllTranscriptDirectories fileOfAllWavFileDirectories fileOfSpeakers')
        sys.exit(1)

    dirTranscript = sys.argv[1]
    dirWavdir = sys.argv[2]
    listSpeakers = sys.argv[3]
    #outputdir = sys.argv[3]

    processFiles(dirTranscript, dirWavdir, listSpeakers)

    #parseTranscript(transcript, wavdir, speaker)



if __name__ == '__main__': main()