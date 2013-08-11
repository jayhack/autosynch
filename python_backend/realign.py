#!/usr/bin/python
import os
import sys
import process_data
import pickle
from process_data import Skeleton

classifier_name = "classifiers/toprock_classifier_all.obj"
important_body_parts = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

class Realign:

	#--- globals ---
	skeletons = None
	pop_indexes = None
	classifier = None

	# list of beat indexes
	beat_indexes = []

	# tuples of beat index
	beats = []

	# tuples of (pop, beat) that need to be realigned
	realignments = []

	# contains the final indexes...
	final_indexes = []

	fd_interval = 6
	sd_interval = 6

	pos = []
	fd = []
	sd = []


	# Function: constructor
	# ---------------------
	# initializes the list of skeletons
	def __init__ (self, analyze_file):


		self.classifier = pickle.load (open(classifier_name, 'rb'))

		self.get_skeleton_timeseries (open(analyze_file, 'r').read())
		self.joints = [s.joints for s in self.skeletons]
		#--- remove the first like 50 examples ---
		# skeletons 	= skeletons[50:]
	
		total_distance = float(self.beat_indexes[-1] - self.beat_indexes[0])
		average_distance = total_distance / float(len(self.beat_indexes) - 1)

		# print "total_distance = ", total_distance
		# print "average_distance = ", int(average_distance + 1)

		### fill in the missing beat indexes ###
		for i in range (self.beat_indexes[-1], len(self.skeletons)):
			if (i - self.beat_indexes[-1]) % int(average_distance) == 0:
				self.beat_indexes.append (i)

		self.beat_indexes = sorted(list(set(self.beat_indexes)))

		remove_beats = []
		for index in range (len(self.beat_indexes) - 1):
			if (self.beat_indexes[index + 1] - self.beat_indexes[index]) < 5:
				remove_beats.append (self.beat_indexes[index])	
		for beat in remove_beats:
			self.beat_indexes.remove (beat);



		fd_interval = 6
		sd_interval = 6

		first_derivatives_raw =	self.get_derivatives 	(self.joints, self.fd_interval)
		second_derivatives_raw = self.get_derivatives 	(first_derivatives_raw, self.sd_interval)

		### --- Note: these are shifted by sd_interval + fd_interval ---###
		self.pos 	= self.joints  [sd_interval + fd_interval:]
		self.fd 	= first_derivatives_raw [sd_interval:]
		self.sd 	= second_derivatives_raw


		### get a feature vector representation for each skeleton ###
		self.get_feature_reps ()

		### find the interval for each beat in which we will look ###
		self.get_intervals ()

		### self.realignments will contain (pop, beat) pairs
		self.realignments = []
		for i in range (len(self.beats)):
			best_index = self.get_pop_index (i)
			self.realignments.append ((best_index, self.beats[i][0]))

		# print self.realignments



	# Function: extract_features
	# --------------------------
	# for SVM - returns a list of features
	def extract_features (self, pos, fd, sd):

		#### make sure they are all the right size ###
		if len(pos) != 15 or len(fd) != 15 or len(sd) != 15:
			return None

		features = []

		un = set(important_body_parts).union(pos.keys())

		for key in un:
			features.append (pos[key][0])
			features.append (pos[key][1])
			features.append (pos[key][2])


		un = set(important_body_parts).union(fd.keys())		
		for key in un:
			features.append (fd[key][0])
			features.append (fd[key][1])
			features.append (fd[key][2])


		if len(features) != 30*3:
			return None
		else:
			return features




	# Function: get_feature_reps
	# --------------------------
	# returns a list of feature vectors, with the ith one corresponding to
	# the ith 'skeleton' or frame (i.e. you add 12 to it.)
	def get_feature_reps (self):
		
		if len (self.pos) != len(self.fd) or len (self.fd) != len(self.sd):
			print "ERROR!!! the lengths are wrong"
			exit ()

		### initialize it with 12 of nothing... ###
		self.feature_reps = [[] for x in range(self.fd_interval + self.sd_interval)]

		### fill it with a feature rep for each skeleton ###
		for index in range (len(self.pos)):

			feature_vector = self.extract_features (self.pos[index], self.fd[index], self.sd[index])
			self.feature_reps.append (feature_vector)

		if len(self.feature_reps) != len (self.skeletons):
			print "Error: something got fucked up here"
			exit ()




	# Function: get_derivatives
	# -------------------------------
	# given a list of all skeletons, this returns a list of first derivatives
	# derivative_length: the number of elements back you go in order to get the deriv
	# - NOTE: framerate for this bitch is apparently 30 frames/second
	def get_derivatives (self, entries, derivative_length):

		cur_index = derivative_length
		prev_index = 0
		considering_entries = entries[cur_index:]

		first_derivatives = []

		prev = entries[prev_index]
		for cur in considering_entries:
			fd = {}
			for i in cur.keys():

				deriv = ((cur[i][0] - prev[i][0]), (cur[i][1] - prev[i][1]), (cur[i][2] - prev[i][2]))
				fd[i] = deriv

			prev_index += 1
			prev = entries[prev_index]
			first_derivatives.append (fd)

		return first_derivatives



	# Function: get_skeleton_timeseries
	# ---------------------------------
	# gets us our skeletons and the beats
	def get_skeleton_timeseries (self, entire_file):

		self.skeletons = []

		### Step 1: get each section by itself ###
		sections = [s for s in entire_file.split ("--- frame ---") if len(s) > 5]

		self.beat_indexes = []
		i = 0
		for section in sections:
			beat_occurred = False

			#--- lines = list of all lines that have joint content ---
			lines = [line for line in section.split ('\n') if len(line) > 5]
			#check if this section has a positive example...
			remove_lines = []
			for line in lines:

				if line[0] == 'b' and '1' in line:
					beat_occurred = True
				else:
					beat_occurred = False

				if line[0] == 'b':
					remove_lines.append (line)

			for remove_line in remove_lines:
				lines.remove(remove_line)
			if beat_occurred:
				self.beat_indexes.append (i)

			joints = {}
			for line in lines:

				splits = line.split (":")
				
				index = int(splits[0])
				rest = splits[1]
				splits = rest.split(',')
				x = float (splits[0])
				y = float (splits[1])
				z = float (splits[2])

				joints[index] = (x, y, z)	
			i += 1

			new_skeleton = Skeleton(joints, False)
			self.skeletons.append (new_skeleton)




	# Function: get_interval
	# ----------------------
	# returns a tuple, the time-slice that we will look into for realignment
	def get_interval (self, current):

		start 	= 	self.beat_indexes[current] - 0.33333*(self.beat_indexes[current] - self.beat_indexes[current - 1])
		end   	= 	self.beat_indexes[current] + 0.33333*(self.beat_indexes[current + 1] - self.beat_indexes[current ])
		return (int(start), int(end))


	# Function: uniform_realign
	# -----------------------
	# this function will uniformly realign the recording
	def get_intervals (self):

		#--- first beat index ---
		for index in range(1, len(self.beat_indexes) - 1):

			(start, end) = self.get_interval (index);
			self.beats.append ((self.beat_indexes[index], (start, end)))



	# Function: get_pop
	# -----------------
	# finds the pop within a given interval - returns its index
	def get_pop_index (self, beat_number):

		(start, end) = self.beats[beat_number][1]

		interval = range(start, end)

		best_prob = -100
		best_index = -1
		for t in interval:

			# print t, ": ",
			### corresponds to the t'th skeleton ###
			feature_vector = self.feature_reps[t]

			prediction = self.classifier.predict_proba (feature_vector)
			p_of_pop = prediction[0][1]
			# print p_of_pop
			if p_of_pop > best_prob:
				# print "			-"
				best_prob = p_of_pop
				best_index = t

		return best_index





