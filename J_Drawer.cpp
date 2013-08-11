#include "NiTE.h"
#include "J_Joint.h"
#include "J_Skeleton.h"
#include "J_Drawer.h"

#include <GLUT/glut.h>



/*########################################################################################################################*/
/*###############################[ --- Constructor/Initialization --- ]###################################################*/
/*########################################################################################################################*/
/* Function: Constructor
 * ---------------------
 * Initializes internal parameters
 */
J_Drawer::J_Drawer () {

	/*--- initialize colors ---*/
	Colors[0][0] = 1;
	Colors[0][1] = 0;
	Colors[0][2] = 0;

	Colors[1][0] = 0;
	Colors[1][1] = 1;
	Colors[1][2] = 0;

	Colors[2][0] = 0;
	Colors[2][1] = 0;
	Colors[2][2] = 1;

	Colors[3][0] = 1;
	Colors[3][1] = 1;
	Colors[3][2] = 1;

	colorCount = 3;

	g_visibleUsers[0] =  false;
	g_skeletonStates[0] = nite::SKELETON_NONE;

	g_userStatusLabels[0][0] = 0;
	g_generalMessage[0] = 0;

	g_drawSkeleton = true;
	g_drawCenterOfMass = false;
	g_drawStatusLabel = true;
	g_drawBoundingBox = false;
	g_drawBackground = true;
	g_drawDepth = true;
	g_drawFrameId = false;

	g_nXRes = 0; 
	g_nYRes = 0;

	g_poseTimeoutToExit = 2000;;

	g_generalMessage[0] = 0;
}


/*########################################################################################################################*/
/*###############################[ --- Depth Frame Utilities --- ]########################################################*/
/*########################################################################################################################*/
void J_Drawer::calculateHistogram(float* pHistogram, int histogramSize, J_VideoFrameRef* depthFrame) {

	const openni::DepthPixel* pDepth = (const openni::DepthPixel*)depthFrame->getData();
	int width = depthFrame->getWidth();
	int height = depthFrame->getHeight();
	// Calculate the accumulative histogram (the yellow display...)
	memset(pHistogram, 0, histogramSize*sizeof(float));
	int restOfRow = depthFrame->getStrideInBytes() / sizeof(openni::DepthPixel) - width;

	unsigned int nNumberOfPoints = 0;
	for (int y = 0; y < height; ++y)
	{
		for (int x = 0; x < width; ++x, ++pDepth)
		{
			if (*pDepth != 0)
			{
				pHistogram[*pDepth]++;
				nNumberOfPoints++;
			}
		}
		pDepth += restOfRow;
	}
	for (int nIndex=1; nIndex<histogramSize; nIndex++)
	{
		pHistogram[nIndex] += pHistogram[nIndex-1];
	}
	if (nNumberOfPoints)
	{
		for (int nIndex=1; nIndex<histogramSize; nIndex++)
		{
			pHistogram[nIndex] = (256 * (1.0f - (pHistogram[nIndex] / nNumberOfPoints)));
		}
	}
}





/*########################################################################################################################*/
/*###############################[ --- Drawing Utilities --- ]############################################################*/
/*########################################################################################################################*/

void J_Drawer::glPrintString(void *font, const char *str) {
	int i,l = (int)strlen(str);
	for(i=0; i<l; i++)
	{   
		glutBitmapCharacter(font,*str++);
	}   
}

void J_Drawer::DrawStatusLabel(nite::UserTracker* pUserTracker, const nite::UserData& user) {
	int color = user.getId() % colorCount;
	glColor3f(1.0f - Colors[color][0], 1.0f - Colors[color][1], 1.0f - Colors[color][2]);

	float x,y;
	pUserTracker->convertJointCoordinatesToDepth(user.getCenterOfMass().x, user.getCenterOfMass().y, user.getCenterOfMass().z, &x, &y);
	x *= GL_WIN_SIZE_X/(float)g_nXRes;
	y *= GL_WIN_SIZE_Y/(float)g_nYRes;
	char *msg = g_userStatusLabels[user.getId()];
	glRasterPos2i(x-((strlen(msg)/2)*8),y);
	glPrintString(GLUT_BITMAP_HELVETICA_18, msg);
}

