import syllabifier, sys
from textgrid import TextGrid
import numpy as np
from phn_info import vowels, consonants
import argparse

def gop_feat(gop_vals, textgrid_file):
    """
    Calculate gop statistics on vowels, consonants and syllables
    :param gop_vals: gop values of one utterance extracted from gop files
    :param textgrid_file: textgrid file
    :return:
    """

    textgrid = TextGrid()
    textgrid.read(textgrid_file)

    phn_seq = ""
    for intervals in textgrid.tiers[1]:
        if intervals.mark is not None:
            if intervals.mark != 'SIL' and intervals.mark != 'SPN':
                phn_seq += " " + intervals.mark

    language = syllabifier.English
    syllables = syllabifier.syllabify(language, str(phn_seq))

    vowel_gop, consonants_gop, syllable_gop = [], [], []

    syllable_idx = 0  # determine which syllable current phoneme is in
    phn_idx = 0
    syllable_phn_gop = []
    for intervals in textgrid.tiers[1]:

        # vowels and consonants
        if intervals.mark is not None:
            if intervals.mark != 'SIL' and intervals.mark != 'SPN':
                if intervals.mark in vowels:
                    vowel_gop.append(gop_vals[phn_idx])
                elif intervals.mark in consonants:
                    consonants_gop.append(gop_vals[phn_idx])
                else:
                    continue

        # syllables
        if syllable_idx < len(syllables):
            current_syllable = syllables[syllable_idx][1] + syllables[syllable_idx][2] + syllables[syllable_idx][3]
            if intervals.mark is not None:
                if intervals.mark != 'SIL' and intervals.mark != 'SPN':
                    if intervals.mark in current_syllable:
                        syllable_phn_gop.append(gop_vals[phn_idx])
                    if intervals.mark == current_syllable[-1]:
                        syllable_idx += 1
                        syllable_gop.append(np.mean(syllable_phn_gop))
                        syllable_phn_gop = []

        if intervals.mark is not None:
            phn_idx += 1

    if not vowel_gop: vowel_gop.append(1)
    if not consonants_gop: consonants_gop.append(1)
    if not syllable_gop: syllable_gop.append(1)

    return [min(vowel_gop), min(consonants_gop), min(syllable_gop), #minimum gops of vowel, consonant and syllable
        np.mean(vowel_gop), np.mean(consonants_gop), np.mean(syllable_gop),
        # average gop of vowels, consonants and syllables
        np.std(vowel_gop), np.std(consonants_gop), np.std(syllable_gop),
        # standard deviation of gops of vowels, consonants and syllables
        np.std(vowel_gop) / np.mean(vowel_gop),
        np.std(consonants_gop) / np.mean(consonants_gop),
        np.std(syllable_gop) / np.mean(syllable_gop),  # standard deviation normalized by average
        ], ["gop_minV","gop_minC","gop_minSyl", "gop_avgV", "gop_avgC", "gop_avgSyl", "gop_stdV", "gop_stdC", "gop_stdSyl", "gop_VacroV", "gop_VacroC", "gop_VacroSyl",
            ]

def gop_feat_simple(gop_vals, textgrid_file):
    """
    Calculate gop statistics on vowels, consonants and syllables
    :param gop_vals: gop values of one utterance extracted from gop files
    :param textgrid_file: textgrid file
    :return:
    """

    textgrid = TextGrid()
    textgrid.read(textgrid_file)

    phn_seq = ""
    for intervals in textgrid.tiers[1]:
        if intervals.mark is not None:
            if intervals.mark != 'SIL' and intervals.mark != 'SPN':
                phn_seq += " " + intervals.mark

    language = syllabifier.English
    syllables = syllabifier.syllabify(language, str(phn_seq))

    vowel_gop, consonants_gop, syllable_gop = [], [], []

    syllable_idx = 0  # determine which syllable current phoneme is in
    phn_idx = 0
    syllable_phn_gop = []
    for intervals in textgrid.tiers[1]:

        # vowels and consonants
        if intervals.mark is not None:
            if intervals.mark != 'SIL' and intervals.mark != 'SPN':
                if intervals.mark in vowels:
                    vowel_gop.append(gop_vals[phn_idx])
                elif intervals.mark in consonants:
                    consonants_gop.append(gop_vals[phn_idx])
                else:
                    continue

        # syllables
        if syllable_idx < len(syllables):
            current_syllable = syllables[syllable_idx][1] + syllables[syllable_idx][2] + syllables[syllable_idx][3]
            if intervals.mark is not None:
                if intervals.mark != 'SIL' and intervals.mark != 'SPN':
                    if intervals.mark in current_syllable:
                        syllable_phn_gop.append(gop_vals[phn_idx])
                    if intervals.mark == current_syllable[-1]:
                        syllable_idx += 1
                        syllable_gop.append(np.mean(syllable_phn_gop))
                        syllable_phn_gop = []

        if intervals.mark is not None:
            phn_idx += 1

    if not vowel_gop: vowel_gop.append(1)
    if not consonants_gop: consonants_gop.append(1)
    if not syllable_gop: syllable_gop.append(1)

    return [np.mean(vowel_gop), np.mean(consonants_gop), np.mean(syllable_gop)], ["gop_avgV", "gop_avgC", "gop_avgSyl"]

def getUttLength(textgrid_file):
    textgrid = TextGrid()
    textgrid.read(textgrid_file)

    return textgrid.maxTime

def processDirectories(gopFiles, alignmentdirectories, outputfile):

    output = open(outputfile, "a")
    uttlengthfile = open(outputfile.strip(".csv")+"_uttlength.csv", "a")

    alignDir = []
    with open(alignmentdirectories, 'r') as f1:
        for line in f1:
            alignDir.append(line.strip('\n'))

    counter = 0
    with open(gopFiles, 'r') as f2:
        for line in f2:
            gopFile = line.strip('\n')

            with open(gopFile,'r') as gop_fid:
                for eachline in gop_fid:

                    outline = ""

                    uttid = eachline.split()[0] #uttid
                    spkname = uttid.split('_')[0]
                    gop_str = eachline.split()[2:-1] # gop values in string
                    gop_vals = [float(item) for item in gop_str] # to float numebrs

                    textgrid_file = alignDir[counter] + '/' + uttid + '.TextGrid' # path of TextGrid file corresponding to uttid

                    feat, descript = gop_feat_simple(gop_vals, textgrid_file)


                    for item in feat:
                        if item != 1 and item != 0: outline = (outline + "," + str(item))

                    output.write(uttid + outline + "\n")

                    length = getUttLength(textgrid_file)
                    uttlengthfile.write(uttid + "," + str(length) + "\n")



            counter += 1


    output.close()
    uttlengthfile.close()

# test
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--gop_files', help='text file with all gop files')
    parser.add_argument('--align_dir', help='text file with directories for all alignment files are stored')
    parser.add_argument('--out_dir', help='output file')

    args = parser.parse_args()

    processDirectories(args.gop_files, args.align_dir, args.out_dir)



    print("Done!")
