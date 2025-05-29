import inspect
from pymclevel.box import BoundingBox

displayName = "Set Selection Filter"

inputs = (	("min x",0),
			("min y",0),
			("min z",0),
			("width",0),
			("height",0),
			("length",0),
			)

def perform(level, box, options):

	newBox = BoundingBox((options["min x"], options["min y"], options["min z"]), (options["width"], options["height"], options["length"]))

	editor = inspect.stack()[1][0].f_locals.get('self', None).editor

	editor.selectionTool.setSelection(newBox)
	editor.mainViewport.cameraPosition = (newBox.size/2)+newBox.origin

	raise Exception("New area selected")
