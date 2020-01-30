#1/usr/bin/env python
import wave
from SegmentSoundTextFiles import textgrid as tg
import decimal

# Takes in a text grid and a wave file and cuts it up based on the text grid (assuming speaking labeled as "S")
# Also looks at whether wave file has one or two channels; if two, it will write out two separate wav files for the two speakers
# Meant to be applied to a textgrid where only 'speaking' or nonspeaking has been identified

# commented out: lines to print filenames to a file

def segment(wavfile, textgridfile, outdir):
    #filepath = "C:\\Nikki\\ASU_Research\\FACT\\Data\\Edits\\Segmentation\\"

    timestampsFiles = "D:\ASU\Experimenter\\filenameTiming.csv"
    filenames = open(timestampsFiles, "a")

    speakers = {1: [], 2: []}

    grid = tg.read_textgrid(textgridfile)                                                   # read in pauses

    #intervals = []
    currentspeaker = ""
    i = 1
    for line in enumerate(grid):
        # x = str(line).split('\n')
        # for z in x:
        if len(line) < 2:
            print ("ISSUE with textgrid encoding: len(z) < 2: ", z)
            continue
        else:
            z = line[1]
            speaker = z[3]
            if currentspeaker == "":
                currentspeaker = speaker

            if speaker == currentspeaker:
                start = z[0]
                stop = z[1]
                speakers[i].append([start, stop])
            else:
                i = i + 1
                start = z[0]
                stop = z[1]
                speakers[i].append([start, stop])

            currentspeaker = speaker
            # if w == "S":
                #    speakers[i + 1].append([z[0], z[1]])

    counter = 0.1
    problemnums = [".1", ".2", ".3", ".4", ".5", ".6", ".7", ".8", ".9", "1.0", "2.0", "3.0", "4.0", "5.0", "6.0", "7.0", "8.0", "9.0"]
    line = ""
    for key, value in speakers.items():
        for t in value:
            #COMMENT WRITE OUT IF WANT ONLY THE FILENAMES FOR ENTRAINMENT ANALYSIS
            write(wavfile, float(t[0]), float(t[1]), counter, key, outdir)

            # COMMENT LINE AND FILENAMES OUT IF WANT ONLY CHUNKED WAV FILES
            line = wavfile + "," + "speaker" + str(key) + "," + str(t[0]) + "," + str(t[1]) + "," + str(counter) + "\n"
            filenames.write(line)

            counter += .001

            for p in problemnums:
                if p in str(counter): counter += .001
            while abs(decimal.Decimal(str(counter)).as_tuple().exponent) < 3:
                counter += .001

    filenames.close()
             

def write(infile, t0, t1, counter, key, outdir):
    infileSplit = infile.split("\\")
    filename = infileSplit[len(infileSplit)-1].split(".wav")[0]

    outfilename = outdir + "\\speaker" + str(key) + "\\" + str(counter) + "_" + filename + '.wav'
    win = wave.open(infile, 'rb')
    wout = wave.open(outfilename, 'wb')

    s0, s1 = int(t0*win.getframerate()), int(t1*win.getframerate())
    win.readframes(s0) # discard
    frames = win.readframes(s1-s0)
    #nchannels = win.getnchannels()

    #data_per_channel = [frames[offset::nchannels] for offset in range(nchannels)]

    wout.setparams(win.getparams())
    #wout.setnchannels(1)
    #wout.setnframes()
    wout.writeframes(frames)

    win.close()
    wout.close()

    #print str(counter)


def main():
    segment(r"D:\ASU\Experimenter\Audio\R05_0018.wav", r"D:\ASU\Experimenter\TextGrid\R05_0018.textGrid",
            r"D:\ASU\Experimenter\TextGrid\SegmentedAudio")


if __name__ == '__main__': main()

'''

        try:
		infile = sys.argv[1]
		turnFile = sys.argv[2]
		IPUFile = sys.argv[3]
		segment(infile, turnFile, IPUFile)
	except:
		print 'usage: ./segmentWav_decimalNames.py wavFile turnFile IPUFile'
		sys.exit(2)
	return
'''

