#ifndef _DRAWING_FUNCTIONS_
#define _DRAWING_FUNCTIONS_

/*--- OpenGL ---*/
#include <GLUT/glut.h>

/*--- NiTE ---*/
#include "NiTE.h"

/*--- OpenCV ---*/
// #include "opencv2/objdetect/objdetect.hpp"
// #include "opencv2/highgui/highgui.hpp"
// #include "opencv2/imgproc/imgproc.hpp"

/*--- My Files ---*/
#include "J_Frame.h"

/*--- Constants ---*/
#define GL_WIN_SIZE_X	1280
#define GL_WIN_SIZE_Y	1024
#define TEXTURE_SIZE	512
#define DEFAULT_DISPLAY_MODE	DISPLAY_MODE_DEPTH
#define MIN_NUM_CHUNKS(data_size, chunk_size)	((((data_size)-1) / (chunk_size) + 1))
#define MIN_CHUNKS_SIZE(data_size, chunk_size)	(MIN_NUM_CHUNKS(data_size, chunk_size) * (chunk_size))
#define MAX_USERS 10
#define MAX_DEPTH 10000
#define USER_MESSAGE(msg) {\
	printf ("");}




class J_Drawer {
private:
	

	/*--- Drawing Parameters ---*/
	int g_nXRes;
	int g_nYRes;
	int g_poseTimeoutToExit; //time to hold pose before program exits


	/*--- Drawing Options ---*/
	bool g_drawSkeleton;
	bool g_drawCenterOfMass;
	bool g_drawStatusLabel;
	bool g_drawBoundingBox;
	bool g_drawBackground;
	bool g_drawDepth;
	bool g_drawFrameId;


	/*--- Drawing Colors ---*/
	float Colors[4][3];
	int colorCount;

	/*--- Dealing with raw depth map ---*/
	// float					depth_histogram[MAX_DEPTH];
	openni::RGB888Pixel*	pixel_texture_map;
	unsigned int			texture_map_x;
	unsigned int			texture_map_y;

	/*--- User Statuses ---*/
	bool g_visibleUsers[MAX_USERS];
	char g_userStatusLabels[MAX_USERS][100];

	/*--- Skeleton States ---*/
	nite::SkeletonState g_skeletonStates[MAX_USERS];
	char g_generalMessage[100];


	/*--- Drawing Utilities ---*/
	void calculateHistogram	(float* pHistogram, int histogramSize, J_VideoFrameRef* depthFrame); 

	/*################[ --- Private Drawing Functions --- ]############*/ 
	/*--- Random Utilities ---*/
	void glPrintString		(void *font, const char *str);
	void DrawStatusLabel 	(nite::UserTracker* pUserTracker, const nite::UserData& user);
	void DrawFrameId 		(nite::UserTracker* pUserTracker, J_Skeleton *skeleton, int frameId);
	void DrawCenterOfMass 	(nite::UserTracker* pUserTracker, const nite::UserData& user);
	void DrawBoundingBox 	(const nite::UserData& user);

	/*--- Skeleton Drawing ---*/
	void Draw_J_Limb 		(J_Joint* joint1, J_Joint* joint2, int color);
	void Draw_J_Skeleton 	(J_Skeleton *skeleton);

	/*--- Beat/Pop Indication ---*/
	void	indicate_beat 	();
	void	indicate_pop 	(J_Skeleton *skeleton);



public:

	/*--- Constructor ---*/
	J_Drawer ();


	/*--- Public Drawing Functions ---*/
	void draw_frame (J_Frame * frame);




};

#endif