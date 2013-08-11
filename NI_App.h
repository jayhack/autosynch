/* ---------------------------------------------- 	*
 *	File: NI_app.h
 *	--------------
 *	an abstract class that both NI_Recorder and NI_Player
 *	inherit from. both of them contain:
 *	- J_StorageDelegate
 *	- J_Drawer
 *	- 
 *	----------------------------------------------	*/

#ifndef _NI_APP_H_
#define _NI_APP_H_

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
#include "Utilities.h"
#include "J_StorageDelegate.h"
#include "J_Drawer.h"


/*--- Namespaces ---*/
using namespace std;



/*########################################################################################################################*/
/*###############################[--- NI_app CLASS DEF ---]#######################################################################*/
/*########################################################################################################################*/

class NI_App {
protected:

	/*--- Name/Self ---*/
	static NI_App * 	self;			/*static reference to the active instance*/
	char				app_name[150];

	/*--- Storage ---*/
	J_StorageDelegate *storage_delegate;

	/*--- Drawing --*/
	J_Drawer drawer;


	/*--- Initialize APIs ---*/
	void initialize_APIs (int argc, char **argv);

	/*--- OpenGL Static Functions ---*/
	// static void glut_keyboard 		(unsigned char key, int x, int y);
	// static void glut_display 		();
	// static void glut_idle 			();

	/*--- OpenGL Member Functions ---*/
	// virtual	void display 	();
	// virtual void onkey 		(unsigned char key, int x, int y);

	/*--- OpenGL Inialization ---*/
	// virtual openni::Status 	InitOpenGL 		(int argc, char **argv);

public:

	/*--- Constructor - won't be inherited ---*/
	NI_App ();


};


#endif // _NI_APP_H_
