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
	if (argc != 5) print_error ("Incorrect usage", "try ./ (record|play|mark) [.sync filename, without .sync]");
	char *mode_string 	= argv[1];
	char *file_path		= argv[2];
	char *read_dir		= argv[3];		//directory we are reading from
	char *write_dir 	= argv[4];		//directory we are writing from


	if (strcmp (mode_string, "record") == 0) {
		print_status ("MAIN", "Beginning Initializion of ni_recorder");
		NI_Recorder ni_recorder (file_path, read_dir, write_dir, argc, argv);
		print_status ("MAIN", "Finished initializion of ni_recorder");
		ni_recorder.Run ();
	}
	else if (strcmp(mode_string, "play") == 0) {
		print_status ("MAIN", "Beginning Initialization of ni_player");
		NI_Player ni_player (file_path, read_dir, write_dir, argc, argv);
		print_status ("MAIN", "Finished initializion of ni_player");	
		ni_player.Run ();
	}	

	return 0;
}







