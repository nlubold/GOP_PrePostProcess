
import argparse
import os
import textgrid
import pandas as pd
import wave
import decimal
import string
import re

'''
What does this program do: 
    given a directory of text grids and a corresponding directory of wav files, segment the wav file into utterances
    create a folder for each of the two speakers of interest: inv (investigatory) and par (participant)
    With the segmentation of the wav files, also generate corresponding .lab files with the same naming convention
    The .lab files will have all punctuation removed

To RUN:
    Hard coded essentials to change for new text grids:
    -- dyad (line 144-ish and 182-ish)
        Directions:  This captures the 'ID' of the dyad or speaker (i.e. dys01, 1, 2). It should also match
        the audio file name. For example, a textgrid file is named RhythmsStudy_1.TextGrid. The ID is 1 for the
        speaker. Dyad will refer to this 1. The audio files should contain ONLY the ID in the name, i.e. 1.wav.
        
        Options:   dyad = file.split(".")[0]                (this options assumes a name like 01.textgrid)
                   dyad = file.split("_")[1].split(".")[0]  (this options assumes a name like RhythmsStudy_1.textgrid)
    
    -- speakers (line 137-ish and 174-ish)
        Directions:  This refers to the InvervalTier name(s). Generally these capture in the textgrid who was speaking 
        (i.e. INV for investigator or Mary for generalizability). Each tier contains the start/stop and text info from
        the transcripts
        
        Options:    speakers= ["INV1", "INV2", "INV3", "PAR"]   (this options assumes four speakers and four tiers)
                    speakers = ["Mary"]                         (this options assumes one speaker, one tier)
    
    -- labfile and outfilename (lines 88-ish and 110-ish)
        Directions:  This writes the text and audio files out to the given directories (utt and lab)
        These directories should have a folder for every dyad and within every dyad, a folder for every speaker in 
        that dyad (there can be more than two). IF it is a monologue, then the dyadic folder is NOT needed.
        
        DYAD: 
            labfile = open(os.path.join(outdir, dyad, speaker, str(counter) + "_" + dyad + "_" + speaker + ".lab"), 'w')
            outfilename = os.path.join(outdir, dyad, speaker, str(counter) + "_" + dyad + "_" + speaker + '.wav')

        MONOLOGUE:
            outfilename = os.path.join(outdir, dyad, str(counter) + "_" + dyad + "_" + speaker + '.wav')
            labfile = open(os.path.join(outdir, dyad,  str(counter) + "_" + dyad + "_" + speaker + ".lab"), 'w')

    -- audio input name (line 162-ish)
        Directions:  This is for reading the audio file input (.wav). It will need to change based on if dyad or monologue
        If it is a dyad, it is assumed the name will be dyadID_speakerID.wav (i.e. 1_one.wav)
        
        Dyad:
            audio_file = os.path.join(ad, dyad + "_" + speaker + ".wav")

        Monologue:
            audio_file = os.path.join(ad, dyad + ".wav")
    
    INPUTS:
        --tgd:      directory to textgrids
        --audio:    directory to audiofiles
        --utt:      directory to where to write the segmented audio files
        --lab:      directory to where to write the segmented text files (as .lab files)
        
        If in PyCharm, change these under the Menu Item Run->Edit Configurations->Parameters
    
    Preprocessing Required PRIOR to running:
        You MUST have a folder for EVERY speaker and if it is dialogue data, folders for every dyad in the --utt 
        and --lab directory.
        
        Dyad example:  Healthy Corpus   -> Dyad1 -> INV, PAR, INV2  (dyad folders should match the file name ID)
                                        -> Dyad2 -> INV, PAR, INV2  (speaker folders should match textgrid labels for speakers)
        Mono example:  Healthy Corpus   -> 01   
                                        -> 02      (just need the ID for the speaker, match file name ID)
'''

startStopMappingFileName = "utteranceID_start_stop_length.csv"

def write_start_to_uttID(t0, t1, counter, dyad, speaker):
    outfile = open(startStopMappingFileName, 'a')
    outfile.write(str(counter) + "_" + dyad + "_" + speaker + "," + str(t0) + "," + str(t1) + "\n")
    outfile.close()

def write_len(text, counter, dyad, speaker, t0, t1):
    outfile = open(startStopMappingFileName, "a")

    spaces = ""
    for x in string.punctuation:
        spaces = spaces + " "

    trantable = str.maketrans(string.punctuation, spaces)
    patternRemove = re.compile(r'\[[a-z].*?\]')

    text = text.strip()
    text = re.sub(patternRemove, "", text)
    text = text.translate(trantable)
    text = ''.join([i if ord(i) < 128 else ' ' for i in text])
    text = text.split()

    outfile.write(str(counter) + "_" + dyad + "_" + speaker + "," + str(len(text)) + "," + str(t0) + "," + str(t1) + "\n")


