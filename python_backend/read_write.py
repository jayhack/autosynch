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


# Function: get_skeleton_timeseries
# ---------------------------------
# given an open file, this will read in the next skeleton
def read_in_skeletons (filename):

	skeletons = []

	### Step 1: open file, get contents ###
	f = open(filename, 'r')
	entire_file = f.read ()

	### Step 1: get each section by itself ###
	sections = [s for s in entire_file.split ("\n\n") if len(s) > 5]

	timestamp = 0
	for section in sections:

		#--- lines = list of all lines except for the newline character ---
		all_lines = [line for line in section.split ('\n') if len(line) > 5]

		#--- get timestamp --
		top_line = all_lines[0]
		digits = ''.join([c for c in top_line if c.isdigit()])
		timestamp = int(digits)


		#--- get joint locations ---
		joint_lines = [l for l in all_lines if l[0].isdigit()]
		joints = {}
		for line in joint_lines:

			splits = line.split (":")
			
			joint_name = int(splits[0])
			rest = splits[1][2:-1]

			splits = rest.split(',')
			x = float (splits[0])
			y = float (splits[1])
			z = float (splits[2])

			joints[joint_name] = J_Joint (x, y, z, joint_name)

		#--- get pop ---
		pop_line = [l for l in all_lines if 'p' in set(l)][0]
		if '1' in set(pop_line): 
			pop = 1
		else:
			pop = 0

		#--- get beat ---
		beat_line = [l for l in all_lines if 'b' in set(l)][0]
		if '1' in set(beat_line): 
			beat = 1
		else:
			beat = 0

		#--- create/add new skeleton with joints ---
		new_skeleton = J_Skeleton(timestamp, joints, pop=pop, beat=beat)
		skeletons.append (new_skeleton)

		#--- increment timestamp ---
		timestamp += 1

	f.close ()

	return skeletons




# Function: write_out_skeletons
# -----------------------------
# prints out the skeletons to text files
def write_out_skeletons (skeletons, outfile_name):
	outfile = open(outfile_name, 'w')
	for skeleton in skeletons:
		outfile.write (skeleton.__str__())
	return