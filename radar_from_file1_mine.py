import scipy.io as w
import scipy as sp
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavefile

def dbv (myin):
    return(20*sp.log10(abs(myin)))

FS,data=wavefile.read('running_outside_20ms.wav')

c = 3e8 #Speed of light
# Variables for trigger detection
thresh = 0 #MIT wav file has bipolar "square wave" so zero crossing good starting thresh"
Tp = 20e-3 #chirp time in sec
N = int(FS * Tp) #Number of samples per chirp
count = 0
sif=[]
time=[]
count=0

#Input is inverted:
trig=-1*data[:,0] #Obtain trigger pulse
bb_raw=-1*data[:,1] #Obtain baseband data

s_trig=trig > thresh
for i in range(100,s_trig.size): #Loop over entire data set (save first 100 samples)
    if s_trig[i] == 1 and sp.mean(s_trig[i-11:i-1]) == 0:
        #mean=sp.mean(bb_raw[i:i+N-1])
        #sif.append(bb_raw[i:i+N-1]-mean)
        sif.append(bb_raw[i:i+N-1])
        time.append(i*1/FS)
        count=count+1

#cant convert entire array as in case last index is not a full collumn (this will cause the array to be cast in a single dim
#sif=sp.array(sif[0:len(sif)-2]) 

#zpad = int(8*N/2)
#
#v = dbv(sp.ifft(sif,zpad))#Matlab script says div by 2
