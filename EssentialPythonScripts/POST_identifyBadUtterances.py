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


    filledpausesList = open("ignoreUtterances.csv", 'a')

    counter = 0
    goodCounter = 0
    with open(directories, 'r') as f:
        for line in f:
            directory = line.strip('\n')
            filenames = []
            for file in sorted(os.listdir(directory)):
                if file.endswith(".lab"):
                    filenames.append(file)

            for f in filenames:
                name = f.split(".lab")[0]

                with open(os.path.join(directory, f), 'r') as currentLabFile:
                    for text in currentLabFile:
                        for word in filled_pauses:
                            if word in text:
                                counter += 1
                                filledpausesList.write(name + "," + text + "\n")
                                break
                            else:
                                goodCounter += 1

    print "Number of identified utterances: ", counter, " out of ", goodCounter
    filledpausesList.close()

# usage: python wavtest.py filename.wav
def main():
    if len(sys.argv) != 2:
        print ('usage: ./badutterance.py directoryLabFiles')
        sys.exit(1)


    alldirectories = sys.argv[1]
    identifyUtterances(alldirectories)



if __name__ == '__main__': main()