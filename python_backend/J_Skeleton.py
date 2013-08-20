# ---------------------------------------------------------- #
# Script: J_Skeleton.py
# ---------------------
# Class containing all data relevant to a single skeleton 
#
#
#
#
# ---------------------------------------------------------- #
from J_Joint import J_Joint

class J_Skeleton:

	#--- properties ---
	read_index = -1
	original_index = -1
	exists = False
	beat = 0
	pop = 0
	pop_probability = 0.0

	#--- joints positions ---
	joints = None		#dict mapping joint_name to J_Joint objects

	#--- first derivatives of joint position ---
	fd_1 = None			# first derivatives of joint motion (over a smaller interval)
	fd_2 = None			# first derivatives of joint motion (over a larger interval)

	#--- second derivatives of joint position ---
	sd_1 = None			#second derivatives of joint motion (over a smaller interval)
	sd_2 = None			#second derivatives of joint motion (over a larger interval)



	# Function: Constructor
	# ---------------------
	# initializes with timestamp and joints
	def __init__ (self, read_index, original_index, exists, beat, pop, joints):

		#--- index ---
		self.read_index = read_index
		self.original_index = original_index
		self.exists = exists
		self.beat = beat
		self.pop = pop
		self.joints = joints


	# Function: setters/getters
	# -------------------------
	# setters/getters for beat/pop
	def setBeat (self, value):
		self.beat = value
	def setPop (self, value):
		self.pop = value
	def getBeat (self):
		return self.beat
	def getPop (self):
		return self.pop



	# Function: String Representation
	# -------------------------------
	# returns a string representation of this object
	def __str__ (self):
		all_strings = []

		#--- timestamp ---
		all_strings.append(str(self.original_index))
		if self.exists == 0:
			all_strings.append (str(0))
		else:
			all_strings.append (str(1))

			if self.beat == True or self.beat == 1:
				all_strings.append ('1')
			else:
				all_strings.append ('0')

			if self.pop == True or self.pop == 1:
				all_strings.append ('1')
			else:
				all_strings.append ('0')


			for i in range(15):
				current_joint = self.joints[i]
				joint_list = [current_joint.x, current_joint.y, current_joint.z, current_joint.x_abs, current_joint.y_abs, current_joint.z_abs]
				joint_list = [str(l) for l in joint_list]
				joint_string = ", ".join(joint_list)

				all_strings.append (joint_string)

		return '\n'.join(all_strings)


	# Function: get_feature_vector
	# ------------------------
	# returns a feature vector representation of this skeleton
	# Note: call this only after setting fd and sd
	def get_feature_vector (self):
		
		features = []

		### absolute position of all the joints ###
		# for joint in self.joints.values ():
			# features.append (joint.x)
			# features.append (joint.y)
			# features.append (joint.z)

		#########################################################
		########[ --- 1st/2nd Derivatives ---]###################
		#########################################################

		for deriv in self.fd_1.values ():
			features.append (abs(deriv.x))
			features.append (abs(deriv.y))
			features.append (abs(deriv.z))

		# for deriv in self.fd_2.values ():
			# features.append (abs(deriv.x))
			# features.append (abs(deriv.y))
			# features.append (abs(deriv.z))
	
		# for deriv in self.sd_1.values ():
			# features.append (deriv.x)
			# features.append (deriv.y)
			# features.append (deriv.z)

		# for deriv in self.sd_2.values ():
			# features.append (deriv.x)
			# features.append (deriv.y)
			# features.append (deriv.z)


		#########################################################
		########[ --- Relative Positions ---]####################
		#########################################################
		left_shoulder = self.joints[2]
		right_shoulder = self.joints[3]
		left_elbow = self.joints[4]
		right_elbow = self.joints[5]
		left_hand = self.joints[6]
		right_hand = self.joints[7]
		torso = self.joints[8]
		left_hip = self.joints [9]
		right_hip = self.joints [10]
		left_knee = self.joints [11]
		right_knee = self.joints[12]
		left_foot = self.joints[13]
		right_foot = self.joints[14]

		# #--- upper body: diff between elbow/shoulder ---
		features.append ((left_shoulder.x - left_elbow.x))
		features.append ((left_shoulder.y - left_elbow.y))
		features.append ((left_shoulder.z - left_elbow.z))
		features.append ((right_shoulder.x - right_elbow.x))
		features.append ((right_shoulder.y - right_elbow.y))		
		features.append ((right_shoulder.z - right_elbow.z))

		# #--- upper body: diff between right/left hand ---
		features.append ((left_hand.x - right_hand.x))
		features.append ((left_hand.y - right_hand.y))
		features.append ((left_hand.z - right_hand.z))

		# #--- upper body: diff between right/left elbow ---
		features.append ((left_elbow.x - right_elbow.x))
		features.append ((left_elbow.y - right_elbow.y))
		features.append ((left_elbow.z - right_elbow.z))		

		# #--- upper body: diff between hand/elbow ---
		features.append ((left_elbow.x - left_hand.x))
		features.append ((left_elbow.y - left_hand.y))
		features.append ((left_elbow.z - left_hand.z))
		features.append ((right_elbow.x - right_hand.x))
		features.append ((right_elbow.y - right_hand.y))
		features.append ((right_elbow.z - right_hand.z))			



		#--- lower body: diff between hip/knee ---
		features.append ((left_hip.x - left_knee.x))
		features.append ((left_hip.y - left_knee.y))
		features.append ((left_hip.z - left_knee.z))			
		features.append ((right_hip.x - right_knee.x))
		features.append ((right_hip.y - right_knee.y))
		features.append ((right_hip.z - right_knee.z))						

		#--- lower body: diff between knee/foot ---
		features.append ((left_knee.x - left_foot.x))
		features.append ((left_knee.y - left_foot.y))
		features.append ((left_knee.z - left_foot.z))			
		features.append ((right_knee.x - right_foot.x))
		features.append ((right_knee.y - right_foot.y))
		features.append ((right_knee.z - right_foot.z))

		#--- lower body: diff between right/left knee ---
		features.append ((left_knee.x - right_knee.x))
		features.append ((left_knee.y - right_knee.y))
		features.append ((left_knee.z - right_knee.z))			

		#--- lower body: diff between right/left foot ---
		features.append ((left_foot.x - right_foot.x))
		features.append ((left_foot.y - right_foot.y))
		features.append ((left_foot.z - right_foot.z))					


		return features



















