##########################################################################
#
#  Copyright (c) 2013, Image Engine Design Inc. All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#      * Redistributions of source code must retain the above
#        copyright notice, this list of conditions and the following
#        disclaimer.
#
#      * Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials provided with
#        the distribution.
#
#      * Neither the name of John Haddon nor the names of
#        any other contributors to this software may be used to endorse or
#        promote products derived from this software without specific prior
#        written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
##########################################################################

import IECore
import IECoreScene

import Gaffer
import GafferUI
import GafferScene

##########################################################################
# Metadata
##########################################################################

def __cameraSummary( plug ) :

	info = []
	if plug["renderCamera"]["enabled"].getValue() :
		info.append( plug["renderCamera"]["value"].getValue() )
	if plug["filmFit"]["enabled"].getValue() :
		info.append( "Fit Mode %s" %
			IECoreScene.Camera.FilmFit.values[ plug["filmFit"]["value"].getValue() ].name
		)
	if plug["renderResolution"]["enabled"].getValue() :
		resolution = plug["renderResolution"]["value"].getValue()
		info.append( "%dx%d" % ( resolution[0], resolution[1] ) )
	if plug["pixelAspectRatio"]["enabled"].getValue() :
		pixelAspectRatio = plug["pixelAspectRatio"]["value"].getValue()
		info.append( "Aspect %s" % GafferUI.NumericWidget.valueToString( pixelAspectRatio ) )
	if plug["resolutionMultiplier"]["enabled"].getValue() :
		resolutionMultiplier = plug["resolutionMultiplier"]["value"].getValue()
		info.append( "Mult %s" % GafferUI.NumericWidget.valueToString( resolutionMultiplier ) )
	if plug["renderCropWindow"]["enabled"].getValue() :
		crop = plug["renderCropWindow"]["value"].getValue()
		info.append( "Crop %s,%s-%s,%s" % tuple( GafferUI.NumericWidget.valueToString( x ) for x in ( crop.min().x, crop.min().y, crop.max().x, crop.max().y ) ) )
	if plug["overscan"]["enabled"].getValue() :
		info.append( "Overscan %s" % ( "On" if plug["overscan"]["value"].getValue() else "Off" ) )
	if plug["depthOfField"]["enabled"].getValue() :
		info.append( "DOF " + ( "On" if plug["depthOfField"]["value"].getValue() else "Off" ) )

	return ", ".join( info )

def __motionBlurSummary( plug ) :

	info = []
	if plug["cameraBlur"]["enabled"].getValue() :
		info.append( "Camera " + ( "On" if plug["cameraBlur"]["value"].getValue() else "Off" ) )
	if plug["transformBlur"]["enabled"].getValue() :
		info.append( "Transform " + ( "On" if plug["transformBlur"]["value"].getValue() else "Off" ) )
	if plug["deformationBlur"]["enabled"].getValue() :
		info.append( "Deformation " + ( "On" if plug["deformationBlur"]["value"].getValue() else "Off" ) )
	if plug["shutter"]["enabled"].getValue() :
		info.append( "Shutter " + str( plug["shutter"]["value"].getValue() ) )

	return ", ".join( info )

def __statisticsSummary( plug ) :

	info = []
	if plug["performanceMonitor"]["enabled"].getValue() :
		info.append( "Performance Monitor " + ( "On" if plug["performanceMonitor"]["value"].getValue() else "Off" ) )

	return ", ".join( info )

