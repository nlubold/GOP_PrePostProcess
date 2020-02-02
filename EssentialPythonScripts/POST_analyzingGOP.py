import sys
import os
import string
import numpy as np
#from sklearn.linear_model import LinearRegression
#from matplotlib import pyplot


# Reads in gop files from directory and creates a single data structure to hold the data
# performs analysis


# calculate the average GOP per turn and plot, ignore zeros
def averageGOP(data):

    uttAvg = open("uttavg.csv", "w")
    average = {}
    for speaker, uttData in data.iteritems():

        numUtt = 0
        average[speaker] = []

        for utt, value in uttData.iteritems():

            average[speaker].append(np.average(value))
            uttAvg.write(speaker + "," + utt + "," + utt + "_" + speaker + "," + str(np.average(value)) + "\n")
            numUtt += 1

        print("Number Utterances: ", numUtt)

    uttAvg.close()

    outfile = open("GOPAvg.csv", "w")
    #outfile = open("E:\\Nikki\\Dropbox\\misc\\Research\\Post-doc\\Data\\GOP_Results\\1stTenDyadResults\\averageGOP.csv", "a")
    for key, values in average.iteritems():
        line1 = key + ","
        lineHalf_1 = key + "_1H" + ","
        lineHalf_2 = key + "_2H" + ","
        lineAltHalf_1 = key + "_A1H" + ","
        lineAltHalf_2 = key + "_A2H" + ","
        lineAltHalf_3 = key + "_A3H" + ","
        lineAltHalf_4 = key + "_A4H" + ","
        lineQuarter_1 = key + "_1Q" + ","
        lineQuarter_4 = key + "_4Q" + ","

        length = len(values)
        counter = 0

        for i in values:
            line1 = line1 + str(i) + ","

            if (counter < length/2):
                lineHalf_1 = lineHalf_1 + str(i) + ","
            else:
                lineHalf_2 = lineHalf_2 + str(i) + ","

            if (counter % 2 == 0 and counter < length/2):
                lineAltHalf_1 = lineAltHalf_1 + str(i) + ","
            elif (counter % 2 == 0):
                lineAltHalf_2 = lineAltHalf_2 + str(i) + ","

            if (counter % 2 != 0 and counter < length/2):
                lineAltHalf_3 = lineAltHalf_3 + str(i) + ","
            elif (counter % 2 != 0):
                lineAltHalf_4 = lineAltHalf_4 + str(i) + ","


            if (counter < length/4):
                lineQuarter_1 = lineQuarter_1 + str(i) + ","
            elif (counter >= (length/4)*3):
                lineQuarter_4 = lineQuarter_4 + str(i) + ","

            counter += 1


        outfile.write(line1 + "\n")
        outfile.write(lineHalf_1 + "\n")
        outfile.write(lineHalf_2 + "\n")
        outfile.write(lineAltHalf_1 + "\n")
        outfile.write(lineAltHalf_2 + "\n")
        outfile.write(lineQuarter_1 + "\n")
        outfile.write(lineQuarter_4 + "\n")


    outfile.close()




def extractData(dirFiles):

    chars = "[]"
    counter = ""
    ID = ""
    allspeakers = {}
    onespeaker = {}

    for file in sorted(os.listdir(dirFiles)):
        if file.endswith(".txt"):
            with open(dirFiles + "/" + file, 'r') as f:
                for line in f:
                    line = line.split(" ", 1)
                    sarray = np.array(line[1].translate(string.maketrans("", "", ), chars).rstrip().lstrip().split(" "))
                    darray = sarray.astype(np.float)
                    counter = line[0].split("_",1)[0]

                    if ID == "":
                        ID = line[0].split("_",1)[1]
                        onespeaker[counter] = darray

                    elif ID != line[0].split("_",1)[1]:
                        allspeakers[ID] = onespeaker
                        onespeaker = {}

                        counter = line[0].split("_",1)[0]
                        ID = line[0].split("_",1)[1]
                        onespeaker[counter] = darray

                    else:
                        onespeaker[counter] = darray



    allspeakers[ID] = onespeaker
    return allspeakers


def main():
    if len(sys.argv) != 2:
        print('usage: ./readfile2.py dirFiles')
        sys.exit(1)

    dirFiles = sys.argv[1]

    data = extractData(dirFiles)
    averageGOP(data)


if __name__ == '__main__': main()

