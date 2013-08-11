#!/usr/bin/python 
import math
import re
from collections import defaultdict

# Source file of raw camera data
skeleton_source = "../Data/sam_dancing.txt"
output_source = "manipulation_test.txt"


# formatted skeleton data
# Format:
# skeleton_collection[int instance_number][body_part][axis] 
skeleton_collection = []

# manipulated skeleton data
# Format:
# manipulated_data[int instance_number][body_part][axis] 
manipulated_data = []


body_parts = ['head', 'neck', 'left_shoulder', 'left_elbow', 'left_hand', 
			  'right_shoulder', 'right_elbow', 'right_hand', 'torso', 'left_hip', 
			  'right_hip', 'left_knee', 'left_foot', 'right_knee', 'right_foot']


body_parts_dict = {	
	'head': 0, 
	'neck': 1,
	'left_shoulder':2,
	'left_elbow': 4,
	'left_hand': 6,
	'right_shoulder':3,
	'right_elbow': 5,
	'right_hand':7,
	'torso':8,
	'left_hip':9,
	'right_hip':10,
	'left_knee':11,
	'left_foot':13,
	'right_knee':12, 
	'right_foot', 14
}


####################################################[ UTILITIES ] ##################################################

# Function: print_error
# ---------------------
# prints an error then exits
def print_error (top_string, bottom_string):
	print "Error: " + top_string
	print "---------------------"
	print "	" + bottom_string
	exit ()




####################################################[ LOADING SKELETON ] ##################################################

# Function: make_skeleton_instance
# -------------------------
# loads all of the meme_types into self.meme_types 
def make_skeleton_instance(line):

	skeleton_instance = defaultdict(lambda: {'x':0.0, 'y':0.0, 'z':0.0})
	parsedString = line.split(",")
	if len(parsedString) != 46:
		print "line contains incorrect number of values; likely missing a body part."
		return

	num_per_body_part = 3
	count = 0
	for val in parsedString:
		if count==45: break
		axis = 'x'
		if count%3==1: axis = 'y'
		if count%3==2: axis = 'z'
		part = body_parts[count/3]
		skeleton_instance[body_parts[count/3]][axis] = float(val)
		count+=1
	skeleton_collection.append(skeleton_instance)



# Function: get_skeleton_timeseries
# ----------------------------
# given an open file, this will read in the next skeleton
def get_skeleton_timeseries (entire_file):

	### Step 1: get each section by itself ###
	sections = entire_file.split ("--- frame ---")

	for section in sections:

		#--- lines = list of all lines that have joint content ---
		lines = [line for line in section.split ('\n') if len (line) > 20]
		joints = {}
		for line in lines:
			splits = line.split (":,")
			index = int (splits[0])
			x = float(splits[1].strip())
			y = float(splits[2].strip())
			z = float(splits[3].strip())
			joints[index] = (x, y, z)
		print index, ": ", x, ", ", y, " ", z





defaultdict(lambda: 0.0)

# Function: read_in_skeleton_data
# -------------------------
# reads in a datafile containing skeleton coordinates 
def read_in_skeleton_data(filename):
	f = open(filename, 'r')
	#file is formatted poorly; only every other line contains data.
	count = 0
	for line in f:
		count+=1
		if count%2==0:
			continue
		make_skeleton_instance(line)



####################################################[ MANIPULATE DATA ] ##################################################

# Function: identity_manipulation
# -------------------------
# Simply copies values from skeleton_collection to manipulated_data
def identity_manipulation():
	for instance in skeleton_collection:
		manipulated_instance = defaultdict(lambda: {'x':0.0, 'y':0.0, 'z':0.0})
		for body_part in instance:
			for axis in instance[body_part]:
				manipulated_instance[body_part][axis] = instance[body_part][axis]
		manipulated_data.append(manipulated_instance)




def dotproduct(v1, v2):
	dotproduct = 0
	for axis in v1:
		dotproduct += v1[axis] * v2[axis]
  	return dotproduct

def length(v):
  return math.sqrt(dotproduct(v, v))

def calc_angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))

def manipulate_shit():
	min = 100
	max = 0
	for instance in skeleton_collection:
		forearm_vec = {'x': instance['left_hand']['x'] - instance['left_elbow']['x'],
					   'y': instance['left_hand']['y'] - instance['left_elbow']['y'],
					   'z': instance['left_hand']['z'] - instance['left_elbow']['z']}		
		bicep_vec = {'x': instance['left_shoulder']['x'] - instance['left_elbow']['x'],
					 'y': instance['left_shoulder']['y'] - instance['left_elbow']['y'],
					 'z': instance['left_shoulder']['z'] - instance['left_elbow']['z']}
		angle = calc_angle(forearm_vec, bicep_vec)
		if angle < min: min = angle
		if angle > max: max = angle
		print angle
	print "min: " + str(min)
	print "max: " + str(max)



####################################################[ WRITING DATA TO FILE] ##############################################

# Function: write_manipulation_to_file
# -------------------------
# outputs manipulated data to file for rendering
def write_manipulation_to_file(filename):
	f = open(filename, 'w')
	for instance in manipulated_data:
		for body_part in instance:
			line = instance[body_part]['x'] + ", " + instance[body_part]['y'] + ", " + instance[body_part]['z']
			f.write(line)
		f.write('\n')





####################################################[ PROGRAM OPERATION ]##################################################

if __name__ == "__main__":

	args = sys.argv;
	if len(args) != 3:
		print_error ("incorrect usage", "try ./SkeletonManipulation.py [operation name] [path to file]")


	read_in_skeleton_data(skeleton_source)

	#identity_manipulation()

	manipulate_shit()

	#write_manipulation_to_file(output_source)


