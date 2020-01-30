__author__ = 'Nikki'

import sys
import os

'''
Identify 'ignore' files if line contains filled pauses - loops through directory of lab files and sees if they have a filled pause and are 'small'

Next steps:
1. figure out how to ignore ALL filled pauses everywhere (longer utterances too)
2. use this to re-create correct transcripts
'''




filled_pauses = ['295',
'Uhhuh ',
'1 95',
'195',
'[laughs]',
'laughs',
'A ',
'Aa',
'Ah ',
'Em',
'er',
'Hm',
'Hmm',
'Hmmm',
'Mm hmm',
'Mm',
'Mmm',
'Mmmm',
'mmhmm',
'mmmm',
'Ummm',
'Mmhmm',
'Mmkay',
'Mmmm',
'oh',
'Oh',
'Oh my',
'Oh',
'Ohhh',
'Ohoh no',
'Uh',
'Uh huh',
'uh',
'um',
'Uhuh',
'um',
'Um',
'Umum',
'Ye ',
]

def identifyUtterances(directories):


    filledpausesList = open("E:\\Nikki\\Dropbox\\misc\\Research\\Post-doc\\Data\\ignoreUtterances.csv", 'a')

    with open(directories, 'r') as f:
        for line in f:
            line = line.strip('\n')
            filenamesplit = (line.split("\\"))
            speaker = filenamesplit[len(filenamesplit)-1]

            for i in range(1,3):
                speakerDir = line + "\\speaker" + str(i) + "\\"

                filenames = []

                for file in sorted(os.listdir(speakerDir)):
                    if file.endswith(".lab"):
                        filenames.append(file)

                for f in filenames:
                    name = f.split(".lab")[0]

                    with open(speakerDir + "\\" + f, 'r') as currentLabFile:
                        for text in currentLabFile:
                            for word in filled_pauses:
                                if word in text and len(text.split()) < 3:
                                    filledpausesList.write(speaker + "," + name + "," + text + "\n")
                                    break


    filledpausesList.close()

# usage: python wavtest.py filename.wav
def main():
    if len(sys.argv) != 2:
        print ('usage: ./badutterance.py directoryLabFiles')
        sys.exit(1)


    alldirectories = sys.argv[1]


    identifyUtterances(alldirectories)



if __name__ == '__main__': main()