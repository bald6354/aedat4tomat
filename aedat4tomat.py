#!/usr/bin/python


"""
data = {'e_p': e_p,
            'e_ts': e_ts,
            'e_x': e_x,
            'e_y': e_y,
            'f_image': f_image,
            'f_position': f_position,
            'f_size': f_size,
            'f_ts': f_ts,
            'f_framestart': f_framestart,
            'f_frameend': f_frameend,
            'f_expstart': f_expstart,
            'f_expend': f_expend,
            'i_ax': i_ax,
            'i_ay': i_ay,
            'i_az': i_az,
            'i_gx': i_gx,
            'i_gy': i_gy,
            'i_gz': i_gz,
            'i_mx': i_mx,
            'i_my': i_my,
            'i_mz': i_mz,
            'i_temp': i_temp,
            'i_ts': i_ts
           }
"""

import sys, getopt
from dv import AedatFile
import scipy.io as sio
import numpy as np

class Struct:
    pass

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('aedat4tomat.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('aedat4tomat.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print('Input file is "', inputfile)
    print('Output file is "', outputfile)
    
    #Define output struct
    out = Struct()
    out.data = Struct()
    out.data.polarity = Struct()
    out.data.frame = Struct()
    out.data.imu6 = Struct()

    #Events
    out.data.polarity.polarity = []
    out.data.polarity.timeStamp = []
    out.data.polarity.x = []
    out.data.polarity.y = []

    #Frames
    out.data.frame.samples = []
    out.data.frame.position = []
    out.data.frame.sizeAll = []
    out.data.frame.timeStamp = []
    out.data.frame.frameStart = []
    out.data.frame.frameEnd = []
    out.data.frame.expStart = []
    out.data.frame.expEnd = []

    #IMU
    out.data.imu6.accelX = []
    out.data.imu6.accelY = []
    out.data.imu6.accelZ = []
    out.data.imu6.gyroX = []
    out.data.imu6.gyroY = []
    out.data.imu6.gyroZ = []
    out.data.imu6.temperature = []
    out.data.imu6.timeStamp = []

    data = {'aedat': out}

    with AedatFile(inputfile) as f:

        # loop through the "events" stream
        for e in f['events']:
            out.data.polarity.timeStamp.append(e.timestamp)
            out.data.polarity.polarity.append(e.polarity)
            out.data.polarity.x.append(e.x)
            out.data.polarity.y.append(e.y)

        # loop through the "frames" stream
        for frame in f['frames']:
            out.data.frame.samples.append(frame.image)
            out.data.frame.position.append(frame.position)
            out.data.frame.sizeAll.append(frame.size)
            out.data.frame.timeStamp.append(frame.timestamp)
            out.data.frame.frameStart.append(frame.timestamp_start_of_frame)
            out.data.frame.frameEnd.append(frame.timestamp_end_of_frame)
            out.data.frame.expStart.append(frame.timestamp_start_of_exposure)
            out.data.frame.expEnd.append(frame.timestamp_end_of_exposure)

         # loop through the "imu" stream
        for i in f['imu']:
            a = i.accelerometer
            g = i.gyroscope
            m = i.magnetometer
            out.data.imu6.accelX.append(a[0])
            out.data.imu6.accelY.append(a[1])
            out.data.imu6.accelZ.append(a[2])
            out.data.imu6.gyroX.append(g[0])
            out.data.imu6.gyroY.append(g[1])
            out.data.imu6.gyroZ.append(g[2])
            out.data.imu6.temperature.append(i.temperature)
            out.data.imu6.timeStamp.append(i.timestamp)

    #Permute images via numpy
    tmp = np.transpose(np.squeeze(np.array(out.data.frame.samples)),(1,2,0))
    out.data.frame.numDiffImages = tmp.shape[2]
    out.data.frame.size = out.data.frame.sizeAll[0]
    out.data.frame.samples = tmp.tolist()
        
    #Add counts
    out.data.polarity.numEvents = len(out.data.polarity.x)
    out.data.imu6.numEvents = len(out.data.imu6.accelX)
    sio.savemat(outputfile, data)
    
if __name__ == "__main__":
   main(sys.argv[1:])