void J_Drawer::DrawFrameId(nite::UserTracker* pUserTracker, J_Skeleton *skeleton, int frameId) {


	char buffer[80] = "";
	sprintf(buffer, "%d", frameId);
	glColor3f(1.0f, 0.0f, 0.0f);
	glRasterPos2i(20, 20);
	glPrintString(GLUT_BITMAP_HELVETICA_18, buffer);
}


void J_Drawer::DrawCenterOfMass(nite::UserTracker* pUserTracker, const nite::UserData& user) {
	glColor3f(1.0f, 1.0f, 1.0f);

	float coordinates[3] = {0};

	pUserTracker->convertJointCoordinatesToDepth(user.getCenterOfMass().x, user.getCenterOfMass().y, user.getCenterOfMass().z, &coordinates[0], &coordinates[1]);

	coordinates[0] *= GL_WIN_SIZE_X/(float)g_nXRes;
	coordinates[1] *= GL_WIN_SIZE_Y/(float)g_nYRes;
	glPointSize(8);
	glVertexPointer(3, GL_FLOAT, 0, coordinates);
	glDrawArrays(GL_POINTS, 0, 1);
}

void J_Drawer::DrawBoundingBox(const nite::UserData& user) {
	glColor3f(1.0f, 1.0f, 1.0f);

	// cout << "bounding box coords: " << user.getBoundingBox().min.x << ", " << user.getBoundingBox().max.y << ", " << user.getBoundingBox().min.y << ", " << user.getBoundingBox().max.x << endl;

	float coordinates[] =
	{
		user.getBoundingBox().max.x, user.getBoundingBox().max.y, 0,
		user.getBoundingBox().max.x, user.getBoundingBox().min.y, 0,
		user.getBoundingBox().min.x, user.getBoundingBox().min.y, 0,
		user.getBoundingBox().min.x, user.getBoundingBox().max.y, 0,
	};
	coordinates[0]  *= GL_WIN_SIZE_X/(float)g_nXRes;
	coordinates[1]  *= GL_WIN_SIZE_Y/(float)g_nYRes;
	coordinates[3]  *= GL_WIN_SIZE_X/(float)g_nXRes;
	coordinates[4]  *= GL_WIN_SIZE_Y/(float)g_nYRes;
	coordinates[6]  *= GL_WIN_SIZE_X/(float)g_nXRes;
	coordinates[7]  *= GL_WIN_SIZE_Y/(float)g_nYRes;
	coordinates[9]  *= GL_WIN_SIZE_X/(float)g_nXRes;
	coordinates[10] *= GL_WIN_SIZE_Y/(float)g_nYRes;

	glPointSize(2);
	glVertexPointer(3, GL_FLOAT, 0, coordinates);
	glDrawArrays(GL_LINE_LOOP, 0, 4);
}

















/*########################################################################################################################*/
/*###############################[--- J_Skeleton drawing functions ---]###################################################*/
/*########################################################################################################################*/

/* Function: Draw_J_Limb
 * ---------------------
 * draws a limb, specified by two joints (and a color), to the screen
 */
void J_Drawer::Draw_J_Limb (J_Joint* joint1, J_Joint* joint2, int color) {

	/*### Step 1: get absolute coordinates ###*/
	float coordinates[6] = {0};
	nite::Point3f joint1_position_absolute = joint1->getPositionAbsolute ();
	nite::Point3f joint2_position_absolute = joint2->getPositionAbsolute ();	
	coordinates[0] = joint1_position_absolute.x;
	coordinates[1] = joint1_position_absolute.y;
	coordinates[3] = joint2_position_absolute.x;
	coordinates[4] = joint2_position_absolute.y;

	/*--- (coordinates need scaling) ---*/
	coordinates[0] *= GL_WIN_SIZE_X/(float)g_nXRes;
	coordinates[1] *= GL_WIN_SIZE_Y/(float)g_nYRes;
	coordinates[3] *= GL_WIN_SIZE_X/(float)g_nXRes;
	coordinates[4] *= GL_WIN_SIZE_Y/(float)g_nYRes;

	if (joint1->getPositionConfidence() == 1 && joint2->getPositionConfidence() == 1)
	{
		glColor3f(1.0f - Colors[color][0], 1.0f - Colors[color][1], 1.0f - Colors[color][2]);
	}
	else if (joint1->getPositionConfidence() < 0.5f || joint2->getPositionConfidence() < 0.5f)
	{
		return;
	}
	else
	{
		glColor3f(.5, .5, .5);
	}
	glPointSize(2);
	glVertexPointer(3, GL_FLOAT, 0, coordinates);
	glDrawArrays(GL_LINES, 0, 2);

	glPointSize(10);
	if (joint1->getPositionConfidence() == 1)
	{
		glColor3f(1.0f - Colors[color][0], 1.0f - Colors[color][1], 1.0f - Colors[color][2]);
	}
	else
	{
		glColor3f(.5, .5, .5);
	}
	glVertexPointer(3, GL_FLOAT, 0, coordinates);
	glDrawArrays(GL_POINTS, 0, 1);

	if (joint2->getPositionConfidence() == 1)
	{
		glColor3f(1.0f - Colors[color][0], 1.0f - Colors[color][1], 1.0f - Colors[color][2]);
	}
	else
	{
		glColor3f(.5, .5, .5);
	}
	glVertexPointer(3, GL_FLOAT, 0, coordinates+3);
	glDrawArrays(GL_POINTS, 0, 1);
}


