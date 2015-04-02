/** @file plotcv_public.h
*   @brief Public prototypes and definitions pertaining to the plotcv library.    
*
*   @author Alex N. Byrley (anbyrley)
*   @date April 2015
*   @bug No known bugs
*/

#ifndef PLOTCV_PUBLIC_H
#define PLOTCV_PUBLIC_H

//================================================================================================//
//=====================================Standard Includes==========================================//
//===============================================================================================//

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>


//================================================================================================//
//==========================================Typedefs==============================================//
//================================================================================================//

//================================================================================================//
/** @enum plotcv_plot_type
*   @brief This enum type contains macros for various plotcv plot types.
*
*   These enums should be used for specifying the type of plot to be generated.
*/
//================================================================================================//
typedef enum{

	PLOTCV_LINE_PLOT,
	PLOTCV_POINT_PLOT,
	PLOTCV_STEM_PLOT

} plotcv_plot_type;


//================================================================================================//
/** @struct plotcv_graph_t
*   @brief This structure is the typedef for the plotcv graph object.
*
*   To create a plot in plotcv, the user must create a plotcv_graph_t object. This object stores all
* 	the information needed to make a plotcv plot. Currently, it can interface ONLY with openCV 
*	functionality. 
*/
//================================================================================================//
typedef struct plotcv_graph_s plotcv_graph_t;

//================================================================================================//
//====================================Function Declarations=======================================//
//================================================================================================//

//================================================================================================//
/**
* @brief This function returns a pointer to a fully intialized plotcv_graph_t object.
*
* If the data pointer is NULL, the function allocates an array of zeros of length data_length. If
* the label pointer is NULL, the function sets the label to f(x). Naturally, the data_length,
* image_height, and image_width parameters must be valid positive unsigned integers. If the plot
* type is incorrectly specified, the plots will not be drawn.
*
* @param[in] double* data
* @param[in] char* label
* @param[in] unsigned int data_length
* @param[in] unsigned int image_height
* @param[in] unsigned int image_width
* @param[in] plotcv_plot_type plot_type
*
* @return plotcv_graph_t* self
*/
//================================================================================================//
plotcv_graph_t* plotcv_create_graph(double*, 
						  			char*, 
									unsigned int, unsigned int, unsigned int,
						  			plotcv_plot_type);


//================================================================================================//
/**
* @brief This function destroys a plotcv graph object.
*
* All internal memory is deallocated in the reverse order it was initalized, and the corresponding
* pointers are set to NULL. Including the object pointer itself.
*
* @param[in,out] plotcv_graph_t* self
*
* @return NONE
*/
//================================================================================================//
void plotcv_destroy_graph(plotcv_graph_t*);


//================================================================================================//
/**
* @brief This function draws a plotcv graph object.
*
* The function sets the plotcv_graph's internal image via its data fields, which should have been
* initialized in the create function. If errors occur, the function prints the issue to stderr
* and exits. 
*
* @param[in] plotcv_graph_t* self
*
* @return NONE
*/
//================================================================================================//
void plotcv_draw_graph(plotcv_graph_t*);


//================================================================================================//
/**
* @brief This function displays a plotcv graph object.
*
* The function creates a window and displays the plotcv graph's internal data for 20 seconds, 
* afterwhich, the window is destroyed.
*
* @param[in] plotcv_graph_t* self
*
* @return NONE
*/
//================================================================================================//
void plotcv_display_graph(plotcv_graph_t*);


//================================================================================================//
/**
* @brief This function saves a plotcv graph as a .jpg file.
*
* The function saved a plotcv graph object to a file, whose name is specified by the passed in char
* ptr. If said ptr is NULL, then the file is named plotcv.jpg.
*
* @param[in] plotcv_graph_t* self
*
* @return NONE
*/
//================================================================================================//
void plotcv_save_graph(plotcv_graph_t*, char*);



#endif // PLOTCV_PUBLIC_H //
