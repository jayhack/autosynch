/* ---------------------------------------------- 	*
 *	File: J_StorageDelegate.cpp
 *	-----------------
 *	class that takes care of playing (and labelling)
 *	recordings, both unsynchronized and otherwise
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
#include "J_Frame.h"
#include "J_FilenameManager.h" 
#include "J_StorageDelegate.h"

/*--- Namespaces ---*/
using namespace std;


/*########################################################################################################################*/
/*###############################[--- Constructor/Initialization/Destructor ---] #########################################*/
/*########################################################################################################################*/

/* Function: Constructor
 * ---------------------
 * - initializes filename manager appropriately
 * 
 */
J_StorageDelegate::J_StorageDelegate () {}
J_StorageDelegate::J_StorageDelegate (	const char *selected_file_path, 		//filepath to the .sync directory
										int new_read_recording_stage,			//stage we will read from
										int new_write_recording_stage): 		//stage we will write to

										filename_manager (selected_file_path) 
{

	print_status ("Initialization", "Setting paramters");
	current_frame_number = 0;
	read_recording_stage = new_read_recording_stage;
	write_recording_stage = new_write_recording_stage;

	print_status ("Initialization", "Opening skeleton file(s)");
	const char *skeleton_infilename 	= filename_manager.get_filename (read_recording_stage, SKEL_FILE);
	const char *skeleton_outfilename	= filename_manager.get_filename (write_recording_stage, SKEL_FILE);
	cout << "		Skeleton infile: " << skeleton_infilename << endl;
	cout << "		Skeleton outfile: " << skeleton_outfilename << endl;
	skel_infile.open (skeleton_infilename);
	skel_outfile.open (skeleton_outfilename);
}
J_StorageDelegate::~J_StorageDelegate () {

	/*### Step 1: close all files we were reading from/writing to ###*/
	skel_infile.close ();
	skel_outfile.close ();

}





/*########################################################################################################################*/
/*###############################[--- Writing/Reading ---] ###############################################################*/
/*########################################################################################################################*/
/* Function: get_next_jvid_filepath
 * --------------------------------
 * determines where the next jvid file to read (write) to is,
 * given the recording stage we are reading from (writing to)
 */
string J_StorageDelegate::get_next_jvid_filepath (int recording_stage) {

	string jvid_directory;
	jvid_directory.assign(filename_manager.get_filename (recording_stage, JVID_FILE));

	stringstream next_jvid_filepath;
	next_jvid_filepath << jvid_directory << "/" << current_frame_number << ".j";
	return next_jvid_filepath.str();

}


/* Function: write_skeleton
 * ------------------------
 * writes the specified J_Skeleton to the .skel outfile.
 */
void J_StorageDelegate::write_skeleton (J_Skeleton * skeleton) {

	/*### Step 1: Skeleton id ###*/
	skel_outfile << "##### " << skeleton->getTimestamp () << " #####" << endl;

	/*### Step 2: if no skeleton exists, then get out of there ###*/
	if (!skeleton->isValid ()) {
		skel_outfile << "----- non-existant -----" << endl << endl;
		return;
	}
	else {

		/*### Step 2: joints ###*/
		for (int i=0;i<JSKEL_NUM_OF_JOINTS;i++) {
		
			J_Joint *current_joint = skeleton->getJoint ((nite::JointType) i);

			nite::Point3f position = current_joint->getPosition ();
			nite::Point3f position_absolute = current_joint->getPositionAbsolute ();

			skel_outfile << i << ": (" << position.x << ", " << position.y << ", " << position.z << ") | ";
			skel_outfile << 		"( " << position_absolute.x << ", " << position_absolute.y << ", " << position_absolute.z << ")" << endl;

		}

		bool beat = skeleton->getBeat ();
		bool pop = skeleton->getPop ();

		/*### Step 3: beat ###*/
		if (beat) 	skel_outfile << "----- beat: 1 -----" << endl;
		else 		skel_outfile << "----- beat: 0 -----" << endl;

		/*### Step 4: pop ###*/
		if (pop) 	skel_outfile << "----- pop: 1 -----" << endl;
		else 		skel_outfile << "----- pop: 0 -----" << endl;

		/*### Step 5: trailing newline ###*/
		skel_outfile << endl;
	}
}

