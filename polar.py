####################################################
#
#
#     Half Polar Plot Example
#
#          10-24-14
#
#      aphdinpython.com
#
#
#
# This script illustrates a function for creating a
# half polar plot using matplotlib. It synthesizes
# some data, plots it, and saves the image.
#
#
####################################################

import numpy as np
import matplotlib.pyplot as plt
from  matplotlib import patches

def make_half_polar(fignum):
	
	#===Create Figure===#
	plt.figure(fignum);
	ax = plt.subplot(111, frameon=False);
	font_size = 14;

	#===Add Top Half of Unit Circle===#
	unit_arc = patches.Arc( (0,0), width = 2, height = 2, theta1=0.0, theta2=180.0, color='black', ls='dashed', linewidth=1.5 );
	ax.add_patch(unit_arc);

	#===Add Half Contour Line===#
	half_unit_arc = patches.Arc( (0,0), width = 1, height = 1, theta1=0.0, theta2=180.0, color='black', ls='dashed', linewidth=0.5 );
	ax.add_patch(half_unit_arc);

	#===Add Angle Ticks===#		
	p45 = np.exp( 1j*0.25*np.pi);
	plt.rc('text', usetex=True);
	ax.text(0.9*0.5, 0, r'$0$', fontsize=0.8*font_size)
	ax.text(-0.975*0.5, 0, r'$\pi$', fontsize=font_size)
	ax.text(0.5*p45.real, 1.125*0.5*p45.imag, r'$\frac{\pi}{4}$', fontsize=font_size)
	ax.text(-0.5*p45.real, 1.125*0.5*p45.imag, r'$\frac{3\pi}{4}$', fontsize=font_size)

	#===Add Radial Lines===#
	ax.plot([0, 0], [0, 1], '--', color="black", linewidth=0.5);
	ax.plot([0, p45.real], [0,p45.imag], '--', color="black", linewidth=0.5 );
	ax.plot([0, -p45.real], [0,p45.imag], '--', color="black", linewidth=0.5 );

	#===Set Axes===#
	plt.axis([-1.2, 1.2, -0.1, 1.7])

	#===Fix Axes===#
	ax.set_yticks([]);
	ax.set_yticklabels([])
	x_ticks = [-1,1];
	ax.set_xticks([])
	ax.set_xticklabels([]);

	return ax;

#===Make Figure===#
ax = make_half_polar(0);

#===Create Data===#
nyq_rate = 24000.0;
frequencies = np.linspace(0,nyq_rate,25)/nyq_rate;
phasor = np.array([ 1.0*np.exp(1j*f*np.pi) for f in frequencies]);

#===Plot Data===#
tp = ax.plot(phasor.real, phasor.imag, 'rx', ms=10, label="Frequencies")
plt.setp( tp, markersize=12.0, markeredgewidth=3.0, markeredgecolor='r', markerfacecolor='r')
plt.legend();

#===Save Figure===#
plt.savefig("polar.jpg");