def write_audio(infile, t0, t1, counter, dyad, speaker, outdir):
    # -------------------------------------------------- CHANGE IF DYAD VS MONOLOGUE ------------------
    outfilename = os.path.join(outdir, dyad, speaker, str(counter) + "_" + dyad + "_" + speaker + '.wav')

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

def write_lab(text, counter, dyad, speaker, outdir):
    # -------------------------------------------------- CHANGE IF DYAD VS MONOLOGUE ------------------
    labfile = open(os.path.join(outdir, dyad, speaker, str(counter) + "_" + dyad + "_" + speaker + ".lab"), 'w')

    spaces = ""
    for x in string.punctuation:
        spaces = spaces + " "

    trantable = str.maketrans(string.punctuation, spaces)
    patternRemove = re.compile(r'\[[a-z].*?\]')

    text = text.strip()
    text = re.sub(patternRemove, "", text)
    text = text.translate(trantable)
    text = ''.join([i if ord(i) < 128 else ' ' for i in text])
    text = " ".join(text.split())

    labfile.write(text)
    labfile.close()

# converting textgrid to a dataframe results in lines consisting of start, stop, name (content), tier
def parse_tg(tgd, ad, uttd, labd):

    problemnums = [".1", ".2", ".3", ".4", ".5", ".6", ".7", ".8", ".9", "1.0", "2.0", "3.0", "4.0", "5.0", "6.0",
                   "7.0", "8.0", "9.0"]

    # ------------------------------ CHANGE BASED ON TIER NAMES FOR SPEAKERS ----------------------
    speakers = ["one", "two"]

    counter = 0.101
    for file in sorted(os.listdir(tgd)):
        if file.endswith(".TextGrid"):
            print("Working on: ", file)
            # -----------------------------  CHANGE BASED ON FILE NAME ---------------------------
            dyad = file.split("C0")[1].split("_")[0]

            tg = textgrid.read_textgrid(os.path.join(tgd, file))
            df = pd.DataFrame(tg)

            for speaker in speakers:
                print("     Speaker: ", speaker)
                # -----------------------------  CHANGE BASED ON DYAD vs. MONOLOGUE ---------------------------
                audio_file = os.path.join(ad, dyad + "_" + speaker + ".wav")
                
                # data = df.loc[df["tier"] == (speaker + " [main]")]
                data = df.loc[df["tier"] == speaker]
                for index, row in data.iterrows():
                    # row[name] refers to the text of the utterance
                    if row["name"] != "":
                        write_audio(audio_file, row['start'], row['stop'], counter, dyad, speaker, uttd)
                        write_lab(row["name"], counter, dyad, speaker, labd)

                        counter = round(counter + .001, 3)

                        for p in problemnums:
                            if str(counter) == p:
                                counter = round(counter + .001, 3)
                                break
                        while abs(decimal.Decimal(str(counter)).as_tuple().exponent) < 3:
                            counter = round(counter + .001, 3)

# doesn't write out audio or lab files - just writes to a single csv the start times of utterances
def link_uttid_start(tgd):
    problemnums = [".1", ".2", ".3", ".4", ".5", ".6", ".7", ".8", ".9", "1.0", "2.0", "3.0", "4.0", "5.0", "6.0",
                   "7.0", "8.0", "9.0"]

    # ------------------------------ CHANGE BASED ON TIER NAMES FOR SPEAKERS ----------------------
    speakers = ["one", "two"]

    for file in sorted(os.listdir(tgd)):
        counter = 0.101
        if file.endswith(".TextGrid"):
            print("Working on: ", file)
            # next two lines take file name and pull out the identifier for the dyad / monologue speaker
            # -----------------------------  CHANGE BASED ON FILE NAME ---------------------------
            dyad = file.split("C0")[1].split("_")[0]
            tg = textgrid.read_textgrid(os.path.join(tgd, file))
            df = pd.DataFrame(tg)
            for speaker in speakers:
                print("     Speaker: ", speaker)
                data = df.loc[df["tier"] == speaker]
                for index, row in data.iterrows():
                    if row["name"] != "":
                        #write_start_to_uttID(row['start'], row['stop'], counter, dyad, speaker)
                        write_len(row["name"], counter, dyad, speaker, row['start'], row['stop'])

                        counter = round(counter + .001, 3)

                        for p in problemnums:
                            if str(counter) == p:
                                counter = round(counter + .001, 3)
                                break
                        while abs(decimal.Decimal(str(counter)).as_tuple().exponent) < 3:
                            counter = round(counter + .001, 3)

def main():
    parser = argparse.ArgumentParser(description='Segment audio and textgrids.')
    parser.add_argument('--tgd', dest="tgd", help='text grid directory')
    parser.add_argument('--audio', dest="audio", help='audio directory')
    parser.add_argument('--utt', dest="utt", help='utterances directory')
    parser.add_argument('--lab', dest="lab", help="lab files directory")
    args = parser.parse_args()

    parse_tg(args.tgd, args.audio, args.utt, args.lab)
    link_uttid_start(args.tgd)

if __name__ == '__main__': main()
