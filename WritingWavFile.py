import wave


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