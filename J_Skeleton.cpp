/* ---------------------------------------------- 	*
 *	File: J_Skeleton.cpp
 *	--------------------
 *	My personal implementation of nite::Skeleton
 *
 *
 *	----------------------------------------------	*/

/*--- Standard ---*/
#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <stdio.h>
#include <map>
#include <vector>
#include <string>
#include <sstream>

/*--- NiTE ---*/
#include "NiTE.h"

/*--- My Files ---*/
#include "J_Skeleton.h"

/*--- Namespaces ---*/
using namespace std;




/*########################################################################################################################*/
/*###############################[--- Constructor/Destructors ---]########################################################*/
/*########################################################################################################################*/

/* Function: initialize_joints
 * ---------------------------
 * initializes joints (without a value) 
 */
void J_Skeleton::initialize () {

	/*### Step 1: initialize timestamp, pop ###*/
	beat 			= false;
	pop 			= false;
				
	/*### Step 2: initialize joints ###*/
	for (int i=0;i<JSKEL_NUM_OF_JOINTS;i++) {
		J_Joint * joint = new J_Joint (nite::Point3f (0, 0, 0), nite::Point3f(0, 0, 0), nite::Quaternion (0, 0, 0, 0));
		joints[i] = joint;
	}
}

/* Constructor: 
 * -----------------------------------------------
 * initializes via a map from nite::JoinType to J_Joints
 */
J_Skeleton::J_Skeleton () {
	/*### Step 1: initialize joints ###*/
	initialize ();
}


/* Constructor: nite::Skeleton
 * ---------------------------------
 * initializes via an nite::Skeleton
 */
J_Skeleton::J_Skeleton (nite::Skeleton *skeleton, nite::UserTracker *user_tracker) {

	/*### Step 1: initialize joints ###*/
	initialize ();

	/*### Step 1: set joint positions/orientations ###*/
	for (unsigned int i=0; i<JSKEL_NUM_OF_JOINTS;i++) {
		
		/*--- get position, position_absolute and orientation  ---*/
		nite::SkeletonJoint current_joint = skeleton->getJoint ((nite::JointType) i);
		nite::Point3f position = current_joint.getPosition ();
		nite::Point3f position_absolute = nite::Point3f (0, 0, 0);
		user_tracker->convertJointCoordinatesToDepth (position.x, position.y, position.z, &position_absolute.x, &position_absolute.y);
		nite::Quaternion orientation = current_joint.getOrientation ();

		/*--- set the joint's properties ---*/
		joints[i]->set (position, position_absolute, orientation);

	}

	is_valid = true;
	return;
}


/* Constructor: J_Skeleton *skeleton
 * ---------------------------------
 * initializes via a J_Skeleton (essentially a copy constructor)
 * if the skeleton passed in is null, this skeleton is set as not valid.
 */
J_Skeleton::J_Skeleton (J_Skeleton *skeleton) {

	/*### Step 1: initialize joints ###*/
	initialize ();

	if (skeleton == NULL) {
		is_valid = false;
		return;
	}
	else {

		/*### Step 1: initialize joints ###*/
		initialize ();

		/*### Step 1: set joint positions/orientations ###*/
		for (unsigned int i=0; i<JSKEL_NUM_OF_JOINTS;i++) {
			J_Joint *current_joint = skeleton->getJoint ((nite::JointType) i);
			joints[i]->set (current_joint);
		}
		is_valid = true;
		return;
	}
}
	


J_Skeleton::~J_Skeleton () {

	/*### Step 1: delete all memory allocated to the joints ###*/
	for (int i = 0;i<JSKEL_NUM_OF_JOINTS;i++) {
		delete joints[i];
	}
}




/*########################################################################################################################*/
/*###############################[--- Computing misc. properties ---]#####################################################*/
/*########################################################################################################################*/
/* Function: getBoundingBox
 * ------------------------
 * returns the convex hull (bounding box) of the current skeleton
 */
