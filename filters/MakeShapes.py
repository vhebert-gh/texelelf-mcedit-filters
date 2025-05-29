from pymclevel import TAG_Byte, TAG_Short
from pymclevel.materials import alphaMaterials
import math

displayName = "Make Shapes"

inputs = (
	("Block:", alphaMaterials.Air),
	("Shape:",(	"Sphere\\Ellipsoid",
				"Vertical Cyllinder",
				"Horizontal X Cyllinder",
				"Horizontal Z Cyllinder",
				"Cone","Tooth")),
	("Hollow:",False),
	("Wall Thickness (Only If Hollow):",1),
	)
	
def theta_range(step):
	start = 0
	while start < 2*math.pi:
		yield start
		start += step
	
def perform(level, box, options):
	block = options["Block:"]
	shape = options["Shape:"]
	hollow = options["Hollow:"]
	thick = options["Wall Thickness (Only If Hollow):"]

	width, height, length = box.size

	width /= 2
	height /= 2
	length /= 2
	w2 = width*width
	h2 = height*height
	l2 = length*length
	wt2 = (width-thick)**2
	ht2 = (height-thick)**2
	lt2 = (length-thick)**2
	centerx = width + box.minx
	centery = height + box.miny
	centerz = length + box.minz
	
	if shape == "Vertical Cyllinder":
		for z in xrange(-length+1,length):
			z2 = z*z
			for x in range(-width+1,width):
				x2 = x*x
				if float(float(x**2)/float(w2)) + float(float(z2)/float(l2)) <= 1:
					if hollow:
						if float(float(x2)/float(wt2)) + float(float(z2)/float(lt2)) >= 1:
							for y in xrange(box.miny, box.maxy):
								level.setBlockAt(centerx + x, y, centerz + z, block.ID)
								level.setBlockDataAt(centerx + x, y, centerz + z, block.blockData)
					else:
						for y in xrange(box.miny, box.maxy):
							level.setBlockAt(centerx + x, y, centerz + z, block.ID)
							level.setBlockDataAt(centerx + x, y, centerz + z, block.blockData)
	elif shape == "Horizontal Z Cyllinder":
		for y in xrange(-height+1,height):
			y2 = y*y
			for x in range(-width+1,width):
				x2 = x*x
				if float(float(x**2)/float(w2)) + float(float(y2)/float(h2)) <= 1:
					if hollow:
						if float(float(x2)/float(wt2)) + float(float(y2)/float(ht2)) >= 1:
							for z in xrange(box.minz, box.maxz):
								level.setBlockAt(centerx + x, centery + y, z, block.ID)
								level.setBlockDataAt(centerx + x, centery + y, z, block.blockData)
					else:
						for z in xrange(box.minz, box.maxz):
							level.setBlockAt(centerx + x, centery + y, z, block.ID)
							level.setBlockDataAt(centerx + x, centery + y, z, block.blockData)
	elif shape == "Horizontal X Cyllinder":
		for z in xrange(-length+1,length):
			z2 = z*z
			for y in range(-height+1,height):
				y2 = y*y
				if float(float(y**2)/float(h2)) + float(float(z2)/float(l2)) <= 1:
					if hollow:
						if float(float(y2)/float(ht2)) + float(float(z2)/float(lt2)) >= 1:
							for x in xrange(box.minx, box.maxx):
								level.setBlockAt(x, centery + y, centerz + z, block.ID)
								level.setBlockDataAt(x, centery + y, centerz + z, block.blockData)
					else:
						for x in xrange(box.minx, box.maxx):
							level.setBlockAt(x, centery + y, centerz + z, block.ID)
							level.setBlockDataAt(x, centery + y, centerz + z, block.blockData)
	elif shape == "Sphere\\Ellipsoid":
		for y in xrange(-height+1,height):
			y2 = y*y
			for z in xrange(-length+1,length):
				z2 = z*z
				for x in range(-width+1,width):
					x2 = x*x
					if float(float(x2)/float(w2)) + float(float(y2)/float(h2)) + float(float(z2)/float(l2)) <= 1:
						if hollow:
							if float(float(x2)/float(wt2)) + float(float(y2)/float(ht2)) + float(float(z2)/float(lt2)) >= 1:
								level.setBlockAt(centerx + x, centery + y, centerz + z, block.ID)
								level.setBlockDataAt(centerx + x, centery + y, centerz + z, block.blockData)
						else:
							level.setBlockAt(centerx + x, centery + y, centerz + z, block.ID)
							level.setBlockDataAt(centerx + x, centery + y, centerz + z, block.blockData)
	elif shape == "Tooth":
		for y in xrange(0,height*2):
			y2 = y*y
			for z in xrange(-length+1,length):
				z2 = z*z
				for x in range(-width+1,width):
					x2 = x*x
					if (float(float(x2)/float(w2)) + float(float(z2)/float(l2))) + float(y)/float(float(height)*2) <= 1:
						if hollow:
							if (float(float(x2)/float(wt2)) + float(float(z2)/float(lt2))) + float(y)/float(float(height)*2) >= 1:
								level.setBlockAt(centerx + x, box.miny + y, centerz + z, block.ID)
								level.setBlockDataAt(centerx + x, box.miny + y, centerz + z, block.blockData)
						else:
							level.setBlockAt(centerx + x, box.miny + y, centerz + z, block.ID)
							level.setBlockDataAt(centerx + x, box.miny + y, centerz + z, block.blockData)
	elif shape == "Cone":
		for y in xrange(0,height*2):
			y2 = y*y
			for z in xrange(-length+1,length):
				z2 = z*z
				for x in range(-width+1,width):
					x2 = x*x
					if (float(float(x2)/float(w2)) + float(float(z2)/float(l2))) + float(y)/float(float(height)*2) <= 1:
						if hollow:
							if float(float(x2)/float(wt2)) + float(float(y2)/float(ht2)) + float(float(z2)/float(lt2)) >= 1:
								level.setBlockAt(centerx + x, box.miny + y, centerz + z, block.ID)
								level.setBlockDataAt(centerx + x, box.miny + y, centerz + z, block.blockData)
						else:
							level.setBlockAt(centerx + x, box.miny + y, centerz + z, block.ID)
							level.setBlockDataAt(centerx + x, box.miny + y, centerz + z, block.blockData)