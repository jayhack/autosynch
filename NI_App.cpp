/* ---------------------------------------------- 	*
 *	File: NI_app.cpp
 *	--------------
 *	Class to take care of all interface to device
 *	and body.
 *
 *	----------------------------------------------	*/
#if (defined _WIN32)
#define PRIu64 "llu"
#else
#define __STDC_FORMAT_MACROS
#include <inttypes.h>
#endif

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

/*--- OPENGL ---*/
#if (ONI_PLATFORM == ONI_PLATFORM_MACOSX)
        #include <GLUT/glut.h>
#else
        #include <GL/glut.h>
#endif

/*--- My Files ---*/
#include "NI_App.h"

/*--- Namespaces ---*/
using namespace std;


NI_App::NI_App () {}


/* Function: initialize_APIs
 * -------------------------
 * initalizes OpenNI, NiTE and OpenGL
 */
void NI_App::initialize_APIs (int argc, char ** argv) {

	/*### Step 1: set internal pointers ###*/
	print_status ("Initialize_APis", "Opening OpenNI");
	openni::Status rc = openni::OpenNI::initialize();
	if (rc != openni::STATUS_OK) {
		print_error("Failed to initialize OpenNI", openni::OpenNI::getExtendedError());
	}

	/*### Step 4: initialize NiTE ###*/
	print_status ("Initialize_APIs", "Opening NiTE");
	nite::NiTE::initialize();
	
	/*### Step 5: start OpenGL ###*/
	// print_status ("Initialize (General)", "Opening OpenGL");
	// InitOpenGL(argc, argv);
}




















