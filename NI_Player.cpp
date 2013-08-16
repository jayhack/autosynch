/* ---------------------------------------------- 	*
 *	File: NI_Player.h
 *	-------------------
 *	Class to take care of all recording of skeleton
 * 	and device streams
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
#include "NI_Player.h"

/*--- Namespaces ---*/
using namespace std;

/*--- Initialize Static Elements ---*/
NI_Player* NI_Player::self = NULL;



/*########################################################################################################################*/
/*###############################[--- Constructor/Initialization/Destructor ---] #########################################*/
/*########################################################################################################################*/
/* Function: Constructor
 * ---------------------
 * initializes all forms of recording, though does not start writing to output
 */
NI_Player::NI_Player (const char* file_path, int mode, int argc, char** argv) {

	self = this;

	/*### Step 1: initialize the APIs ###*/
	print_status ("Initialization (Player)", "Initializing APIs");
	initialize_APIs (argc, argv);

	/*### Step 2: initialize opengl ###*/
	print_status ("Initialization (Player)", "Initializing OpenGL");
	InitOpenGL (argc, argv);

	/*### Step 3: initialize the storage delegate ###*/
	print_status ("Initialization (Player)", "Creating Storage Delegate");
	storage_delegate = new J_StorageDelegate (file_path, mode);

	print_status ("Initialization (Player)", "Complete");	

}

/* Function: Destructor
 * --------------------
 * stops recording and closes all files
 */
NI_Player::~NI_Player () {

	/*### Step 2: free all memory allocatd for the device delegate ###*/
	print_status ("Finalization (Player)", "Deleting storage delegate");
	delete storage_delegate;

}




/*########################################################################################################################*/
/*###############################[--- OpenGL Initialization ---]##########################################################*/
/*########################################################################################################################*/
/* Function: InitOpenGLHooks
 * -------------------------
 * sets up OpenGL hooks 
 */
void NI_Player::InitOpenGLHooks () {
	glutKeyboardFunc 	(glut_keyboard);
	glutDisplayFunc		(glut_display);
	glutIdleFunc		(glut_idle);
}

/* Function: InitOpenGL 
 * --------------------
 * initializes OpenGL
 */
openni::Status NI_Player::InitOpenGL (int argc, char **argv) {

	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH);
	glutInitWindowSize(GL_WIN_SIZE_X, GL_WIN_SIZE_Y);
	glutCreateWindow ("Display");
	
	/*--- uncomment for full screen ---*/
	// 	glutFullScreen();

	glutSetCursor(GLUT_CURSOR_NONE);
	InitOpenGLHooks();
	glDisable(GL_DEPTH_TEST);
	glEnable(GL_TEXTURE_2D);
	glEnableClientState(GL_VERTEX_ARRAY);
	glDisableClientState(GL_COLOR_ARRAY);

	return openni::STATUS_OK;
}


/*########################################################################################################################*/
/*#####################[--- OPENGL INTERFACE FUNCTIONS ---]###############################################################*/
/*########################################################################################################################*/
/* Functions: glut(Idle|Display|Keyboard)
 * --------------------------------------
 * these functions serve as the interface to OpenGL;
 * they are static (?)
 */
void NI_Player::glut_idle() {
	
	glutPostRedisplay();
}
void NI_Player::glut_display() {

	NI_Player::self->display();
}
void NI_Player::glut_keyboard(unsigned char key, int x, int y) {
	
	NI_Player::self->onkey(key, x, y);
}





/*########################################################################################################################*/
/*###############################[--- OpenGL Interface ---] ##############################################################*/
/*########################################################################################################################*/
/* Function: onkey
 * ---------------
 * callback function for handling keyboard events.
 * here, it mainly controls wether recording is active or not, 
 * also quitting the application.
 */
void NI_Player::onkey (unsigned char key, int x, int y) {
	
	switch (key)
	{
		/*### ESC: exits application ###*/
		case 27:	
			// Finalize();
			exit (1);
	}
}

void NI_Player::display () {

	/*### Step 1: get the next J_Frame ###*/
	// print_status ("Display", "Getting frame");
	J_Frame *frame = storage_delegate->read ();
	if (frame == NULL) {
		print_status ("Display", "No frames left. terminating");
		exit (0);
	}

	/*### Step 2: draw it to the screen ###*/
	// print_status ("Display", "Drawing frame");
	drawer.draw_frame (frame, false);

	/*### Step 3: free all memory dedicated to the frame ###*/
	delete frame;
	usleep (30000);
}

/* Function: Run
 * -------------
 * engages in the main loop, does not return.
 */
openni::Status NI_Player::Run() {	
	glutMainLoop();
	return openni::STATUS_OK;
}












