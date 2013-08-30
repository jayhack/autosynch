#!/usr/bin/python
# ---------------------------------------------------------- #
# Script: add_derivatives
# -----------------------
# adds derivatives to a list of skeletons
#
#
#
# ---------------------------------------------------------- #

# Class: Derivative
# -----------------
# used in classification
class Derivative:
	x = None
	y = None
	z = None

	def __init__ (self, x, y, z):
		self.x = x
		self.y = y
		self.z = z


# Function: get_first_derivatives
# -------------------------------
# given a list of all skeletons, this returns a list of first derivatives
# derivative_length: the number of elements back you go in order to get the deriv
# - NOTE: framerate for this bitch is apparently 30 frames/second
def get_derivatives (entries, derivative_length):

	cur_index = derivative_length
	prev_index = 0
	considering_entries = entries[cur_index:]

	first_derivatives = []

	prev = entries[prev_index]
	for cur in considering_entries:

		derivs = {}
		if cur:
			for i in range(len(cur)):


				dx_dt = cur[i].x - prev[i].x
				dy_dt = cur[i].y - prev[i].y
				dz_dt = cur[i].z - prev[i].z

				derivs[i] = Derivative (dx_dt, dy_dt, dz_dt)

			prev_index += 1
			prev = entries[prev_index]

		first_derivatives.append (derivs)

	return first_derivatives



# Function: add_derivatives_to_skeletons
# --------------------------------------
# returns skeletons_with_derivs
def add_derivatives_to_skeletons (skeletons_raw, fd_interval_1, fd_interval_2, sd_interval_1, sd_interval_2):


	if (fd_interval_1 >= fd_interval_2):
		print_error ("fd_interval_1 is <= fd_interval_2", "make sure that 1 is smaller than 2")
	if (sd_interval_1 >= sd_interval_2):
		print_error ("sd_interval_1 is <= sd_interval_2", "make sure that 1 is smaller than 2")

	### Step 1: get the first and second derivatives ###
	joints = [s.joints for s in skeletons_raw]
	fd_1_raw 	=	get_derivatives 	(joints, 	fd_interval_1)
	fd_2_raw	=	get_derivatives 	(joints, 	fd_interval_2)
	sd_1_raw 	= 	get_derivatives 	(fd_1_raw, 	sd_interval_1)
	sd_2_raw	= 	get_derivatives 	(sd_1_raw, 	sd_interval_2)	

	### Step 4: associate them with the original skeletons ###
	skeletons_with_derivs = skeletons_raw[fd_interval_2 + sd_interval_2:]
	fd_1 = fd_1_raw [sd_interval_2:]
	fd_2 = fd_2_raw [sd_interval_2:]
	sd_1 = sd_1_raw
	sd_2 = sd_2_raw
	for i in range(len(skeletons_with_derivs)):
		skeletons_with_derivs[i].fd_1 = fd_1[i]
		skeletons_with_derivs[i].fd_2 = fd_2[i]
		skeletons_with_derivs[i].sd_1 = sd_1[i]
		skeletons_with_derivs[i].sd_2 = sd_2[i]

	return skeletons_with_derivs