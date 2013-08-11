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
#include "VideoFrameRef_Wrapper.h"
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
	const char *skeleton_filename 	= filename_manager.get_filename (read_recording_stage, SKEL_FILE);
	skel_infile.open (skeleton_filename);
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
 	frame->write_skel (skel_outfile);

 	/*### Step 2: get/open the jvid file we are writing to ###*/
 	string next_jvid_filepath = get_next_jvid_filepath (write_recording_stage);
 	jvid_outfile.open (next_jvid_filepath.c_str(), ios::binary);

 	/*### Step 3: write the jvid and close it ###*/ 
 	frame->write_jvid (jvid_outfile);
 	jvid_outfile.close ();

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












