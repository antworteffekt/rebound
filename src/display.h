/**
 * @file 	display.h
 * @brief 	Realtime OpenGL visualization.
 * @author 	Hanno Rein <hanno@hanno-rein.de>
 * 
 * @section 	LICENSE
 * Copyright (c) 2011 Hanno Rein, Shangfei Liu
 *
 * This file is part of rebound.
 *
 * rebound is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * rebound is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with rebound.  If not, see <http://www.gnu.org/licenses/>.
 *
 */
#ifndef _DISPLAY_H
#define _DISPLAY_H
#include <semaphore.h>
sem_t* display_mutex;

struct reb_simulation;
extern struct reb_simulation* display_r; 

/**
 * This routine is called by the glut run loop or manually, whenever the screen has to be redrawn 
 */
void display(void);

/**
 * This function initializes OpenGL and starts the run loop. It will never return.
 * @param argc Number of command line arguments.
 * @param argv Command line arguments.
 */
void display_init(int argc, char* argv[], double tmax);

#ifdef OPENGL
extern double display_rotate_x;	/**< Rotate everything around the x-axis. */
extern double display_rotate_z;	/**< Rotate everything around the z-axis. */
#endif  // OPENGL
#endif