########################################################################################################################
#############################[ --- REALIGNMENT ALGORITHM ---] ##########################################################
########################################################################################################################
	# Function: realign
	# -----------------
	# returns a list of indeces which is the final sequence that will be played
	def get_realignment (self):

		self.final_indexes = []

		### all data is in realignments ###
		beats = [r[1] for r in self.realignments]
		pops = [r[0] for r in self.realignments]

		prev_beat = beats[0]
		prev_pop = pops[0]
		current_index = 1
		for beat in beats[:-1]:

			### get distances ###
			beat_dist = beats[current_index] - prev_beat
			pop_dist = pops[current_index] - prev_pop



			for frame_ind in range(beat_dist):
				ind = prev_pop + (float(frame_ind) / float(beat_dist)) * pop_dist
				self.final_indexes.append(int(ind))

			### udpate iterators ###
			prev_beat = beats[current_index]
			prev_pop = pops[current_index]
			current_index += 1

		print len(self.final_indexes)
		print len(self.skeletons)


	# Function: print_realignment
	# ---------------------------
	# prints the new skeleton to a file.
	def print_realignment (self):

		for i in range(len(self.final_indexes)):
			index = self.final_indexes[i]
			print self.skeletons[index]
			if i in set(self.beat_indexes):
				print "beat_exists: 1\n"
			else:
				print "beat_exists: 0\n"





if __name__ == "__main__":

	realign = Realign ('Data/toprock/testing/labelled.txt')
	realign.get_realignment ()
	realign.print_realignment ()