/* Function: DrawSkeleton_J_Skeleton
 * ---------------------------------
 * Draws a J_Skeleton to the screen
 */
void J_Drawer::Draw_J_Skeleton (J_Skeleton *skeleton) {

	/*--- Head + Neck ---*/
	Draw_J_Limb(skeleton->getJoint(nite::JOINT_HEAD), skeleton->getJoint(nite::JOINT_NECK), 0);

	/*--- Left Shoulder/Elbow/Hand---*/
	Draw_J_Limb(skeleton->getJoint(nite::JOINT_LEFT_SHOULDER), skeleton->getJoint(nite::JOINT_LEFT_ELBOW), 0);
	Draw_J_Limb(skeleton->getJoint(nite::JOINT_LEFT_ELBOW), skeleton->getJoint(nite::JOINT_LEFT_HAND), 0);

	/*--- Right Shoulder/Elbow/Hand ---*/
	Draw_J_Limb(skeleton->getJoint(nite::JOINT_RIGHT_SHOULDER), skeleton->getJoint(nite::JOINT_RIGHT_ELBOW), 0);
	Draw_J_Limb(skeleton->getJoint(nite::JOINT_RIGHT_ELBOW), skeleton->getJoint(nite::JOINT_RIGHT_HAND), 0);

	/*--- Left/Right Shoulders ---*/
	Draw_J_Limb(skeleton->getJoint(nite::JOINT_LEFT_SHOULDER), skeleton->getJoint(nite::JOINT_RIGHT_SHOULDER), 0);

	/*--- Shoulder - torso ---*/
	Draw_J_Limb(skeleton->getJoint(nite::JOINT_LEFT_SHOULDER), skeleton->getJoint(nite::JOINT_TORSO), 0);
	Draw_J_Limb(skeleton->getJoint(nite::JOINT_RIGHT_SHOULDER), skeleton->getJoint(nite::JOINT_TORSO), 0);

	/*--- Torso/Hip ---*/
	Draw_J_Limb(skeleton->getJoint(nite::JOINT_TORSO), skeleton->getJoint(nite::JOINT_LEFT_HIP), 0);
	Draw_J_Limb(skeleton->getJoint(nite::JOINT_TORSO), skeleton->getJoint(nite::JOINT_RIGHT_HIP), 0);

	/*--- Hips ---*/
	Draw_J_Limb(skeleton->getJoint(nite::JOINT_LEFT_HIP), skeleton->getJoint(nite::JOINT_RIGHT_HIP), 0);

	/*--- Left leg ---*/
	Draw_J_Limb(skeleton->getJoint(nite::JOINT_LEFT_HIP), skeleton->getJoint(nite::JOINT_LEFT_KNEE), 0);
	Draw_J_Limb(skeleton->getJoint(nite::JOINT_LEFT_KNEE), skeleton->getJoint(nite::JOINT_LEFT_FOOT), 0);

	/*--- Right leg ---*/
	Draw_J_Limb(skeleton->getJoint(nite::JOINT_RIGHT_HIP), skeleton->getJoint(nite::JOINT_RIGHT_KNEE), 0);
	Draw_J_Limb(skeleton->getJoint(nite::JOINT_RIGHT_KNEE), skeleton->getJoint(nite::JOINT_RIGHT_FOOT), 0);

	/*--- Beat and Pop ---*/
	if (skeleton->getPop ()) 	indicate_pop 	(skeleton);
	if (skeleton->getBeat()) 	indicate_beat 	();

}










