/*******************************************************************************
*                                                                              *
*   PrimeSense NiTE 2.0 - User Viewer Sample                                   *
*   Copyright (C) 2012 PrimeSense Ltd.                                         *
*                                                                              *
*******************************************************************************/

/*--- Standard ---*/
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

/*--- My Files ---*/
#include "Utilities.h"
#include "J_StorageDelegate.h"
#include "NI_Recorder.h"
#include "NI_Player.h"


/*--- Namespaces ---*/
using namespace std;


int main(int argc, char** argv)
{


	/*### Step 1: make sure the arguments are correct ###*/
	if (argc != 3) print_error ("Incorrect usage", "try ./ (record|play|mark) [.sync filename, without .sync]");
	char *mode_string 	= argv[1];
	char *file_path		= argv[2];	


	// /*### For recording ###*/
	// print_status ("MAIN", "Beginning Initializion of ni_recorder");
	// NI_Recorder ni_recorder (file_path, argc, argv);
	// print_status ("MAIN", "Finished initializion of ni_recorder");
	// ni_recorder.Run ();

	/*### For playing ###*/
	print_status ("MAIN", "Beginning Initialization of ni_player");
	NI_Player ni_player (file_path, argc, argv);
	ni_player.Run ();

	// /*### Step 2: intialize apis ###*/
	// initialize_apis ();

	// /*### Step 3: get the storage delgate ###*/
	// J_StorageDelegate storage_delegate (file_path);

	// /*### Step 4: get the drawer... ###*/
	// //gotta do something here...

	// /*###[ --- RECORD MODE --- ]###*/
	// if (mode == RECORD) {

	// 	/*### Step 1: set up the device ###*/
	// 	print_status ("Setup", "Initializing device")
	// 	rc = primesense.open(uri);
	// 	if ( (rc != openni::STATUS_OK) || (!primesense.isValid ())) {
	// 		print_error ("Failed to open device", openni::OpenNI::getExtendedError());


	// 		/*### Step 2: set up the user tracker ###*/
	// 		print_status ("Setup", "Initializing user tracker");
	// 		if (user_tracker.create(primesense) != nite::STATUS_OK) {
	// 			print_error ("Could not create the user tracker", "Not sure what to do here...");
	// 		}


	// 	}



	// }




	// /*###[ --- PLAY MODE --- ]###*/
	// if (mode == PLAY) {

	// 	/*### Step 1: get the next frame 


	// }


	// /*### Step 1: get the mode ###*/
	// char * mode_arg = argv[1];
	// int mode = -1;
	// if 		(strcmp (mode_arg, "record")	== 0) 	mode = RECORD_MODE;
	// else if (strcmp (mode_arg, "play") 		== 0) 	mode = PLAY_MODE;
	// else 											print_error ("entered mode not recognized", "try (play|record)");

	// if (mode == RECORD_MODE) {
	// 	print_status("Main", "Starting record mode");
	// 	if (argc != 4) print_error ("incorrect usage", "try ./[program name] record [skeleton_filename] [video_filename]");
	// 	char *skeleton_outfilename = argv[2];
	// 	char *video_outfilename = argv[3];
	// 	char *skeleton_infilename = argv[2];
	// 	NI_app ni_app ("Dance Autosynchronization Recorder", mode, skeleton_infilename, skeleton_outfilename, video_outfilename, argc, argv);
	// 	ni_app.Run ();
	// }
	// else {
	// 	print_status("Main", "Starting play mode");
	// 	if (argc != 5) print_error ("incorrect usage", "try ./[program name] play [skeleton_infilename] [skeleton_outfilename] [video_filename]");		
	// 	char *skeleton_infilename = argv[2];
	// 	char *skeleton_outfilename = argv[3];
	// 	char *video_infilename = argv[4];
	// 	NI_app ni_app ("Dance Autosynchronization Player", mode, skeleton_infilename, skeleton_outfilename, video_infilename, argc, argv);
	// 	ni_app.Run();
	// }

	return 0;
}







