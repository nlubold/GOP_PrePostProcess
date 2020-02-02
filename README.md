# GOP_PostProcess

The files in this repository are primarily Python scripts written for pre and post processing of audio and transcript data in the analysis of articulatory precision or goodness of pronunciation. The files are described in more detail below.

## Parsing Audio

PRE_segmentWavTextGrid.py:  This script contains the functions to parse audio and write out individual audio files that can then be used to for the calculation of articulatory precision or other analyses. 

textgrid.py:  This script enables reading and writing of Praat textgrid files.

## Analyzing Data

POST_analyzingGOP.py:  This script accepts a directory of GOP.txt files (originating from the kaldi-dnn-ali-gop project). The GOP text files contain the articulatory precision by phoneme. The script also accepts a file of utterances to ignore based on utterance ID. It aggregates the GOP values per utterance.  

POST_identifyBadUtterances.py:  This script identifies utterances with filled pauses, laughter, or other features which are not ideal for analyzing articulatory precision. 

POST_VowelConsonantSyllableAnalysis: This set of scripts will extract the GOP of vowels, consonants, and syllables per utterance.