/*########################################################################################################################*/
/*###############################[--- Beat/Pop indication functions ---]##################################################*/
/*########################################################################################################################*/

/* Function: J_IndicateBeat
 * ------------------------
 * draws a red box to indicate when the beat has occurred
 */
void J_Drawer::indicate_beat () {
	glColor3f(1.0f, 0.0f, 0.0f);
	
	float coordinates[] =
	{
		50, 50, 0,
		50, 20, 0,
		20, 20, 0,
		20, 50, 0,
	};
	coordinates[0]  *= GL_WIN_SIZE_X/(float)g_nXRes;
	coordinates[1]  *= GL_WIN_SIZE_Y/(float)g_nYRes;
	coordinates[3]  *= GL_WIN_SIZE_X/(float)g_nXRes;
	coordinates[4]  *= GL_WIN_SIZE_Y/(float)g_nYRes;
	coordinates[6]  *= GL_WIN_SIZE_X/(float)g_nXRes;
	coordinates[7]  *= GL_WIN_SIZE_Y/(float)g_nYRes;
	coordinates[9]  *= GL_WIN_SIZE_X/(float)g_nXRes;
	coordinates[10] *= GL_WIN_SIZE_Y/(float)g_nYRes;

	glPointSize(20);
	glVertexPointer(3, GL_FLOAT, 0, coordinates);
	glDrawArrays(GL_LINE_LOOP, 0, 4);
}

/* Function: J_IndicatePop
 * -----------------------
 * draws a box around the dancert to indicate where their pops are
 */
void J_Drawer::indicate_pop (J_Skeleton *skeleton) {

	nite::BoundingBox bounding_box = skeleton->getBoundingBox ();

	glColor3f(1.0f, 1.0f, 1.0f);

	float coordinates[] =
	{
		bounding_box.max.x, bounding_box.max.y, 0,
		bounding_box.max.x, bounding_box.min.y, 0,
		bounding_box.min.x, bounding_box.min.y, 0,
		bounding_box.min.x, bounding_box.max.y, 0,
	};
	coordinates[0]  *= GL_WIN_SIZE_X/(float)g_nXRes;
	coordinates[1]  *= GL_WIN_SIZE_Y/(float)g_nYRes;
	coordinates[3]  *= GL_WIN_SIZE_X/(float)g_nXRes;
	coordinates[4]  *= GL_WIN_SIZE_Y/(float)g_nYRes;
	coordinates[6]  *= GL_WIN_SIZE_X/(float)g_nXRes;
	coordinates[7]  *= GL_WIN_SIZE_Y/(float)g_nYRes;
	coordinates[9]  *= GL_WIN_SIZE_X/(float)g_nXRes;
	coordinates[10] *= GL_WIN_SIZE_Y/(float)g_nYRes;

	glPointSize(2);
	glVertexPointer(3, GL_FLOAT, 0, coordinates);
	glDrawArrays(GL_LINE_LOOP, 0, 4);
}


/*########################################################################################################################*/
/*###############################[--- Frame Drawing ---]##################################################################*/
/*########################################################################################################################*/
/* Function: draw_frame
 * --------------------
 * given a pointer to a frame, this function will draw it on screen.
 */