## This dictionary is shared with certain nodes that have options- and
# camera-related plugs. We assume that the first metadata element for
# each user-facing plug is the string `"description"`, so take care to
# maintain this when updating these entries or adding new ones.
plugsMetadata = {

	# Section summaries

	"options" : [

		"layout:section:Camera:summary", __cameraSummary,
		"layout:section:Motion Blur:summary", __motionBlurSummary,
		"layout:section:Statistics:summary", __statisticsSummary,

	],

	# Camera plugs

	"options.renderCamera" : [

		"description",
		"""
		The primary camera to be used for rendering. If this
		is not specified, then a default orthographic camera
		positioned at the origin is used.
		""",

		"layout:section", "Camera",
		"label", "Camera",

	],

	"options.renderCamera.value" : [

		"plugValueWidget:type", "GafferSceneUI.ScenePathPlugValueWidget",
		"path:valid", True,
		"scenePathPlugValueWidget:setNames", IECore.StringVectorData( [ "__cameras" ] ),
		"scenePathPlugValueWidget:setsLabel", "Show only cameras",

	],

	"options.filmFit" : [
		"description",
		"""
		Determines how the size of the rendered image relates to the
		camera aperture. If the aspect ratios of the aperture and the
		output resolution are the same, then this has no effect,
		otherwise it dictates what method is used to preserve the pixel
		aspect ratio of the rendered image.

		Horizontal
		:   The frustum is adjusted so that the rendered image fills
			the full width of the aperture and aspect ratio is
			preserved.

		Vertical
		:   The frustum is adjusted so that the rendered image fills
			the full height of the aperture and aspect ratio is
			preserved.

		Fit
		:   Automatically picks Horizontal or Vertical such that all of
			the aperture is contained within the output image. This may
			result in seeing outside the aperture at the top and bottom
			or left and right.

		Fill
		:   Automatically picks Horizontal or Vertical such that the
			output image is fully covered by the aperture. Part of the
			aperture may be cropped off at the top and bottom or left
			and right.

		Distort
		:   Distorts the frustum so that the aperture is fitted exactly
			to the output display window, resulting in non-square
			pixels.
		""",
		"layout:section", "Camera",
		"label", "Film Fit",
	],

	"options.filmFit.value" : [

		"preset:Horizontal", IECoreScene.Camera.FilmFit.Horizontal,
		"preset:Vertical", IECoreScene.Camera.FilmFit.Vertical,
		"preset:Fit", IECoreScene.Camera.FilmFit.Fit,
		"preset:Fill", IECoreScene.Camera.FilmFit.Fill,
		"preset:Distort", IECoreScene.Camera.FilmFit.Distort,

		"plugValueWidget:type", "GafferUI.PresetsPlugValueWidget",

	],

	"options.renderResolution" : [

		"description",
		"""
		The resolution of the image to be rendered. Use the
		resolution multiplier as a convenient way to temporarily
		render at multiples of this resolution.
		""",

		"layout:section", "Camera",
		"label", "Resolution",

	],

	"options.pixelAspectRatio" : [

		"description",
		"""
		The aspect ratio (x/y) of the pixels in the rendered image.
		""",

		"layout:section", "Camera",

	],

	"options.resolutionMultiplier" : [

		"description",
		"""
		Multiplier applied to the render resolution.
		""",

		"layout:section", "Camera",

	],

	"options.renderCropWindow" : [

		"description",
		"""
		Limits the render to a region of the image. The rendered
		image will have the same resolution as usual, but areas
		outside the crop will be rendered black. Coordinates
		range from 0,0 at the top left of the image to 1,1 at the
		bottom right. The crop window tool in the viewer may be
		used to set this interactively.
		""",

		"layout:section", "Camera",
		"label", "Crop Window",

	],

	"options.overscan" : [

		"description",
		"""
		Adds extra pixels to the sides of the rendered image.
		This can be useful when camera shake or blur will be
		added as a post process. This plug just enables overscan
		as a whole - use the overscanTop, overscanBottom, overscanLeft
		and overscanRight plugs to specify the amount of overscan
		on each side of the image.
		""",

		"layout:section", "Camera",

	],

	"options.overscanTop" : [

		"description",
		"""
		The amount of overscan at the top of the image. Specified
		as a 0-1 proportion of the original image height.
		""",

		"layout:section", "Camera",

	],

	"options.overscanBottom" : [

		"description",
		"""
		The amount of overscan at the bottom of the image. Specified
		as a 0-1 proportion of the original image height.
		""",

		"layout:section", "Camera",

	],

	"options.overscanLeft" : [

		"description",
		"""
		The amount of overscan at the left of the image. Specified
		as a 0-1 proportion of the original image width.
		""",

		"layout:section", "Camera",

	],

	"options.overscanRight" : [

		"description",
		"""
		The amount of overscan at the right of the image. Specified
		as a 0-1 proportion of the original image width.
		""",

		"layout:section", "Camera",

	],

	"options.depthOfField" : [

		"description",
		"""
		Enable rendering with depth of field blur.  To get blur, you
		must enable this setting, and set an f-stop on the camera you
		are rendering.
		""",

		"layout:section", "Camera",
	],

	# Motion blur plugs

	"options.cameraBlur" : [

		"description",
		"""
		Whether or not camera motion is taken into
		account in the renderered image. To specify the
		number of segments to use for camera motion, use
		a StandardAttributes node filtered for the camera.
		""",

		"layout:section", "Motion Blur",
		"label", "Camera",

	],

	"options.transformBlur" : [

		"description",
		"""
		Whether or not transform motion is taken into
		account in the renderered image. To specify the
		number of transform segments to use for each
		object in the scene, use a StandardAttributes node
		with appropriate filters.
		""",

		"layout:section", "Motion Blur",
		"label", "Transform",

	],

	"options.deformationBlur" : [

		"description",
		"""
		Whether or not deformation motion is taken into
		account in the renderered image. To specify the
		number of deformation segments to use for each
		object in the scene, use a StandardAttributes node
		with appropriate filters.
		""",

		"layout:section", "Motion Blur",
		"label", "Deformation",

	],

	"options.shutter" : [

		"description",
		"""
		The interval over which the camera shutter is open.
		Measured in frames, and specified relative to the
		frame being rendered.
		""",

		"layout:section", "Motion Blur",

	],

	"options.sampleMotion" : [

		"description",
		"""
		Whether to actually render motion blur.  Disabling this
		setting while motion blur is set up produces a render where
		there is no blur, but there is accurate motion information.
		Useful for rendering motion vector passes.
		""",

		"layout:section", "Motion Blur",

	],

	# Statistics plugs

	"options.performanceMonitor" : [

		"description",
		"""
		Enables a performance monitor and uses it to output
		statistics about scene generation performance.
		""",

		"layout:section", "Statistics",

	],

}

Gaffer.Metadata.registerNode(

	GafferScene.StandardOptions,

	"description",
	"""
	Specifies the standard options (global settings) for the
	scene. These should be respected by all renderers.
	""",

	plugs = plugsMetadata

)
