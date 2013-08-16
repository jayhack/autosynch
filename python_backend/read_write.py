#!/usr/bin/python
# ---------------------------------------------------------- #
# Script: read_write.py
# -------------------------------
# everything related to reading/writing from datafiles
#
#
#
#
# ---------------------------------------------------------- #
#--- Standard ---
import os
import sys
import pickle

#--- My files ---
from J_Joint import J_Joint
from J_Skeleton import J_Skeleton


# Function: read_in_skeletons
# ---------------------------------
# given an open file, this will read in the next skeleton
def read_in_skeletons (jvid_filename):

	### data ###
	skeletons = []
	infile_name = ''
	read_index = 0


	while True:
	
		#--- initial values ---
		original_index = -1
		exists = 0
		beat = 0
		pop = 0
		joints = {}

		### Step 1: make sure infile exists, open it ###
		infile_name = jvid_filename + "/" + str(read_index) + ".s"
		# print "infile name = " + infile_name
 		if not os.path.exists (infile_name):
			break
		infile = open (infile_name, 'r')

		### Step 2: read out the info from it ###
		lines 	=  [l.strip() for l in infile.readlines ()]

		original_index = int(lines[0])
		exists = int(lines[1])
		if exists == 1:
			beat = int(lines[2])
			pop = int(lines[3])

			joint_lines = lines[4:]

			for i in range(15):
				joint_line = joint_lines [i].strip().split (',')
				x = float(joint_line[0])
				y = float(joint_line[1])
				z = float(joint_line[2])
				x_abs = float(joint_line[3])
				y_abs = float(joint_line[4])
				z_abs = float(joint_line[5])
				joints[i] = J_Joint(x, y, z, x_abs, y_abs, z_abs, i)

		else:
			joints = None
			beat = 0
			pop = 0

		skeleton = J_Skeleton (read_index, original_index, exists, beat, pop, joints)
		skeletons.append (skeleton)
		read_index += 1

	return skeletons
		


# Function: write_out_skeletons
# -----------------------------
# prints out the skeletons to text files
def write_out_skeletons (skeletons, jvid_filename):

	write_index = 0
	for skeleton in skeletons:	

		outfile_name = jvid_filename + "/" + str(write_index) + ".s"
		outfile = open(outfile_name, 'w')
		outfile.write (skeleton.__str__())
		outfile.close ()
		write_index += 1
	return



if __name__ == "__main__":

	infilename = '/Users/jhack/Programming/NI/ni_template/Recordings/jay_training.sync/Marked/video.jvid'
	skeletons =	read_in_skeletons (infilename)