void J_Drawer::draw_frame (J_Frame *frame) {

	J_VideoFrameRef *depthFrame = frame->get_frame_ref ();

	/*### Step 1: initialize (allocate) the texture map if has not previously been initialized ###*/
	if (pixel_texture_map == NULL) {
		texture_map_x = MIN_CHUNKS_SIZE(depthFrame->getResolutionX(), TEXTURE_SIZE);
		texture_map_y = MIN_CHUNKS_SIZE(depthFrame->getResolutionY(), TEXTURE_SIZE);
		pixel_texture_map = new openni::RGB888Pixel[texture_map_x * texture_map_y];
	}

	/*### --- OpenGL Stuff... not sure what this does --- ###*/
	glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	glMatrixMode(GL_PROJECTION);
	glPushMatrix();
	glLoadIdentity();
	glOrtho(0, GL_WIN_SIZE_X, GL_WIN_SIZE_Y, 0, -1.0, 1.0);


	/*### if we are drawing the depth map, calculate a histogram ###*/
	calculateHistogram(depth_histogram, MAX_DEPTH, depthFrame);


	/*### initialize m_pTexMap to zero ###*/
	int data_size = texture_map_y*texture_map_x*sizeof(openni::RGB888Pixel);
	memset(pixel_texture_map, 0, data_size);


	float factor[3] = {1, 1, 1};
	/*###[ --- Drawing Users in Special Colors --- ]###*/
	// check if we need to draw depth frame to texture
	// if (depthFrame->isValid() && drawer.g_drawDepth) {
	if (depthFrame->isValid ()) {

		// const nite::UserId* pLabels = userLabels.getPixels();

		const openni::DepthPixel* pDepthRow = (const openni::DepthPixel*)depthFrame->getData();
		openni::RGB888Pixel* pTexRow = pixel_texture_map + depthFrame->getCropOriginY() * texture_map_x;
		int rowSize = depthFrame->getStrideInBytes() / sizeof(openni::DepthPixel);

		for (int y = 0; y < depthFrame->getHeight(); ++y)
		{
			const openni::DepthPixel* pDepth = pDepthRow;
			openni::RGB888Pixel* pTex = pTexRow + depthFrame->getCropOriginX();

			// for (int x = 0; x < depthFrame->getWidth(); ++x, ++pDepth, ++pTex, ++pLabels)
			for (int x = 0; x < depthFrame->getWidth(); ++x, ++pDepth, ++pTex)
			{
				if (*pDepth != 0)
				{
					// if (*pLabels == 0)
					// {
						if (!g_drawBackground)
						{
							factor[0] = factor[1] = factor[2] = 0;

						}
						else
						{
							factor[0] = Colors[colorCount][0];
							factor[1] = Colors[colorCount][1];
							factor[2] = Colors[colorCount][2];
						}
					// }
					// else
					// {
						// factor[0] = drawer.Colors[*pLabels % drawer.colorCount][0];
						// factor[1] = drawer.Colors[*pLabels % drawer.colorCount][1];
						// factor[2] = drawer.Colors[*pLabels % drawer.colorCount][2];
					// }

					int nHistValue = depth_histogram[*pDepth];
					pTex->r = nHistValue*factor[0];
					pTex->g = nHistValue*factor[1];
					pTex->b = nHistValue*factor[2];

					factor[0] = factor[1] = factor[2] = 1;
				}
			}

			pDepthRow += rowSize;
			pTexRow += texture_map_x;
		}
	}

	glTexParameteri(GL_TEXTURE_2D, GL_GENERATE_MIPMAP_SGIS, GL_TRUE);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, texture_map_x, texture_map_y, 0, GL_RGB, GL_UNSIGNED_BYTE, pixel_texture_map);

	// Display the OpenGL texture map
	glColor4f(1,1,1,1);

	glEnable(GL_TEXTURE_2D);
	glBegin(GL_QUADS);

	g_nXRes = depthFrame->getResolutionX();
	g_nYRes = depthFrame->getResolutionY();

	// upper left
	glTexCoord2f(0, 0);
	glVertex2f(0, 0);
	// upper right
	glTexCoord2f((float)g_nXRes/(float)texture_map_x, 0);
	glVertex2f(GL_WIN_SIZE_X, 0);
	// bottom right
	glTexCoord2f((float)g_nXRes/(float)texture_map_x, (float)g_nYRes/(float)texture_map_y);
	glVertex2f(GL_WIN_SIZE_X, GL_WIN_SIZE_Y);
	// bottom left
	glTexCoord2f(0, (float)g_nYRes/(float)texture_map_y);
	glVertex2f(0, GL_WIN_SIZE_Y);

	glEnd();
	glDisable(GL_TEXTURE_2D);

	/*### Finally - draw the skeleton ###*/
	J_Skeleton *skeleton = frame->get_skeleton ();
	if (skeleton->isValid ()) {
		Draw_J_Skeleton (frame->get_skeleton ());
	}


	/*### Swap buffers (display) ###*/
	glutSwapBuffers ();
}