nite::BoundingBox J_Skeleton::getBoundingBox () {

	nite::Point3f top_left, bottom_right;

	top_left.x 		= 1000000;
	top_left.y 		= 1000000;
	bottom_right.x 	= 0;
	bottom_right.y	= 0;

	for (int i=0;i<JSKEL_NUM_OF_JOINTS;i++) {

		nite::Point3f position_absolute = joints[i]->getPositionAbsolute ();

		if (position_absolute.x < top_left.x) 		top_left.x = position_absolute.x;
		if (position_absolute.y < top_left.y) 		top_left.y = position_absolute.y;
		if (position_absolute.x > bottom_right.x) 	bottom_right.x = position_absolute.x;
		if (position_absolute.y > bottom_right.y) 	bottom_right.y = position_absolute.y;			

	}
	return nite::BoundingBox (top_left, bottom_right);
}













/*########################################################################################################################*/
/*###############################[--- Reading/Writing ---]################################################################*/
/*########################################################################################################################*/

// void J_Skeleton::read (ifstream& infile) {

// 	int beat_val, pop_val;
// 	string line;

// 	/*### Step 1: timestamp ###*/
// 	getline (infile, line);
// 	sscanf (line.c_str(), "##### %d #####\n", &timestamp);

// 	/*### Step 2: joints ###*/
// 	for (int i=0;i<JSKEL_NUM_OF_JOINTS;i++) {

// 		getline (infile, line);

// 		int joint_name;
// 		float x, y, z;

// 		sscanf (line.c_str(), "%d: (%f, %f, %f)\n", &joint_name, &x, &y, &z);
// 		setJointPosition ((nite::JointType) joint_name, nite::Point3f(x, y, z));
// 	}

// 	/*### Step 3: beat existence ###*/
// 	getline(infile, line);
// 	sscanf(line.c_str(), "----- beat: %d -----\n", &beat_val);
// 	setBeat ((beat_val == 1));

// 	/*### Step 4: pop existence ###*/
// 	getline (infile, line);
// 	sscanf (line.c_str(), "----- pop: %d -----\n", &pop_val);
// 	setPop ((pop_val == 1));

// 	/*### Step 5: get final line ###*/
// 	getline(infile, line);

// 	return;
// }














/*########################################################################################################################*/
/*###############################[--- Setters/Getters ---]################################################################*/
/*########################################################################################################################*/
/* Setter/Getter: validity
 * -----------------------
 * sets this skeleton as valid or otherwise
 */
void J_Skeleton::setValid (bool value) {
	is_valid = value;
}
bool J_Skeleton::isValid () {
	return is_valid;
}

/* Setter/Getter: get/set index
 * ----------------------------
 * gets/sets the timestamp
 */
 int J_Skeleton::getTimestamp () {
 	return timestamp;
 }
 void J_Skeleton::setTimestamp (int new_timestamp) {
 	timestamp = new_timestamp;
 }	

/* Setter/Getter: beat
 * ----------------------------
 * gets/sets the beat
 */
bool J_Skeleton::getBeat () {
 	return beat;
}
void J_Skeleton::setBeat (bool beat_value) {
 	beat = beat_value;
}	

/* Setter/Getter: pop
 * ------------------
 * gets/sets the beat
 */
bool J_Skeleton::getPop () {
 	return pop;
}
void J_Skeleton::setPop(bool pop_value) {
 	pop = pop_value;
}	


/* Setter/Getter: get/setJoint
 * ---------------------------
 * gets/sets a particular joint
 */
J_Joint *J_Skeleton::getJoint (nite::JointType joint_type) {
	return joints [(int) joint_type];
}
void J_Skeleton::setJointPosition (nite::JointType joint_type, nite::Point3f new_position) {
	joints[(int) joint_type]->setPosition(new_position);
	return;
}
void J_Skeleton::setJointOrientation (nite::JointType joint_type, nite::Quaternion new_orientation) {
	joints[(int) joint_type]->setOrientation(new_orientation);
	return;
}
















