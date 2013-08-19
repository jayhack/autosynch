#!/usr/bin/python
# ---------------------------------------------------------- #
# Script: train_classifier.py
# ---------------------------
# trains the 'pop' classifier
#
#
# ---------------------------------------------------------- #
import sys
import os
import math
import random
import pickle

#--- ML ---
from sklearn.linear_model import LogisticRegression

#--- my files ---
from common_utilities import print_error, print_status
from J_Joint import J_Joint
from J_Skeleton import J_Skeleton
from read_write import read_in_skeletons, write_out_skeletons 
from add_derivatives import Derivative, add_derivatives_to_skeletons


class Trainer:

	#--- Data ---
	skeletons_raw = None
	skeletons_with_derivs = None

	#--- Parameters for 1st/2nd deriv ---
	fd_interval_1 = 5
	fd_interval_2 = 10
	sd_interval_1 = 5
	sd_interval_2 = 10

	#--- Classifier ---
	classifier = None


	# Function: constructor
	# ---------------------
	# loads in all of the skeletons
	def __init__ (self, jvid_filename, recording_name, classifier_name=None, save=True, test=False):

		print_status ("Trainer", "Starting")

		### Step 1: get in the original skeletons ###
		self.skeletons_raw = read_in_skeletons (jvid_filename)

		### Step 2: add derivatives to them (fills skeletons_with_derivs) ###
		self.skeletons_with_derivs = add_derivatives_to_skeletons (self.skeletons_raw, self.fd_interval_1, self.fd_interval_2, self.fd_interval_1, self.fd_interval_2)

		### Step 3: put it into training data form ###
		(X, Y) = self.get_training_data ()

		### Step 4: get it in training data form ###
		all_data = zip(X, Y)
		print "	### Number of examples: ", len(all_data)
		random.shuffle (all_data);

		training = all_data
		# training = all_data[:5000]
		# testing = all_data[5000:]
		#--- training ---
		X_train = [t[0] for t in training]
		Y_train = [t[1] for t in training]
		#--- testing ---
		# X_test = [t[0] for t in testing]
		# Y_test = [t[1] for t in testing]



		#--- get the classifier ---
		print_status ("Trainer", "Training the classifier")
		self.classifier = LogisticRegression().fit(X_train, Y_train)


		#--- saving data ----
		if save:
			if classifier_name == None:
				classifier_name = recording_name.split('.')[0] + '.obj'
				classifier_name = os.path.join (os.getcwd (), 'python_backend/classifiers', classifier_name)
			print_status ("Trainer", "Pickling the classifier at " + classifier_name)
			self.save_classifier (classifier_name)

		#--- testing ---
		# if test:
			# print_status ("Trainer", "Evaluating classifier")
			# self.evaluate_classifier (classifier, X_test, Y_test)




	# Function: get_training_examples 
	# -------------------------------
	# given position/all derivatives, this returns a tuple of positive/negative examples.
	def get_training_data (self):

		examples = []
		labels = []
		for skeleton in self.skeletons_with_derivs:

			examples.append (skeleton.get_feature_vector ())
			labels.append (skeleton.getBeat ())

		return (examples, labels)



	# Function: load_classifier
	# -------------------------
	# loads the classifier from a pickled file
	def load_classifier (self, filename):
		
		return pickle.load (open(filename, 'rb'))


	# Function: save_classifier
	# -------------------------
	# save the classifier to a pickled file
	def save_classifier (self, filename):

		return pickle.dump (self.classifier, open(filename, 'wb'))


	# Function: evaluate_classifier
	# -----------------------------
	# evaluates the classifier...
	def evaluate_classifier (classifier, X, Y):

		hits = 0
		misses = 0

		total_prob_true = 0.0
		total_prob_false = 0.0
		num_true = 0
		num_false = 0

		for i in range (len(X)):

			example = X[i]
			true_label = Y[i]

			prediction = classifier.predict (example)


			prediction_prob = classifier.predict_proba (example)
			p_of_pop = prediction_prob[0][1]


			if prediction == true_label:
				hits += 1
			else:
				misses += 1

			# print "true_label | prediction: ", true_label, " | ", prediction


			prediction_prob = classifier.predict_proba (example)
			print "true_label | prediction: ", true_label, " | ", prediction_prob, " | ", prediction

		print "--- RESULTS ---"
		print 'hits: ', hits
		print 'misses: ', misses
		print 'accuracy: ', float(hits)/float(hits+misses)




if __name__ == "__main__":

	print_status ("Train Classifier", "Starting")

	### Step 1: manage args ###
	if len(sys.argv) < 3:
		print_error ("Not enough args", "Usage: ./train_classifier.py [infile] [classifier_name] [(load|save|test)]")
	infile_name 	= sys.argv[1]
	classifier_name	= sys.argv[2]
	if 'load' in sys.argv:
		load = True
	else:
		load = False
	if 'save' in sys.argv:
		save = True
	else:
		save = False
	if 'test' in sys.argv:
		test = True
	else:
		test = False


	### Step 2: read in the skeleton timeseries and add derivatives to them ###
	skeletons = read_in_skeletons (infile_name)
	fd_interval_1 = 5
	fd_interval_2 = 10
	sd_interval_1 = 5
	sd_interval_2 = 10
	skeletons = add_derivatives_to_skeletons (skeletons, fd_interval_1, fd_interval_2, sd_interval_1, sd_interval_2)

	### Step 3: put it into training data form ###
	(X, Y) = get_training_data (skeletons)

	### Step 4: get it in training data form ###
	all_data = zip(X, Y)
	print "	### Number of examples: ", len(all_data)
	random.shuffle (all_data);

	training = all_data
	# training = all_data[:5000]
	# testing = all_data[5000:]
	#--- training ---
	X_train = [t[0] for t in training]
	Y_train = [t[1] for t in training]
	#--- testing ---
	# X_test = [t[0] for t in testing]
	# Y_test = [t[1] for t in testing]



	#--- get the classifier ---
	classifier = None
	if load:
		print "---> Status: loading classifier"
		classifier = load_classifier (classifier_name)
	else:
		print "---> Status: training classifier"
		classifier = LogisticRegression().fit(X_train, Y_train)


	#--- saving data ----
	if save:
		print "---> Status: pickling classifier"
		save_classifier (classifier, classifier_name)

	# #--- testing ---
	if test:
		print "---> Status: evaluating"
		evaluate_classifier (classifier, X_test, Y_test)









