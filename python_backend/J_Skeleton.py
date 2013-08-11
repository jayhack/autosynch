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
	timestamp = -1		#time at which this skeleton originally occurred

	#--- joints positions ---
	joints = None		#dict mapping joint_name to J_Joint objects

	#--- first derivatives of joint position ---
	fd_1 = None			# first derivatives of joint motion (over a smaller interval)
	fd_2 = None			# first derivatives of joint motion (over a larger interval)

	#--- second derivatives of joint position ---
	sd_1 = None			#second derivatives of joint motion (over a smaller interval)
	sd_2 = None			#second derivatives of joint motion (over a larger interval)

	beat = False			#wether a beat occurred or not
	pop = False				#wether a pop occurred or not
	pop_probability = 0.0	#p(pop|feature_vector), as computed by the classifier



	# Function: Constructor
	# ---------------------
	# initializes with timestamp and joints
	def __init__ (self, timestamp, joints, beat=False, pop=False):

		#--- timestamp ---
		self.timestamp = timestamp

		#--- joints ---
		self.joints = joints

		#--- beat ----
		self.beat = beat

		#--- pop ---
		self.pop = pop



	# Function: String Representation
	# -------------------------------
	# returns a string representation of this object
	def __str__ (self):
		all_strings = []

		#--- timestamp ---
		all_strings.append("##### " + str(self.timestamp) + " #####")

		#--- joints ---
		for joint_name in self.joints.keys():
			all_strings.append (self.joints[joint_name].__str__())

		#--- beat ---
		if self.beat:
			all_strings.append ("----- beat: " + str(1) + " -----")
		else:
			all_strings.append ("----- beat: " + str(0) + " -----")

		#--- pop ---
		if self.pop:
			all_strings.append ("----- pop: " + str(1) + " -----")
		else:
			all_strings.append ("----- pop: " + str(0) + " -----")

		return '\n'.join(all_strings) + '\n\n'

	
	# Function: json 
	# -----------------------
	# returns a form that can be dumped to json
	def json (self):

		name_json = 'Skeleton_' + str(self.timestamp)
		joints_json	= dict (j.json() for j in self.joints.values())
		return {name_json:joints_json}



	# Function: get_feature_vector
	# ------------------------
	# returns a feature vector representation of this skeleton
	# Note: call this only after setting fd and sd
	def get_feature_vector (self):
		
		features = []

		for joint in self.joints.values ():
			features.append (joint.x)
			features.append (joint.y)
			features.append (joint.z)

		for deriv in self.fd_1.values ():
			features.append (deriv.x)
			features.append (deriv.y)
			features.append (deriv.z)

		for deriv in self.fd_2.values ():
			features.append (deriv.x)
			features.append (deriv.y)
			features.append (deriv.z)	
	
		for deriv in self.sd_1.values ():
			features.append (deriv.x)
			features.append (deriv.y)
			features.append (deriv.z)

		for deriv in self.sd_1.values ():
			features.append (deriv.x)
			features.append (deriv.y)
			features.append (deriv.z)

		return features


	# Function: get_label
	# -------------------
	# returns the label of this skeleton
	def get_label (self):

		return self.pop




















