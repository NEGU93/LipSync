# LipSync
by: José Agustín Barrachina & Matias Dwek

![GUI](https://github.com/NEGU93/LipSync/blob/master/Capture.PNG)

This programs loads an audio of one or two speakers and performs the following audio processing algorithms.

- Phonems Identifier using a LPC analysis system and formants detection
- Voice recognition using a RNN-LMST [[1]](#1)
  - Input of the network 13 MFCC (Mel-Frequency Cepstral Coeficients)
  - 3 hidden layers
  - 250 LSTM cells
  - Optimizer: Adam
  - Loss: CTC (Connectionist Temporal Classification)
- Speaker recognition (up to two speakers) using a GMM (Gaussian Mixture Model) [[2]](#2)
- Speed modifier
  - Uses over/sub sampling to avoid deep/acute deformation
- Pitch modification using FFT


## GUI

- Mouth image shows the speaker mouth movement
- Progress line in green (in sync with the playing audio)
- Done with pyQT5


## References

<a id="1">[1]</a> 
Abdel-rahman Mohamed Alex Graves and Geoffrey Hinton (2012). 
“SPEECH RECOGNITION WITH DEEP RECURRENT NEURAL NETWORKS”. 
Department of Computer Science, University of Toronto.

<a id="2">[2]</a> 
Vibha Tiwari (2010). 
“MFCC and its applications in speaker recognition”. En: International journal on emerging
technologies 1.1, p´ags. 19-22.
