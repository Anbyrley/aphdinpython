####################################################
#
#
#        Useful Image Masks
#
#            9-15-14
#
#        aphdinpython.com
#
#
#
# This script creates some useful masks for image
# processing. Namely, circles, rectangles, and annuli.
#
#
####################################################

import numpy as np
from PIL import Image

np.set_printoptions(threshold=np.inf)

#=====================================#
#===========Draw Rectangle============#
#=====================================#
pil_array = np.zeros((1000,1000));
t_array = np.linspace(0,1,1000);

#===Define Location and Size of Rectangle===#
center = (500,500);
x_length = 500;
y_length = 500;

#===Define X Line===#
x_start = int(center[0] - 0.5*x_length);
x_end = int(center[0] + 0.5*x_length);
x_line = lambda t: x_start + t*(x_end-x_start);

#===Define Y Line===#
y_start = int(center[1] + 0.5*y_length);
y_end = int(center[1] - 0.5*y_length);
y_line = lambda t: y_start + t*(y_end-y_start);

#===Outline Rectangle===#
for t in t_array:

	#===Draw Bottom Line===#
	pil_array[y_start,x_line(t)] = 1.0;

	#===Draw Top line===#
	pil_array[y_end,x_line(t)] = 1.0;

	#===Draw Right Line===#
	pil_array[y_line(t),x_end] = 1.0;

	#===Draw Left Line===#
	pil_array[y_line(t),x_start] = 1.0;

pil_im = Image.fromarray(255*pil_array.astype(np.uint8));
pil_im.save("rectangle.jpg");


#=====================================#
#==========Rectangle Masks============#
#=====================================#
x_array = x_line(t_array);
y_array = y_line(t_array); 

#===Define Bounds===#
min_x = min(x_array);
max_x = max(x_array);
min_y = min(y_array);
max_y = max(y_array);

#===Mask Rectangles Inside===#
pil_array = np.zeros((1000,1000));
for x_val in range(pil_array.shape[0]):
	for y_val in range(pil_array.shape[1]):
		if x_val>=min_x and x_val<=max_x and y_val>=min_y and y_val<=max_y:
			pil_array[y_val,x_val] = 1.0;
pil_im = Image.fromarray(255*pil_array.astype(np.uint8));
pil_im.save("rectangles_masked_inside.jpg");

#===Mask Rectangles Outside===#
pil_array = np.zeros((1000,1000));
for x_val in range(pil_array.shape[0]):
	for y_val in range(pil_array.shape[1]):
		if x_val<=min_x or x_val>=max_x or y_val<=min_y or y_val>=max_y:
			pil_array[y_val,x_val] = 1.0;
pil_im = Image.fromarray(255*pil_array.astype(np.uint8));
pil_im.save("rectangles_masked_outside.jpg");

#=====================================#
#==============Circles================#
#=====================================#

#===Outline Circles===#
pil_array = np.zeros((1000,1000));
center = (500,500);
radii = [100,200,300];
for radius in radii:

	x = lambda a: radius*np.cos(a) + center[0];
	y = lambda a: radius*np.sin(a) + center[1];

	theta = np.linspace(0,2*np.pi,2000);
	x_array = x(theta);
	y_array = y(theta);

	#===Draw Circle===#
	for t in range(int(len(x_array))):
		pil_array[int(x_array[t]),int(y_array[t])] = 1.0;

pil_im = Image.fromarray(255*pil_array.astype(np.uint8));
pil_im.save("circles.jpg");

#===Mask Circles Inside===#
pil_array = np.zeros((1000,1000));
center = (500,500);
radii = [100];
for radius in radii:
	#===Fill Inside===#	
	for x_val in range(pil_array.shape[0]):
		for y_val in range(pil_array.shape[1]):
			rad = np.sqrt((x_val-center[0])**2.0 + (y_val-center[1])**2.0);
			if rad<=radius:
				pil_array[y_val,x_val] = 1.0;
pil_im = Image.fromarray(255*pil_array.astype(np.uint8));
pil_im.save("circles_masked_inside.jpg");

#===Mask Circles Outside===#
pil_array = np.zeros((1000,1000));
center = (500,500);
radii = [100];
for radius in radii:
	#===Fill Outside===#	
	for x_val in range(pil_array.shape[0]):
		for y_val in range(pil_array.shape[1]):
			rad = np.sqrt((x_val-center[0])**2.0 + (y_val-center[1])**2.0);
			if rad>=radius:
				pil_array[y_val,x_val] = 1.0;
pil_im = Image.fromarray(255*pil_array.astype(np.uint8));
pil_im.save("circles_masked_outside.jpg");


#=====================================#
#===============Annulus===============#
#=====================================#
outer_array = np.zeros((1000,1000));
inner_array = np.zeros((1000,1000));
outer_radius = 200;
inner_radius = 100;
center = (500,500);

#===Inner First===#
for x_val in range(pil_array.shape[0]):
	for y_val in range(pil_array.shape[1]):
		rad = np.sqrt((x_val-center[0])**2.0 + (y_val-center[1])**2.0);
		if rad>=inner_radius:
			inner_array[y_val,x_val] = 1.0;

#===Outer Second===#	
for x_val in range(pil_array.shape[0]):
	for y_val in range(pil_array.shape[1]):
		rad = np.sqrt((x_val-center[0])**2.0 + (y_val-center[1])**2.0);
		if rad<=outer_radius:
			outer_array[y_val,x_val] = 1.0;

pil_array = np.logical_and(inner_array,outer_array);
pil_im = Image.fromarray(255*pil_array.astype(np.uint8));
pil_im.save("annulus.jpg");
