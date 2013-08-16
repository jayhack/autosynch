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
	if (argc != 3) print_error ("Incorrect usage", "try ./ (record|observe_raw|observe_marked|observe_synced) [.sync filename, without .sync]");
	char *mode_string 	= argv[1];
	char *file_path		= argv[2];


	int mode = 0;

	if (strcmp (mode_string, "record") == 0) {
		print_status ("MAIN", "Beginning Initializion of ni_recorder");
		NI_Recorder ni_recorder (file_path, argc, argv);
		print_status ("MAIN", "Finished initializion of ni_recorder");
		ni_recorder.Run ();
	}
	else {
		int mode = -1;
		if 			(strcmp (mode_string, "observe_raw") == 0)		mode = OBSERVE_RAW_MODE;
		else if 	(strcmp (mode_string, "observe_marked") == 0) 	mode = OBSERVE_MARKED_MODE;
		else if 	(strcmp (mode_string, "observe_synced") == 0) 	mode = OBSERVE_SYNCHRONIZED_MODE;
		else 		print_error ("MAIN", "Could not parse the mode you entered");

		print_status ("MAIN", "Beginning Initialization of ni_player");
		NI_Player ni_player (file_path, mode, argc, argv);
		print_status ("MAIN", "Finished initializion of ni_player");	
		ni_player.Run ();
	}	

	return 0;
}







