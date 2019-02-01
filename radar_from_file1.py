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
coef=3.051763129240305e-5

fstart = 2260e6; #(Hz) LFM start frequency for example
fstop = 2590e6; #(Hz) LFM stop frequency for example
#fstart = 2402E6; %(Hz) LFM start frequency for ISM band
#fstop = 2495E6; %(Hz) LFM stop frequency for ISM band
bw = fstop-fstart

#range resolution
rr = c/(2*bw)
max_range = rr * N / 2




#Input is inverted:
trig=(-1*data[:,0])*coef #Obtain trigger pulse
bb_raw=(-1*data[:,1])*coef #Obtain baseband data

s_trig=trig > thresh
t=sp.zeros(len(s_trig))

for i in range(99,s_trig.size-N+1): #Loop over entire data set (save first 100 samples)
    if s_trig[i] == True and sp.mean(s_trig[i-10:i]) == 0: #Create strobe on each rising edge and perform actions in if.  In this case each strobe saves N (# of samples in chirp)
        #mean_v=sp.mean(bb_raw[i:i+N-1],axis=0)
        #sif.append(bb_raw[i:i+N-1]-mean_v) 
        sif.append(bb_raw[i:i+N+1])
        time.append(i*1/FS)
        count=count+1

#sif2=sp.array(sif[0:len(sif)-2]) 
sif2=sp.array(sif)
sif3=sp.zeros(sif2.shape)

#Subtract collumn average
ave = sp.mean(sif2,axis=0)
for i in range(0,sif2.shape[0] - 1):
    sif3[i] = sif2[i,:] - ave


zpad = int(8*N/2)

v = dbv(sp.ifft(sif3,zpad,1))#Matlab script says div by 2
s = v[:,0:int(v.shape[1]/2)]
m = v.max()
domain = sp.linspace(0,max_range,zpad)
plt.imshow(s-m,vmin=-80,vmax=0,extent=[0,max_range,max(time),0],aspect='2')
plt.colorbar()
plt.xlabel('Distance (m)')
plt.ylabel('Time (s)')
plt.show()