/* Function: write_frame_ref
 * -------------------------
 * writes the specified J_VideoFrameRef to the .jvid file
 */
void J_StorageDelegate::write_frame_ref (J_VideoFrameRef *frame_ref) {

	/*### Step 1: open the outfile ###*/
	/*### NOTE: change this from just 'RAW' later on ###*/
	string filename = get_next_jvid_filepath (RAW); 
	cout << "writing to " << filename << endl;
	ofstream jvid_outfile;
	jvid_outfile.open (filename.c_str());

	/*### Step 3: write all the significant information into the file ###*/
	jvid_outfile << "resolution_x: "		<< frame_ref->getResolutionX () << endl;
	jvid_outfile << "resoution_y: " 		<< frame_ref->getResolutionY () << endl;
	jvid_outfile << "crop_origin_x: " 		<< frame_ref->getCropOriginX () << endl;
	jvid_outfile << "crop_origin_y: " 		<< frame_ref->getCropOriginY () << endl;
	jvid_outfile << "data_size: " 			<< frame_ref->getDataSize () << endl;
	jvid_outfile << "frame_index: " 		<< frame_ref->getFrameIndex () << endl;
	jvid_outfile << "height: " << frame_ref->getHeight () << endl;
	jvid_outfile << "width: " << frame_ref->getWidth () << endl;
	jvid_outfile << "stride_in_bytes: " << frame_ref->getStrideInBytes () << endl;
	jvid_outfile << "timestamp: " << frame_ref->getTimestamp () << endl;
	jvid_outfile << "is_valid: " << frame_ref->isValid () << endl;

	/*### Step 4: write the data ###*/
	jvid_outfile << "---------- DATA ----------" << endl;
	jvid_outfile.write(frame_ref->getData(), frame_ref->getDataSize());
	jvid_outfile.close ();
	return;
}


/* Function: write_frame 
 * ---------------------
 * given a pointer to a J_Frame object, this function will write it
 * to a file
 */
void J_StorageDelegate::write_frame (J_Frame *frame) {

	/*### Step 0: assert that the frame is in fact valid ###*/
	if (!frame->isValid ()) {
		print_error ("J_StorateDelegate::write_frame error", "you passed in an invalid J_Frame");
	}

 	/*### Step 1: write the skeleton ###*/
 	print_status ("Storage", "Writing J_Skeleton");
 	write_skeleton (frame->get_skeleton());

 	/*### Step 2: write the frame_ref ###*/
 	print_status ("Storage", "Writing J_VideoFrameRef");
 	write_frame_ref (frame->get_frame_ref());
 }



/* Function: read_frame 
 * ---------------------
 * given a pointer to a J_Frame object, this function will write it
 * to a file
 */
void J_StorageDelegate::read_frame (J_Frame *frame) {

	/*### Step 0: assert that the frame passed in is not valid ###*/
	if (frame->isValid ()) {
		print_error ("J_StorateDelegate::read_frame error", "you passed in an already valid J_Frame");
	}

 	// /*### Step 1: write the skeleton ###*/
 	// frame->write_skeleton (skel_outfile);

 	// /*### Step 2: get/open the jvid file we are writing to ###*/
 	// string next_jvid_filepath = get_next_jvid_filepath (write_recording_stage);
 	// jvid_outfile.open (next_jvid_filepath.c_str());

 	// /*### Step 3: write the jvid and close it ###*/ 
 	// frame->write_jvid (jvid_outfile);
 	// jvid_outfile.close ();

 }












