/* ---------------------------------------------- 	*
 *	File: J_Frame.cpp
 *	-----------------
 *	Class that contains everything for dealing with 
 * 	a single "frame" from a video, including a J_Skeleton
 *	and a VideoFrameRef
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
#include <unistd.h>

/*--- NiTE ---*/
#include "NiTE.h"

/*--- My Files ---*/
#include "Utilities.h"
#include "J_Skeleton.h"
#include "VideoFrameRef_Wrapper.h"
#include "J_Frame.h"

 /*--- Namespaces ---*/
 using namespace std;
 using namespace openni;


/*########################################################################################################################*/
/*###############################[--- Constructor/Initialization/Destructor ---] #########################################*/
/*########################################################################################################################*/
/* : Constructor 
 * ---------------------
 * fills out all of the data in this J_Frame
 */
J_Frame::J_Frame () {

	is_valid = false;
 }
J_Frame::J_Frame 	(	J_Skeleton *new_skeleton, 
						VideoFrameRef *new_frame_ref,
						int new_frame_index):			

						/*--- member initializers ---*/
						skeleton (new_skeleton), 
						frame_ref (new_frame_ref) 
{
	cout << "HERE" << endl;
	frame_index = new_frame_index;
	is_valid = true;
}

/* Function: isValid
 * -----------------
 * returns true if this J_Frame contains actual data
 */
bool J_Frame::isValid () {
	return is_valid;
}


/*########################################################################################################################*/
/*###############################[--- Getters ---] #######################################################################*/
/*########################################################################################################################*/
J_Skeleton  *		J_Frame::get_skeleton 	() {

	return &skeleton;
}

J_VideoFrameRef * 	J_Frame::get_frame_ref 	() {
	return &frame_ref;
}




/*########################################################################################################################*/
/*###############################[--- Writing ---] #######################################################################*/
/*########################################################################################################################*/
/* Function: write_skeleton
 * ------------------------
 * writes the skeleton to the outfile
 */
void J_Frame::write_skel (ofstream &outfile) {

	skeleton.write (outfile);
}

/* Function: write_jvid
 * --------------------
 * writes the jvid to the outfile
 */
void J_Frame::write_jvid (ofstream &outfile) {
	// frame_ref.write (outfile);
	cout << "not implemented yet" << endl;
}

/*########################################################################################################################*/
/*###############################[--- Debugging ---] #######################################################################*/
/*########################################################################################################################*/
/* Function: print_data
 * --------------------
 * prints out data on the currently observed skeletons
 */
void J_Frame::print_data () {

	cout << "#####[ --- FRAME: --- ]#####" << endl;

	/*### Step 1: loop through all the joints and print out their locations ###*/
	if (!skeleton.isValid ()) {
		cout << ">> NO USERS DETECTED <<" << endl;
	}
	else {
		for (int i=0;i<JSKEL_NUM_OF_JOINTS;i++) {

			nite::Point3f position = skeleton.getJoint((nite::JointType) i)->getPosition();
			cout << i << ": " << position.x << ", " << position.y << ", " << position.z << endl;
		}
	}

}










