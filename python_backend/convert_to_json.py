#!/usr/bin/python
# ---------------------------------------------------------- #
# Script: convert_to_json.py
# --------------------------
# converts files from the old format to the new one, json
#
#
#
#
# ---------------------------------------------------------- #
#--- Standard ---
import os
import sys

#--- JSON ---
import json

#--- My files ---
from common_utilities import print_error, print_status
from J_Joint import J_Joint
from J_Skeleton import J_Skeleton


# Function: get_skeleton_timeseries
# ---------------------------------
# given an open file, this will read in the next skeleton
def read_in_skeletons (entire_file):

	skeletons = []

	### Step 1: get each section by itself ###
	sections = [s for s in entire_file.split ("--- frame ---") if len(s) > 5]

	timestamp = 0
	for section in sections:

		#--- lines = list of all lines that have joint content ---
		# lines = [line for line in section.split ('\n') if len(line) > 20 and type(line[0]) == type(0)]
		lines = [line for line in section.split ('\n') if len(line) > 20 and line[0].isdigit ()]

		#--- get joint locations ---
		joints = {}
		for line in lines:

			splits = line.split (":")
			
			joint_name = int(splits[0])
			rest = splits[1]
			splits = rest.split(',')
			x = float (splits[0])
			y = float (splits[1])
			z = float (splits[2])

			joints[joint_name] = J_Joint (x, y, z, joint_name)


		#--- create/add new skeleton with joints ---
		new_skeleton = J_Skeleton(timestamp, joints)
		skeletons.append (new_skeleton)

		#--- increment timestamp ---
		timestamp += 1

	return skeletons


# Function: print_txt
# -------------------
# prints out the skeletons as text files (more primitive...)
def record_to_txt (skletons, outfile_name):
	outfile = open(outfile_name, 'w')
	for skeleton in skeletons:
		outfile.write (skeleton.__str__())
	return


if __name__ == "__main__":

	### Step 1: get/sanitize args ###
	args = sys.argv
	if len(args) != 3:
		print_error ("Not enough arguments", "Usage: ./convert_to_json.py infile outfile")
	infile_name = args[1]
	outfile_name = args[2]

	### Step 2: read in infile ###
	print_status ("Main", "Opening infile")
	entire_infile = open (infile_name, 'r').read ()
	skeletons = read_in_skeletons (entire_infile)

	### Step 2: write out skeletons ###
	print_status("Main", "Writing in txt format to outfile")
	record_to_txt(skeletons, outfile_name)

	### Step 3: get json representation ###
	# print_status("Main", "Getting json representations")
	# json_skeletons_list = [s.json () for s in skeletons]

	### Step 4: open outfile and write ###
	# print_status ("Main", "Writing to outfile")
	# outfile = open(outfile_name, 'w')
	# outfile.write (json.dumps(json_skeletons_list))















