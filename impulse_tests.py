####################################################
#
#
#     Impulse Response Analysis
#
#            9-13-14
#
#		 aphdinpython.com
#
#
#
# This script runs the testing plan for impulse response
# recovery. It compares the recovered response to the
# original, and illustrates the theoretical recovery.
#
#
####################################################

import numpy as np
import matplotlib.pyplot as plt
import scikits.audiolab as audio  

np.set_printoptions(threshold=np.inf)

#===============================================#
#============Define Test Signals================#
#===============================================#

signals = ["linear_chirp", "exponential_chirp", "noise"];
signal_type = signals[0];
kirkeby = 0;

impulse_length = 2**15;
excitation_length = 2**15;
points = np.arange(0,excitation_length);
fs = 16000.0

if (signal_type == "linear_chirp"):

	'''''''''''''''''''''''''''''''''
	#=========Linear Chirp==========#
	'''''''''''''''''''''''''''''''''

	#===Chirp Parameters===#
	f0 = 0.0;
	f1 = fs/2.0;
	k = (f1-f0)/float(excitation_length);
	f = f0 + 0.5*k*points;

	#===Create Chirp===#
	excitation = np.sin(2.0*np.pi*(f*points)/fs);
	excitation = 0.707 * excitation/np.amax(excitation);

	#===Save Wav File===#
	audio.wavwrite(excitation,"linear_chirp.wav",fs,'pcm16');

elif (signal_type == "exponential_chirp"):

	'''''''''''''''''''''''''''''''''''
	#========Exponential Chirp========#
	'''''''''''''''''''''''''''''''''''

	#===Chirp Parameters===#
	f0 = 10.0;
	f1 = fs/2.0
	k = (f1/f0)**(1.0/float(excitation_length))

	#===Create Chirp===#
	excitation = np.sin( (2.0 * np.pi * f0 / np.log(k)) * (k**points-1.0) / fs)
	excitation = 0.707 * excitation/np.amax(excitation);

	#===Save Wav File===#
	audio.wavwrite(excitation,"exponential_chirp.wav",fs,'pcm16');

else:

	'''''''''''''''''''''''''''''''''''
	#==========Random Noise===========#
	'''''''''''''''''''''''''''''''''''
	excitation = np.random.normal(0,1.0,excitation_length);
	excitation = 0.707 * excitation/np.amax(excitation);
	
	#===Save Wav File===#
	audio.wavwrite(excitation,"excitation_noise.wav",fs,'pcm16');

exciation = np.r_[excitation,np.zeros(len(excitation))];

#===Test Response===#
impulse_response = np.asarray(np.arange(0,impulse_length),dtype=float);
impulse_response = np.r_[impulse_response,np.zeros(len(impulse_response))];

#=========Play Into Room=========#
room_response = np.convolve(impulse_response,excitation);

#===Pad with Zeros for FFT===#
if len(excitation) != len(room_response):
	print "\nWarning: Different Degree of Interpolation For FFT!\n";
	if len(excitation)>len(room_response):
		room_response = np.r_[room_response,np.zeros(len(excitation)-len(room_response))];
	else:
		excitation = np.r_[excitation,np.zeros(len(room_response)-len(excitation))];

#===Create Mismatched Filter===#
if kirkeby:
	
	#===Conjugate Response===#
	excitation_fft = np.fft.fft(excitation);
	conjugate_fft = np.conjugate(excitation_fft);
	
	#===Form Regularization===#
	regularization = np.random.uniform(0.1,1.1);
	regularization = 10e-8 * regularization / np.amax(regularization);

	#===Create Inverse Filter===#
	filter_fft = conjugate_fft/(conjugate_fft * excitation_fft + regularization);
	excitation_inverse = np.fft.ifft(filter_fft);

else:
	
	#===Flip Magnitude and Negate Phase===#
	excitation_fft = np.fft.fft(excitation);
	excitation_mag = 1.0/abs(excitation_fft);
	excitation_phase = np.exp(-1j*np.angle(excitation_fft));
	#max_val = np.amax(excitation_phase);
	#excitation_phase += np.linspace(-2.0, 2.0, len(excitation_phase)) + -1j *np.linspace(-2.0, 2.0, len(excitation_phase));
	#excitation_phase /= max_val;

	#===Create Inverse Filter===#
	filter_fft = excitation_mag * excitation_phase;
	excitation_inverse = np.fft.ifft(filter_fft);

#===Check for Kronecker===#
kronecker = np.convolve(excitation,excitation_inverse);
kronecker = np.r_[kronecker[0:0.5*len(kronecker)][::-1], kronecker[0.5*len(kronecker)::]];
kronecker_points = np.arange(-0.5*len(kronecker),0.5*len(kronecker));

#===Recover Room Response===#
room_fft = np.fft.fft(room_response);
output_fft = filter_fft * room_fft;
recovered_response = np.fft.ifft(output_fft)[0:2*impulse_length];

#===Plots===#
plt.figure(0);
plt.plot(impulse_response,label="Original");
plt.plot(recovered_response,label="Recovered");
plt.title("Recovered Impulse Response Comparison");
plt.xlim([0,len(impulse_response)]);
plt.legend();

plt.figure(1);
plt.plot(kronecker_points,kronecker);
plt.title("Kronecker Delta");
plt.show();
