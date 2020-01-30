# GOP_PostProcess

The files in this repository are primarily Python scripts written for pre and post processing of audio and transcript data in the analysis of articulatory precision or goodness of pronunciation. The files are described in more detail below.

## Parsing Audio

CallSegmentWav.py:  This script is hard coded to read in the Dysarthric corpora and call segmentWav. SegmentWav parses audio based on information given in a Praat textgrid format about the beginning and ends of utterances.

SegmentWav.py:  This script contains the functions to parse audio and write out individual audio files that can then be used to for the calculation of articulatory precision or other analyses. 

textgrid.py:  This script enables reading and writing of Praat textgrid files.

parseTranscript.py:  This script reads in a transcript that contains timestamps in the Rev format and writes out a textgrid.

## Analyzing Data

analyzingGOP_v2.py:  This script accepts a directory of GOP.txt files (originating from the kaldi-dnn-ali-gop project). The GOP text files contain the articulatory precision by phoneme. The script also accepts a file of utterances to ignore based on utterance ID. It aggregates the GOP values per utterance.  

processValues_CalcEnt.py:  This script takes in the output of analyzingGOP_v2 with timing incorporated and writes out the ordered dialogues. It can also produce files for calculating proximity, synchrony and convergence but this depends highly on formating. 

identifyBadUtterances.py:  This script identifies utterances with filled pauses, laughter, or other features which are not ideal for analyzing articulatory precision. 
