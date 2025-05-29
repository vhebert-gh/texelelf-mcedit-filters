import sys
import os
import re
from copy import deepcopy
if sys.platform == "win32":
	import tempfile
	temppath = os.path.join(tempfile.gettempdir(),"NBT_Filter_Temp.txt")
else:
	temppath = "/tmp/NBT_Filter_Temp.txt"

displayName = "NBT Editor - Multiplatform"

inputs = (
	("Edit...",("Selection","File","level.dat")),
	)

template = {"name":"", "value":None , "id":-1, "type":-1,"parent":None, "children":[]}

COMPOUND = 0
LIST = 1
LONG = 2
INT = 3
SHORT = 4
BYTE = 5
DOUBLE = 6
FLOAT = 7
INT_ARRAY = 8
BYTE_ARRAY = 9
STRING = 10
UBYTE = 99

tagtypenames = {COMPOUND:"COMP",LIST:"LIST",LONG:"LONG",INT:"INT",SHORT:"SHORT",BYTE:"BYTE",DOUBLE:"DOUBLE",
				FLOAT:"FLOAT",INT_ARRAY:"INT_ARRAY",BYTE_ARRAY:"BYTE_ARRAY",STRING:"STRING"}

tags = {}
newtag = []
clipboard = []
FindHandle = None
TreeHandle = None

clipidctr = 0
idcounter = 0
targettag = 0

def GetID():
	global idcounter
	idcounter+= 1
	return idcounter


def GetValue():
	try:
		with open(temppath,"r") as f:
			result = f.read()
		f.closed
	except:
		return "Error"
	return result

def SetValue(value):
	try:
		with open(temppath,"w") as f:
			f.write(value)
		f.closed
	except:
		pass

if __name__ != "__main__":
	from pymclevel import nbt, TAG_Compound, TAG_List, TAG_Int_Array, TAG_Byte_Array, TAG_String, TAG_Long, TAG_Int, TAG_Short, TAG_Byte, TAG_Double, TAG_Float
	import numpy
	import mcplatform
	from cStringIO import StringIO
	import gzip, zlib
	import pickle
	
	tagtypes =	{	TAG_Compound:0, TAG_List:1, TAG_Long:2, TAG_Int:3, TAG_Short:4,TAG_Byte:5, TAG_Double:6, TAG_Float:7,TAG_Int_Array:8, TAG_Byte_Array:9, TAG_String:10 }

	def NewTag(name, value, id, type, parent, children):
		return {"name":name,"value":value,"id":id,"type":type,"parent":parent,"children":children}

	def Deserialize(obj, tag_num):
		global tags
		if type(obj) is TAG_Compound:
			for tag in sorted(obj.keys(),key=lambda s: s.lower()):
				if type(obj[tag]) in (TAG_Compound, TAG_List):
					new_tag = GetID()
					tags[new_tag] = NewTag(tag,0,new_tag,tagtypes[type(obj[tag])],tag_num,[])
					tags[tag_num]["children"].append(new_tag)
					Deserialize(obj[tag],new_tag)
				elif type(obj[tag]) in (TAG_Byte_Array, TAG_Int_Array):
					new_tag = GetID()
					tags[new_tag] = NewTag(tag,",".join(obj[tag].value.astype("unicode")),new_tag,tagtypes[type(obj[tag])],tag_num,[])
					tags[tag_num]["children"].append(new_tag)
				else:
					new_tag = GetID()
					tags[new_tag] = NewTag(tag,unicode(obj[tag].value),new_tag,tagtypes[type(obj[tag])],tag_num,[])
					tags[tag_num]["children"].append(new_tag)
		elif type(obj) is TAG_List:
			for index in range(0,len(obj)):
				if type(obj[index]) in (TAG_Compound, TAG_List):
					new_tag = GetID()
					tags[new_tag] = NewTag(index,0,new_tag,tagtypes[type(obj[index])],tag_num,[])
					tags[tag_num]["children"].append(new_tag)
					Deserialize(obj[index],new_tag)
				elif type(obj[index]) in (TAG_Byte_Array, TAG_Int_Array):
					new_tag = GetID()
					tags[new_tag] = NewTag(index,",".join(obj[index].value.astype("unicode")),new_tag,tagtypes[type(obj[index])],tag_num,[])
					tags[tag_num]["children"].append(new_tag)
				else:
					new_tag = GetID()
					tags[new_tag] = NewTag(index,unicode(obj[index].value),new_tag,tagtypes[type(obj[index])],tag_num,[])
					tags[tag_num]["children"].append(new_tag)

	def NBT_Tag(type, value):
		if type == COMPOUND:
			return TAG_Compound()
		elif type == LIST:
			return TAG_List()
		elif type == BYTE_ARRAY:
			return TAG_Byte_Array(value)
		elif type == INT_ARRAY:
			return TAG_Int_Array(value)
		elif type == STRING:
			return TAG_String(unicode(value))
		elif type == LONG:
			return TAG_Long(int(value))
		elif type == INT:
			return TAG_Int(int(value))
		elif type == SHORT:
			return TAG_Short(int(value))
		elif type == BYTE:
			return TAG_Byte(int(value))
		elif type == DOUBLE:
			return TAG_Double(float(value))
		elif type == FLOAT:
			return TAG_Float(float(value))

	def GetNBT(obj):
		global tags
		entlist = TAG_List()
		cmpnd = TAG_Compound()
		if "children" in obj:
			for o in obj["children"]:
				retval = Serialize(tags,o,cmpnd)
				newervar = deepcopy(retval)
				entlist.append(newervar)
				del newervar
		return entlist
			
	def Serialize(tree,obj,nbt,scalar=False):
		if tree[obj]["type"] in (COMPOUND, LIST):
			if isinstance(tree[obj]["name"], (int,long)):
				nbt = NBT_Tag(tree[obj]["type"],0)
				nextnbt = nbt
			else:
				nbt[tree[obj]["name"]] = NBT_Tag(tree[obj]["type"],0)
				nextnbt = nbt[tree[obj]["name"]]
			if tree[obj]["children"]:
				if tree[obj]["type"] == COMPOUND:
					for o in tree[obj]["children"]:
						nextnbt = Serialize(tree,o,nextnbt)
				elif tree[obj]["type"] == LIST:
					for o in tree[obj]["children"]:
						nbt[tree[obj]["name"]].append(Serialize(tree,o,0,True))
				elif tree[obj]["type"] in (BYTE_ARRAY, INT_ARRAY):
					intbytearray = tree[obj]["value"]
					intbytearray = re.sub("[^0-9,+-]","",intbytearray)
					if tree[obj]["type"] == INT_ARRAY:
						nbt[tree[obj]["name"]] = NBT_Tag(tree[obj]["type"],numpy.array(intbytearray.split(","),dtype=">u4"))
					else:
						nbt[tree[obj]["name"]] = NBT_Tag(tree[obj]["type"],numpy.array(intbytearray.split(","),dtype="uint8"))
		elif tree[obj]["type"] in (BYTE_ARRAY, INT_ARRAY):
			intbytearray = tree[obj]["value"]
			intbytearray = re.sub("[^0-9,+-]","",intbytearray)
			if tree[obj]["type"] == INT_ARRAY:
				nbt[tree[obj]["name"]] = NBT_Tag(tree[obj]["type"],numpy.array(intbytearray.split(","),dtype=">u4"))
			else:
				nbt[tree[obj]["name"]] = NBT_Tag(tree[obj]["type"],numpy.array(intbytearray.split(","),dtype="uint8"))
		else:
			if scalar:
				return NBT_Tag(tree[obj]["type"],tree[obj]["value"])
			nbt[tree[obj]["name"]] = NBT_Tag(tree[obj]["type"],tree[obj]["value"])
		return nbt
	
else:
	if sys.platform == "darwin":
		for p in sys.path:
			if "MCEdit" in p:
				sys.path.remove(p)

	if "linux" in sys.platform:
		if "DISPLAY" not in os.environ:
			os.environ["DISPLAY"] = ":0"

	import Tkinter as tk
	import tkFileDialog as tkf
	import tkSimpleDialog as tks
	import ttk
	import tkMessageBox
	import pickle
	
	def indent(ct):
		return "    "*ct

	def strexplode(command):
		coms = []
		if not command:
			return coms
		i = 0
		line = ""
		inquote = 0
		for c in xrange(len(command)):
			if command[c] == "{":
				if inquote:
					line += command[c]
				else:
					if line:
						coms.append(indent(i)+line)
						line = ""
					coms.append(indent(i)+"{")
					i += 1
			elif command[c] == "}":
				if inquote:
					line += command[c]
				else:
					if line:
						coms.append(indent(i)+line)
						line = ""
					i -= 1
					line += command[c]
			elif command[c] == "[":
				if inquote:
					line += command[c]
				else:
					if line:
						coms.append(indent(i)+line)
						line = ""
					coms.append(indent(i)+"[")
					i += 1
			elif command[c] == "]":
				if inquote:
					line += command[c]
				else:
					if line:
						coms.append(indent(i)+line)
						line = ""
					i -= 1
					line += command[c]
			elif command[c] == '\"':
				if command[c-1] != "\\":
					inquote ^= 1
				line += command[c]
			elif command[c] == ",":
				if inquote:
					line += command[c]
				else:
					coms.append(indent(i)+line+",")
					line = ""
			else:
				line += command[c]
		else:
			if line:
				coms.append(indent(i)+line)
		return coms

	def strcollapse(lines):
		command = ""
		if len(lines) < 1:
			return command
		elif len(lines) == 1:
			return lines[0]

		if lines[0] == "{":
			command += lines[0].lstrip().rstrip()
		else:
			command += lines[0].lstrip().rstrip() + " "
		for l in lines:
			if not l:
				continue
			if lines.index(l) == 0:
				continue
			command += l.lstrip().rstrip()
		return command

	def NBT2Command(nbtData, tag_list):
		command = ""

		if tag_list[nbtData]["type"] == COMPOUND:
			if tag_list[nbtData]["name"] != "" and isinstance(tag_list[nbtData]["name"], (unicode, str)):
				command += tag_list[nbtData]["name"]+":"
			command += "{"

			for tag in tag_list[nbtData]["children"]:
				command += NBT2Command(tag,tag_list)
				command += ","
			else:
				if command[-1] == ",":
					command = command[:-1]
			command += "}"

		elif tag_list[nbtData]["type"] == LIST:
			if tag_list[nbtData]["name"] != "" and isinstance(tag_list[nbtData]["name"], (unicode, str)):
				command += tag_list[nbtData]["name"]+":"
			command += "["

			for tag in tag_list[nbtData]["children"]:
				command += NBT2Command(tag,tag_list)
				command += ","
			else:
				if command[-1] == ",":
					command = command[:-1]
			command += "]"

		else:
			if tag_list[nbtData]["name"] != "" and isinstance(tag_list[nbtData]["name"], (unicode, str)):
				command += tag_list[nbtData]["name"]+":"
			if tag_list[nbtData]["type"] == STRING:
				command += "\""
				command += unicode.replace(tag_list[nbtData]["value"], ur'"',ur'\"')
				command += "\""
			else:
				if tag_list[nbtData]["type"] == BYTE_ARRAY:
					command += "["+",".join(["%sb" % num for num in tag_list[nbtData]["value"].split(",")])+"]"
				elif tag_list[nbtData]["type"] == INT_ARRAY:
					command += "["+tag_list[nbtData]["value"]+"]"
				else:
					command += unicode(tag_list[nbtData]["value"])
					if tag_list[nbtData]["type"] == BYTE:
						command += "b"
					elif tag_list[nbtData]["type"] == SHORT:
						command += "s"
					elif tag_list[nbtData]["type"] == LONG:
						command += "l"
					elif tag_list[nbtData]["type"] == FLOAT:
						command += "f"
					elif tag_list[nbtData]["type"] == DOUBLE:
						command += "d"
				command += ","
		if command[-1] == ",":
			command = command[:-1]
		return command

	class NBT_Editor(tk.Tk):
		def __init__(self,parent):
			global idcounter, tags
			tk.Tk.__init__(self,parent)
			self.parent = parent
			self.initialize()
			self.modified = False
			idcounter = max(map(int, tags.keys()))

		def initialize(self):
			global TreeHandle
			self.grid()
			self.protocol("WM_DELETE_WINDOW", self.OnCancel)
			self.grid_rowconfigure(0,minsize=457,weight=1)
			self.minsize(520,500)

			TreeHandle = self.tree = ttk.Treeview(self)
			self.tree["show"] = "tree"
			ysb = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
			xsb = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
			self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)

			self.tree.grid(column=0,row=0,sticky="NWSE",columnspan=13)
			ysb.grid(row=0, column=13, sticky="NS")
			xsb.grid(row=1, column=0, sticky="EWS",columnspan=13)

			new_button = tk.Button(self,text=u"New", command=self.OnNew)
			new_button.grid(column=0,row=2,sticky="EWS")
			edit_button = tk.Button(self,text=u"Edit", command=self.OnEdit)
			edit_button.grid(column=1,row=2,sticky="EWS")
			delete_button = tk.Button(self,text=u"Delete", command=self.OnDelete)
			delete_button.grid(column=2,row=2,sticky="EWS")
			copy_button = tk.Button(self,text=u"Copy", command=self.OnCopy)
			copy_button.grid(column=3,row=2,sticky="EWS")
			cut_button = tk.Button(self,text=u"Cut", command=self.OnCut)
			cut_button.grid(column=4,row=2,sticky="EWS")
			paste_button = tk.Button(self,text=u"Paste", command=self.OnPaste)
			paste_button.grid(column=5,row=2,sticky="EWS")
			view_button = tk.Button(self,text=u"View", command=self.OnView)
			view_button.grid(column=6,row=2,sticky="EWS")
			self.plus_button = tk.Button(self,text=u"\u2191", command=self.OnPlus)
			self.plus_button.grid(column=7,row=2,sticky="EWS")
			self.minus_button = tk.Button(self,text=u"\u2193", command=self.OnMinus)
			self.minus_button.grid(column=8,row=2,sticky="EWS")
			find_button = tk.Button(self,text=u"Expand", command=self.OnExpand)
			find_button.grid(column=9,row=2,sticky="EWS")
			find_button = tk.Button(self,text=u"Find", command=self.OnFind)
			find_button.grid(column=10,row=2,sticky="EWS")
			cancel_button = tk.Button(self,text=u"Cancel", command=self.OnCancel)
			cancel_button.grid(column=11,row=2,sticky="EWS")
			done_button = tk.Button(self,text=u"Done", command=self.OnDone)
			done_button.grid(column=12,row=2,sticky="EWS",columnspan=2)
			
			self.bind("<Control-n>", self.OnNew)
			self.bind("<Control-e>", self.OnEdit)
			self.bind("<Delete>", self.OnDelete)
			self.bind("<Control-c>", self.OnCopy)
			self.bind("<Control-x>", self.OnCut)
			self.bind("<Control-v>", self.OnPaste)
			self.bind("<equal>", self.OnPlus)
			self.bind("<minus>", self.OnMinus)
			self.bind("<Control-f>", self.OnFind)
			self.bind("<Escape>", self.OnCancel)
			self.bind("<Return>", self.OnDone)
			
			self.tree.bind("<Double-1>", self.OnEdit)
			self.tree.bind("<<TreeviewSelect>>", self.OnSelectionChange)
			
			for i in xrange(13):
				self.grid_columnconfigure(i,weight=1)
			self.resizable(True,True)
			self.update()
			self.geometry(self.geometry())

			self.plus_button.config(state=tk.DISABLED)
			self.minus_button.config(state=tk.DISABLED)

			self.tree.insert("", "end",1,text="["+tagtypenames[tags[1]["type"]]+"]: "+unicode(tags[1]["name"]), values=[1])
			for i in tags[1]["children"]:
				self.FillTree(i,1)

		def OnNew(self,*args):
			global tags, targettag, newtag
			newtag = None
			newsel = self.tree.selection()[0]
			if newsel == "":
				return
			targettag = self.current_lparam = int(newsel)

			editor = Tag_Editor(self,self.current_lparam,True)
			self.wait_window(editor.EditWindow)
			self.tree.focus_set()

			if newtag:
				tg = deepcopy(template)
				tg["name"] = 0 if newtag[0] == "" else newtag[0]
				tg["type"] = newtag[2]
				tg["value"] = newtag[1]
				if tags[targettag]["type"] == LIST:
					isList = True
					tg["name"] = 0
					if tg["type"] == COMPOUND:
						tg["value"] = 0
				newID = GetID()
				tags[newID] = tg
				tags[newID]["id"] = newID
				tags[newID]["parent"] = targettag
				self.FillTree(newID,targettag)
				tags[targettag]["children"].append(newID)

				self.tree.selection_set(newID)
				self.tree.focus_set()
				self.tree.focus(newID)

				self.modified = True

		def OnSelectionChange(self,*args):
			global targettag, tags
			newsel = self.tree.selection()[0]
			self.current_lparam = targettag = int(newsel)

			if tags[targettag]["parent"]:
				if tags[tags[targettag]["parent"]]["type"] == LIST:
					self.plus_button.config(state=tk.NORMAL)
					self.minus_button.config(state=tk.NORMAL)
					return

			self.plus_button.config(state=tk.DISABLED)
			self.minus_button.config(state=tk.DISABLED)


		def OnEdit(self,*args):
			global tags, targettag, newtag
			newtag = None
			newsel = self.tree.selection()[0]
			if newsel == "":
				return
			targettag = self.current_lparam = int(newsel)

			if self.current_lparam <= 1:
				return
			if tags[tags[self.current_lparam]["parent"]]["type"] == LIST and tags[self.current_lparam]["type"] == COMPOUND:
				return
			editor = Tag_Editor(self,self.current_lparam)
			self.wait_window(editor.EditWindow)
			self.tree.focus_set()

			if newtag:
				self.modified = True
				nodeval = u"["+unicode(tagtypenames[newtag[2]])+u"]: "
				if newtag[0] != "":
					tags[targettag]["name"] = newtag[0]
				if newtag[2] in (COMPOUND, LIST):
					tags[targettag]["value"] = 0
				else:
					tags[targettag]["value"] = newtag[1]
				tags[targettag]["type"] = newtag[2]
				if tags[targettag]["type"] in (COMPOUND, LIST):
					if not isinstance(tags[targettag]["name"], (int,long)):
						nodeval += unicode(tags[targettag]["name"])
				else:
					if isinstance(tags[targettag]["value"], (str,unicode)):
						tags[targettag]["value"] = tags[targettag]["value"]
					if isinstance(tags[targettag]["name"], (int,long)):
						nodeval += unicode(tags[targettag]["value"])
					else:
						nodeval += unicode(unicode(tags[targettag]["name"])+u": "+unicode(tags[targettag]["value"]))
				self.tree.item(targettag,text=nodeval)

		def OnDelete(self,*args):
			global targettag
			newsel = self.tree.selection()[0]
			if newsel == "":
				return
			targettag = self.current_lparam = int(newsel)

			if self.current_lparam <= 1:
				return
			self.tree.focus_set()
			self.DeleteItem(self.current_lparam)
			self.tree.delete(self.current_lparam)
			self.modified = True				

		def OnCopy(self,*args):
			global targettag, clipboard
			newsel = self.tree.selection()[0]
			if newsel == "":
				return
			targettag = self.current_lparam = int(newsel)

			if self.current_lparam > 1 and self.current_lparam != None:
				self.tree.focus_set()
				del clipboard
				clipboard = {}
				self.CopyItem(clipboard, self.current_lparam)
				clipval = NBT2Command(0,clipboard)
				
				self.clipboard_clear()
				self.clipboard_append(clipval)

		def OnCut(self,*args):
			global targettag, clipboard
			newsel = self.tree.selection()[0]
			if newsel == "":
				return
			targettag = self.current_lparam = int(newsel)

			if self.current_lparam > 1 and self.current_lparam != None:
				self.tree.focus_set()
				del clipboard
				clipboard = {}
				self.CopyItem(clipboard, self.current_lparam)
				clipval = NBT2Command(0,clipboard)

				self.DeleteItem(self.current_lparam)
				self.tree.delete(self.current_lparam)
				self.modified = True				

				self.clipboard_clear()
				self.clipboard_append(clipval)

		def OnPaste(self,*args):
			if not clipboard:
				return
			self.tree.focus_set()
			newsel = self.tree.selection()[0]
			if newsel == "":
				return
			targettag = self.current_lparam = int(newsel)
			if tags[targettag]["type"] == COMPOUND:
				if clipboard[0]["name"] == "" or isinstance(clipboard[0]["name"], (int,long)):
					newstring = tks.askstring("Name","Please enter a new tag name.")
					if not newstring:
						return
					clipboard[0]["name"] = newstring
				for c in tags[targettag]["children"]:
					if tags[c]["name"] == clipboard[0]["name"]:
						doloop = True
						newstring = clipboard[0]["name"]
						while doloop:
							newstring = tks.askstring("Name Error","There is already a tag named "+newstring+". Please enter a new one.")
							if not newstring:
								return
							for c in tags[targettag]["children"]:
								if tags[c]["name"] == newstring:
									break
							else:
								doloop = False
						clipboard[0]["name"] = newstring
						break	
			elif tags[targettag]["type"] == LIST:
				if tags[targettag]["children"]:
					if clipboard[0]["type"] != tags[tags[targettag]["children"][0]]["type"]:
						tkMessageBox.showinfo("Error", "The copied tag's type does not match the List child tag type.  Lists can only hold one tag type.")
						return
					clipboard[0]["name"] = 0
				else:
					clipboard[0]["name"] = 0
			else:
				targettag = tags[targettag]["parent"]
				if clipboard[0]["name"] == "" or isinstance(clipboard[0]["name"], (int,long)):
					newstring = tks.askstring("Name","Please enter a new tag name.")
					if not newstring:
						return
					clipboard[0]["name"] = newstring
				for c in tags[targettag]["children"]:
					if tags[c]["name"] == clipboard[0]["name"]:
						doloop = True
						newstring = clipboard[0]["name"]
						while doloop:
							newstring = tks.askstring("Name Error","There is already a tag named "+newstring+". Please enter a new one.")
							if not newstring:
								return
							for c in tags[targettag]["children"]:
								if tags[c]["name"] == newstring:
									break
							else:
								doloop = False
						clipboard[0]["name"] = newstring
						break	
			self.InsertItem(targettag)
			self.FillTree(tags[targettag]["children"][-1],targettag)
			self.modified = True

			self.tree.selection_set(targettag)
			self.tree.focus_set()
			self.tree.focus(targettag)

			targettag = self.current_lparam

		def OnView(self,*args):
			global clipboard
			if not clipboard:
				return
			viewer = Clipboard_Viewer(self,NBT2Command(0,clipboard))
			self.wait_window(viewer.ViewWindow)
			self.tree.focus_set()

		def OnPlus(self,*args):
			global tags
			newsel = self.tree.selection()[0]
			self.current_lparam = targettag = int(newsel)

			self.tree.focus_set()
			parent = tags[self.current_lparam]["parent"]
			if tags[parent]["type"] == LIST:
				ind = tags[parent]["children"].index(self.current_lparam)
				if ind == 0:
					return
				val = tags[parent]["children"].pop(ind)
				tags[parent]["children"].insert(ind-1,val)
				if ind-1 == 0:
					insert = tags[parent]["children"][0]
				else:
					insert = tags[parent]["children"][ind-1]
				self.tree.move(self.current_lparam,parent,self.tree.index(insert)-1)

		def OnMinus(self,*args):
			global tags
			newsel = self.tree.selection()[0]
			self.current_lparam = targettag = int(newsel)

			self.tree.focus_set()
			parent = tags[self.current_lparam]["parent"]
			if tags[parent]["type"] == LIST:
				ind = tags[parent]["children"].index(self.current_lparam)
				if ind == len(tags[parent]["children"])-1:
					return
				val = tags[parent]["children"].pop(ind)
				tags[parent]["children"].insert(ind+1,val)
				if ind+1 == len(tags[parent]["children"])-1:
					insert = "end"
				else:
					insert = tags[parent]["children"][ind]
				self.tree.move(self.current_lparam,parent,self.tree.index(insert) if insert != "end" else insert)

		def OnExpand(self,*args):
			global idcounter
			for a in range(1,idcounter+1):
				self.tree.item(a,open=True)

		def OnFind(self,*args):
			global targettag, tags, FindHandle
			
			newsel = self.tree.selection()[0]
			if newsel == "":
				return
			targettag = self.current_lparam = int(newsel)

			if not FindHandle:
				FindHandle = Find_Tag(self)
			else:
				FindHandle.FindWindow.focus_set()				

		def OnCancel(self,*args):
			global tags
			if self.modified:
				if tkMessageBox.askyesno("Warning!","Changes have been made.  Discard all modifications?"):
					tags = {"Cancelled":True}
					self.destroy()
			else:
				tags = {"Cancelled":True}
				self.destroy()			

		def OnDone(self,*args):
			self.destroy()

		def FillTree(self, tag_num, parent, insertat=None):
			global tags
			if type(tag_num) is list:
				for tag in tag_num:
					nodeval = u"["+unicode(tagtypenames[tags[tag]["type"]])+u"]: "
					if tags[tag]["type"] in (COMPOUND, LIST):
						if not isinstance(tags[tag]["name"], (int,long)):
							nodeval += unicode(unicode(tags[tag]["name"]))
					else:
						if isinstance(tags[tag]["name"], (int,long)):
							nodeval += unicode(unicode(tags[tag]["value"]))
						else:
							nodeval += unicode(unicode(tags[tag]["name"])+": "+unicode(tags[tag]["value"]))
					self.tree.insert(parent, "end", tag, text=nodeval)
					if tags[tag]["type"] in (COMPOUND, LIST):
						self.FillTree(tags[tag]["children"],tag)
			else:
				nodeval = u"["+unicode(tagtypenames[tags[tag_num]["type"]])+u"]: "
				if tags[tag_num]["type"] in (COMPOUND, LIST):
					if not isinstance(tags[tag_num]["name"], (int,long)):
						nodeval += unicode(unicode(tags[tag_num]["name"]))
				else:
					if isinstance(tags[tag_num]["name"], (int,long)):
						nodeval += unicode(tags[tag_num]["value"])
					else:
						nodeval += unicode(unicode(tags[tag_num]["name"])+unicode(": ")+unicode(tags[tag_num]["value"]))
				self.tree.insert(parent, "end", tag_num, text=nodeval)
				if tags[tag_num]["type"] in (COMPOUND, LIST):
					self.FillTree(tags[tag_num]["children"],tag_num)		

		def DeleteItem(self, lparam):
			global tags
			for c in tags[lparam]["children"]:
				self.DeleteItem(c)
			tags[tags[lparam]["parent"]]["children"].remove(lparam)
			del tags[lparam]
			pass

		def CopyItem(self, result, lparam, parent=None, ID=False):
			global tags, clipidctr
			if ID:
				clipidctr += 1
			else:
				clipidctr = 0
			result[clipidctr] = deepcopy(tags[lparam])
			result[clipidctr]["id"] = clipidctr
			result[clipidctr]["parent"] = parent
			if parent != None:
				result[parent]["children"].append(clipidctr)
			result[clipidctr]["children"] = []
			clipidctrnow = clipidctr
			for c in tags[lparam]["children"]:
				self.CopyItem(result,c,clipidctrnow,True)
		
		def InsertItem(self,lparam,clipid=0):
			global tags, clipboard
			newitem = GetID()
			tags[lparam]["children"].append(newitem)
			tags[newitem] = deepcopy(clipboard[clipid])
			tags[newitem]["id"] = newitem
			tags[newitem]["parent"] = lparam
			tags[newitem]["children"] = []
			for c in clipboard[clipid]["children"]:
				self.InsertItem(newitem,c)

	class Tag_Editor:
		def __init__(self,parent,item,new=False):
			import time
			self.EditWindow = tk.Toplevel(parent)
			self.EditWindow.focus_set()
			self.EditWindow.transient(parent)
			if "linux" in sys.platform:
				time.sleep(0.2) #bullshit delay put in for Linux systems
			self.EditWindow.grab_set()
			self.parent = parent
			self.targettag = item
			self.new_tag = new
			self.initialize()

		def RangeCheck(self,val,nttype):
			retval = success = -1
			if nttype == LONG:
				try:
					retval = long(val)
				except ValueError:
					tkMessageBox.showinfo("Error","Could not convert value \""+val[:50]+"\" to TAG_Long")
					return (retval, success)
			elif nttype == INT:
				try:
					retval = int(val)
				except ValueError:
					tkMessageBox.showinfo("Error","Could not convert value \""+val[:50]+"\" to TAG_Int")
					return (retval, success)
				if retval > 2147483647:
					retval = 2147483647
				elif retval < -2147483648:
					retval = -2147483648
			elif nttype == SHORT:
				try:
					retval = int(val)
				except ValueError:
					tkMessageBox.showinfo("Error","Could not convert value \""+val[:50]+"\" to TAG_Short")
					return (retval, success)
				if retval > 32767:
					retval = 32767
				elif retval < -32768:
					retval = -32768
			elif nttype == BYTE:
				try:
					retval = int(val)
				except ValueError:
					tkMessageBox.showinfo("Error","Could not convert value \""+val[:50]+"\" to TAG_Byte")
					return (retval, success)
				if retval > 127:
					retval = 127
				elif retval < -128:
					retval = -128
			elif nttype == DOUBLE:
				try:
					retval = float(val)
				except ValueError:
					tkMessageBox.showinfo("Error","Could not convert value \""+val[:50]+"\" to TAG_Double")
					return (retval, success)
			elif nttype == FLOAT:
				try:
					retval = float(val)
				except ValueError:
					tkMessageBox.showinfo("Error","Could not convert value \""+val[:50]+"\" to TAG_Float")
					return (retval, success)
			elif nttype == INT_ARRAY:
				newarray = []
				for parts in val.split(","):
					newval, success = self.RangeCheck(parts,INT)
					if success == -1:
						return (-1,-1)
					newarray.append(str(newval))
				retval = ",".join(newarray)
			elif nttype == BYTE_ARRAY:
				newarray = []
				for parts in val.split(","):
					newval, success = self.RangeCheck(parts,UBYTE)
					if success == -1:
						return (-1,-1)
					newarray.append(str(newval))
				retval = ",".join(newarray)
			elif nttype == UBYTE:
				try:
					retval = int(val)
				except ValueError:
					tkMessageBox.showinfo("Could not convert value \""+val[:50]+"\" to unsigned TAG_Byte")
					return (retval, success)
				if retval > 255:
					retval = 255
				elif retval < 0:
					retval = 0
			return (retval, 1)

		def initialize(self):
			global tags, targettag
			self.EditWindow.grid()
			self.EditWindow.title("Edit Tag")
			
			self.radiovar = tk.IntVar()
			self.radios = {}

			self.radios[0] = tk.Radiobutton(self.EditWindow, variable=self.radiovar, value=COMPOUND, text="Compound", command=self.OnSelectionChange) 
			self.radios[1] = tk.Radiobutton(self.EditWindow, variable=self.radiovar, value=LIST, text="List", command=self.OnSelectionChange)
			self.radios[2] = tk.Radiobutton(self.EditWindow, variable=self.radiovar, value=LONG, text="Long", command=self.OnSelectionChange)
			self.radios[3] = tk.Radiobutton(self.EditWindow, variable=self.radiovar, value=INT, text="Int", command=self.OnSelectionChange)
			self.radios[4] = tk.Radiobutton(self.EditWindow, variable=self.radiovar, value=SHORT, text="Short", command=self.OnSelectionChange)
			self.radios[5] = tk.Radiobutton(self.EditWindow, variable=self.radiovar, value=BYTE, text="Byte", command=self.OnSelectionChange)
			self.radios[6] = tk.Radiobutton(self.EditWindow, variable=self.radiovar, value=DOUBLE, text="Double", command=self.OnSelectionChange)
			self.radios[7] = tk.Radiobutton(self.EditWindow, variable=self.radiovar, value=FLOAT, text="Float", command=self.OnSelectionChange)
			self.radios[8] = tk.Radiobutton(self.EditWindow, variable=self.radiovar, value=INT_ARRAY, text="Int_Array", command=self.OnSelectionChange)
			self.radios[9] = tk.Radiobutton(self.EditWindow, variable=self.radiovar, value=BYTE_ARRAY, text="Byte_Array", command=self.OnSelectionChange)
			self.radios[10] = tk.Radiobutton(self.EditWindow, variable=self.radiovar, value=STRING, text="String", command=self.OnSelectionChange)
			
			self.radios[0].grid(column=0,row=0,sticky="W")
			self.radios[1].grid(column=0,row=1,sticky="W")
			self.radios[2].grid(column=1,row=0,sticky="W")
			self.radios[3].grid(column=1,row=1,sticky="W")
			self.radios[4].grid(column=2,row=0,sticky="W")
			self.radios[5].grid(column=2,row=1,sticky="W")
			self.radios[6].grid(column=3,row=0,sticky="W")
			self.radios[7].grid(column=3,row=1,sticky="W")
			self.radios[8].grid(column=4,row=0,sticky="W")
			self.radios[9].grid(column=4,row=1,sticky="W")
			self.radios[10].grid(column=5,row=0,sticky="W")
			
			self.radios[STRING].select()
			if not self.new_tag:
				if tags[self.targettag]["type"] in (COMPOUND,LIST):
					for a in xrange(len(self.radios)):
						if a != tags[self.targettag]["type"]:
							self.radios[a].config(state=tk.DISABLED)
				self.radios[tags[self.targettag]["type"]].select()
			else:
				if tags[self.targettag]["type"] == COMPOUND:
					pass
				elif tags[self.targettag]["type"] == LIST:
					if tags[self.targettag]["children"]:
						self.radios[tags[tags[self.targettag]["children"][0]]["type"]].select()
						for a in xrange(len(self.radios)):
							if a != tags[tags[self.targettag]["children"][0]]["type"]:
								self.radios[a].config(state=tk.DISABLED)
				elif tags[tags[self.targettag]["parent"]]["type"] == LIST:
					self.radios[tags[self.targettag]["type"]].select()
					for a in xrange(len(self.radios)):
						if a != tags[self.targettag]["type"]:
							self.radios[a].config(state=tk.DISABLED)
					targettag = self.targettag = tags[self.targettag]["parent"]
				elif tags[tags[self.targettag]["parent"]]["type"] == COMPOUND:
					targettag = self.targettag = tags[self.targettag]["parent"]
			
			self.Formatted = tk.IntVar()
			self.FormatCheckbox = tk.Checkbutton(self.EditWindow, text="Format Command", variable=self.Formatted, command=self.DoFormat)
			self.FormatCheckbox.grid(column=5,row=2,sticky="W")
			self.Hex = tk.IntVar()
			self.HexCheckbox = tk.Checkbutton(self.EditWindow, text="Hexadecimal", variable=self.Hex, command=self.DoHex)
			self.HexCheckbox.grid(column=5,row=1,sticky="W")
			if tags[self.targettag]["type"] != STRING:
				self.FormatCheckbox.config(state=tk.DISABLED)

			self.NameLabel = tk.Label(self.EditWindow,text="Tag Name:")
			self.NameLabel.grid(column=0,row=2,sticky="N")
			self.NameVal = tk.Entry(self.EditWindow)
			self.NameVal.grid(column=1,row=2,sticky="EW",columnspan=4)

			self.ValLabel = tk.Label(self.EditWindow,text="Tag Value:")
			self.ValLabel.grid(column=0,row=3,sticky="N")
			ysb = ttk.Scrollbar(self.EditWindow, orient="vertical")
			self.ValVal = tk.Text(self.EditWindow,yscrollcommand=ysb.set)
			ysb.config(command=self.ValVal.yview)
			self.ValVal.grid(column=1,row=3,sticky="EW",rowspan=6,columnspan=5)
			ysb.grid(column=6, row=3, sticky="WNS",rowspan=6)
			
			if not self.new_tag:
				if tags[tags[self.targettag]["parent"]]["type"] != LIST:
					self.NameVal.insert(0,tags[self.targettag]["name"])

				if tags[self.targettag]["type"] not in (COMPOUND,LIST):
					self.ValVal.insert("1.0",tags[self.targettag]["value"])

			done_button = tk.Button(self.EditWindow,text=u"Done", command=self.OnDone)
			done_button.grid(column=0,row=4,sticky="EWN")
			cancel_button = tk.Button(self.EditWindow,text=u"Cancel", command=self.OnCancel)
			cancel_button.grid(column=0,row=5,sticky="EWN")
			
			placeholder = tk.Label(self.EditWindow, text=" ")
			placeholder.grid(column=0,row=6,sticky="EWN")

			self.SectionButton = tk.Button(self.EditWindow,text=u"\xa7", command=self.DoSection)
			self.SectionButton.grid(column=0,row=7,sticky="EWN")
			
			self.EditWindow.grid_rowconfigure(7,weight=1,minsize=300)
			self.EditWindow.grid_columnconfigure(7,weight=1)

			self.EditWindow.bind("<Escape>", self.OnCancel)
			self.ValVal.bind("<Control-a>", self.SelAll)
			self.EditWindow.bind("<Control-a>", self.SelAll)

			self.EditWindow.resizable(False,False)
			self.EditWindow.update()
			self.EditWindow.geometry(self.EditWindow.geometry())
			self.OnSelectionChange()
			if self.new_tag:
				if tags[self.targettag]["type"] == LIST:
					self.NameVal.config(state=tk.DISABLED)

		def OnCancel(self,*args):
			self.EditWindow.destroy()
		def OnDone(self,*args):
			global newtag, tags
			nameval = self.NameVal.get()
			if nameval == "":
				if (self.new_tag and tags[self.targettag]["type"] != LIST) or (not self.new_tag and tags[tags[self.targettag]["parent"]]["type"] != LIST):
					tkMessageBox.showinfo("Error","No name provided!")
					return
			elif self.new_tag and tags[targettag]["type"] == COMPOUND:
				for tag in tags[targettag]["children"]:
					if tags[tag]["name"] == nameval:
						tkMessageBox.showinfo("Error","There is already a \""+nameval+"\" tag! All tag names must be unique within a Compound tag!")
						return
				
			if not self.new_tag and tags[tags[targettag]["parent"]]["type"] == COMPOUND:
				if tags[targettag]["name"] != nameval:
					for tag in tags[tags[targettag]["parent"]]["children"]:
						if tags[tag]["name"] == nameval:
							tkMessageBox.showinfo("Error","There is already a \""+nameval+"\" tag! All tag names must be unique within a Compound tag!")
							return
			valval = self.ValVal.get(1.0, tk.END)

			if valval[-1] == "\n": #strip off annoying newline placed at the end
				valval = valval[:-1]

			if self.Hex.get():
				valval = re.sub("[^0-9A-Fa-f,+-]","",valval)
				vals = valval.split(",")
				vals = ["0" if v == "" else v for v in vals]
				valval = unicode(",".join([str(int(v,16)) for v in vals]))
				
			if self.Formatted.get():
				valval = strcollapse(valval.split("\n"))

			nttype = self.radiovar.get()
			if nttype in (COMPOUND, LIST):
				newval = 0
			elif nttype == STRING:
				newval = valval
			else:
				newval, result = self.RangeCheck(valval, nttype)
				if result == -1:
					return 1
			newtag = [nameval,newval,nttype]
			self.EditWindow.destroy()

		def SelAll(self,*args):
			self.ValVal.tag_add(tk.SEL, "1.0", tk.END)
			self.ValVal.mark_set(tk.INSERT, "1.0")
			self.ValVal.see(tk.INSERT)

		def DoSection(self,*args):
			self.ValVal.insert(tk.INSERT, u"\xa7")
			self.ValVal.focus_set()

		def DoFormat(self,*args):
			valval = self.ValVal.get(1.0, tk.END)
			if not self.Formatted.get():
				self.ValVal.delete("1.0", tk.END)
				self.ValVal.insert("1.0", unicode(strcollapse(valval.split("\n"))))
			else:
				newvalue = ""
				if "{" in valval:
					mdatapos = valval.find("{")
					if mdatapos == 0:
						newvalue += "\n".join(strexplode(valval))
					else:
						newvalue += valval[:mdatapos]+"\n"+"\n".join(strexplode(valval[mdatapos:]))
				else:
					newvalue = valval
				self.ValVal.delete("1.0", tk.END)
				self.ValVal.insert("1.0", newvalue)
			self.ValVal.focus_set()

		def DoHex(self,*args):
			valval = self.ValVal.get(1.0, tk.END)
			if self.Hex.get():
				valval = re.sub("[^0-9,+-]","",valval)
			else:
				valval = re.sub("[^0-9A-Fa-f,+-]","",valval)
			vals = valval.split(",")
			vals = ["0" if v == "" else v for v in vals]

			try:
				newval = [format(int(v),"X") if self.Hex.get() else str(int(v,16)) for v in vals]
			except ValueError:
				tkMessageBox.showinfo("Error","Unable to convert value!")
				self.HexCheckbox.toggle()
				return

			newval = unicode(",".join(newval))
			self.ValVal.delete("1.0", tk.END)
			self.ValVal.insert("1.0",newval)
			self.ValVal.focus_set()


		def OnSelectionChange(self,*args):
			newsel = self.radiovar.get()
			valval = self.ValVal.get(1.0, tk.END)

			if self.Hex.get():
				valval = re.sub("[^0-9A-Fa-f,+-]","",valval)
				vals = valval.split(",")
				vals = ["0" if v == "" else v for v in vals]
				newval = [str(int(v,16)) for v in vals]
				newval = unicode(",".join(newval))
				self.ValVal.delete("1.0", tk.END)
				self.ValVal.insert("1.0",newval)
				self.HexCheckbox.deselect()

			if self.Formatted.get():
				valval = unicode(strcollapse(valval.split("\n")))
				self.ValVal.delete("1.0", tk.END)
				self.ValVal.insert("1.0", valval)
				self.FormatCheckbox.deselect()

			if newsel in (COMPOUND,LIST):
				self.ValLabel.config(state=tk.DISABLED)
				self.ValVal.config(state=tk.DISABLED)
				self.FormatCheckbox.config(state=tk.DISABLED)
				self.HexCheckbox.config(state=tk.DISABLED)
				self.SectionButton.config(state=tk.DISABLED)

			else:
				self.ValLabel.config(state=tk.NORMAL)
				self.ValVal.config(state=tk.NORMAL)

				if newsel == STRING:
					self.FormatCheckbox.config(state=tk.NORMAL)
					self.EditWindow.unbind("<Return>")
					self.ValVal.unbind("<Return>")
					self.SectionButton.config(state=tk.NORMAL)
				else:
					self.EditWindow.bind("<Return>", self.OnDone)
					self.ValVal.bind("<Return>", self.OnDone)
					self.FormatCheckbox.config(state=tk.DISABLED)
					self.SectionButton.config(state=tk.DISABLED)

			if newsel in (COMPOUND,LIST): #select the correct edit box and select/deselect text
				self.NameVal.focus_set()
				self.NameVal.select_range(0, tk.END)
				self.ValVal.tag_add(tk.SEL, "1.0", "1.0")
				self.ValVal.mark_set(tk.INSERT, "1.0")
				self.ValVal.see(tk.INSERT)

			else:
				self.NameVal.select_clear()
				self.ValVal.focus_set()
				if newsel != STRING:
					self.ValVal.tag_add(tk.SEL, "1.0", tk.END)
					self.ValVal.mark_set(tk.INSERT, "1.0")
					self.ValVal.see(tk.INSERT)
			if newsel in (BYTE,SHORT,INT,LONG,INT_ARRAY,BYTE_ARRAY):
				self.HexCheckbox.config(state=tk.NORMAL)
			else:
				self.HexCheckbox.config(state=tk.DISABLED)

	class Clipboard_Viewer:
		def __init__(self,parent,value):
			self.ViewWindow = tk.Toplevel(parent)
			self.ViewWindow.focus_set()
			self.ViewWindow.transient(parent)
			self.ViewWindow.grab_set()
			self.parent = parent
			self.val = value
			self.initialize()

		def initialize(self):
			global tags, targettag
			self.ViewWindow.minsize(420,400)
			self.ViewWindow.grid()
			self.ViewWindow.title("View Clipboard (Read Only)")
			
			ysb = ttk.Scrollbar(self.ViewWindow, orient="vertical")
			self.ValVal = tk.Text(self.ViewWindow,yscrollcommand=ysb.set)
			ysb.config(command=self.ValVal.yview)
			self.ValVal.grid(column=0,row=0,sticky="EW")
			ysb.grid(column=1, row=0, sticky="WNS")
			self.ValVal.insert("1.0",self.val)

			self.ViewWindow.bind("<Escape>", self.OnClose)
			self.ViewWindow.resizable(False,False)
			self.ViewWindow.update()
			self.ViewWindow.geometry(self.ViewWindow.geometry())

		def OnClose(self,*args):
			self.ViewWindow.destroy()

	class Find_Tag:
		def __init__(self,parent):
			self.FindWindow = tk.Toplevel(parent)
			self.FindWindow.focus_set()
			self.initialize()

		def initialize(self):
			global tags, targettag
			self.FindWindow.grid()
			self.FindWindow.title("Find Tag")
			
			self.checkvars = []
			for i in xrange(STRING+1):
				self.checkvars.append(tk.IntVar())
			self.checks = {}

			self.checks[0] = tk.Checkbutton(self.FindWindow, variable=self.checkvars[0], text="Compound") 
			self.checks[1] = tk.Checkbutton(self.FindWindow, variable=self.checkvars[1], text="List")
			self.checks[2] = tk.Checkbutton(self.FindWindow, variable=self.checkvars[2], text="Long")
			self.checks[3] = tk.Checkbutton(self.FindWindow, variable=self.checkvars[3], text="Int")
			self.checks[4] = tk.Checkbutton(self.FindWindow, variable=self.checkvars[4], text="Short")
			self.checks[5] = tk.Checkbutton(self.FindWindow, variable=self.checkvars[5], text="Byte")
			self.checks[6] = tk.Checkbutton(self.FindWindow, variable=self.checkvars[6], text="Double")
			self.checks[7] = tk.Checkbutton(self.FindWindow, variable=self.checkvars[7], text="Float")
			self.checks[8] = tk.Checkbutton(self.FindWindow, variable=self.checkvars[8], text="Int_Array")
			self.checks[9] = tk.Checkbutton(self.FindWindow, variable=self.checkvars[9], text="Byte_Array")
			self.checks[10] = tk.Checkbutton(self.FindWindow, variable=self.checkvars[10], text="String")
			
			self.checks[0].grid(column=0,row=0,sticky="W")
			self.checks[1].grid(column=0,row=1,sticky="W")
			self.checks[2].grid(column=1,row=0,sticky="W")
			self.checks[3].grid(column=1,row=1,sticky="W")
			self.checks[4].grid(column=2,row=0,sticky="W")
			self.checks[5].grid(column=2,row=1,sticky="W")
			self.checks[6].grid(column=3,row=0,sticky="W")
			self.checks[7].grid(column=3,row=1,sticky="W")
			self.checks[8].grid(column=4,row=0,sticky="W")
			self.checks[9].grid(column=4,row=1,sticky="W")
			self.checks[10].grid(column=5,row=0,sticky="W")
			
			self.NameLabel = tk.Label(self.FindWindow,text="Tag Name:")
			self.NameLabel.grid(column=0,row=2,sticky="N")
			self.NameVal = tk.Entry(self.FindWindow)
			self.NameVal.grid(column=1,row=2,sticky="EW",columnspan=5)

			self.ValLabel = tk.Label(self.FindWindow,text="Tag Value:")
			self.ValLabel.grid(column=0,row=3,sticky="N")
			ysb = ttk.Scrollbar(self.FindWindow, orient="vertical")
			self.ValVal = tk.Text(self.FindWindow,yscrollcommand=ysb.set, width=60,height=6)
			ysb.config(command=self.ValVal.yview)
			self.ValVal.grid(column=1,row=3,sticky="EW",rowspan=3,columnspan=5)
			ysb.grid(column=6, row=3, sticky="WNS",rowspan=3)
			
			find_button = tk.Button(self.FindWindow,text=u"Find", command=self.OnFind)
			find_button.grid(column=7,row=4,sticky="EWS")
			cancel_button = tk.Button(self.FindWindow,text=u"Cancel", command=self.OnCancel)
			cancel_button.grid(column=0,row=5,sticky="EWS")
			
			self.DoMatchCase = tk.IntVar()
			self.ExactName = tk.IntVar()
			self.ExactValue = tk.IntVar()
			self.DoMatchCaseButton = tk.Checkbutton(self.FindWindow, variable=self.DoMatchCase, text="Match Case")
			self.ExactNameButton = tk.Checkbutton(self.FindWindow, variable=self.ExactName, text="Exact Match")
			self.ExactValueButton = tk.Checkbutton(self.FindWindow, variable=self.ExactValue, text="Exact Match")
			self.DoMatchCaseButton.grid(column=7,row=5,sticky="EWS")
			self.ExactNameButton.grid(column=7,row=2,sticky="EWN")
			self.ExactValueButton.grid(column=7,row=3,sticky="EWN")
			self.FindWindow.bind("<Escape>", self.OnCancel)

			self.FindWindow.resizable(False,False)
			self.FindWindow.update()
			self.FindWindow.geometry(self.FindWindow.geometry())

		def OnCancel(self,*args):
			global FindHandle
			FindHandle = None
			self.FindWindow.destroy()

		def OnFind(self,*args):
			global tags, targettag
			if targettag == None:
				targettag = 0
			taglist = []
			for button in self.checkvars:
				if button.get():
					taglist.append(self.checkvars.index(button))
			if not taglist:
				taglist = range(11)
			name = self.NameVal.get()
			if not self.DoMatchCase.get():
				name = name.upper()
			value = self.ValVal.get(1.0, tk.END)
			if value[-1] == "\n":
				value = value[:-1]
			if not self.DoMatchCase.get():
				value = value.upper()
			found = self.FindTag(name, value, taglist, self.DoMatchCase.get(), self.ExactName.get(), self.ExactValue.get(), targettag, targettag)
			if found != -1:
				TreeHandle.selection_set(found)
				TreeHandle.see(found)
				TreeHandle.focus_set()
			else:
				tkMessageBox.showinfo("404","No matching item found.")

		def FindTag(self,name, value, taglist, MatchCase, ExactName, ExactValue, item, start):
			global tags
			if item == -1:
				return -1
			result = self.SearchDown(name, value, taglist, MatchCase, ExactName, ExactValue, item, start)
			if result != -1:
				return result
			return self.FindTag(name, value, taglist, MatchCase, ExactName, ExactValue, self.SearchUp(item), start)

		def TestItem(self, name, value, taglist, MatchCase, ExactName, ExactValue, item):
			global tags
			if item == -1:
				return -1
			nameval = tags[item]["name"]
			if isinstance(nameval, (int, long)):
				nameval = ""
			valval = unicode(tags[item]["value"])
			if not MatchCase:
				nameval = nameval.upper()
				valval = valval.upper()
				
			if tags[item]["type"] in taglist:
				if ExactName:
					if name == "":
						if value == "":
							return item
						if ExactValue:
							if valval == value:
								return item
						else:
							if value in valval:
								return item
					elif nameval == name:
						if value == "":
							return item
						if tags[item]["type"] in (COMPOUND,LIST):
							return item
						if ExactValue:
							if valval == value:
								return item
						else:
							if value in valval:
								return item
				else:
					if name == "":
						if value == "":
							return item
						if ExactValue:
							if valval == value:
								return item
						else:
							if value in valval:
								return item
					elif name in nameval:
						if value == "":
							return item
						if tags[item]["type"] in (COMPOUND,LIST):
							return item
						if ExactValue:
							if valval == value:
								return item
						else:
							if value in valval:
								return item
			return -1

		def SearchDown(self,name, value, taglist, MatchCase, ExactName, ExactValue, item, start):
			global tags
			if item == -1:
				return -1
			if item == start: #crappy hack to search after the currently-selected item.
				result = -1
			else:
				result = self.TestItem(name, value, taglist, MatchCase, ExactName, ExactValue, item)
			if result != -1:
				return result
			else:
				for c in tags[item]["children"]:
					result = self.SearchDown(name, value, taglist, MatchCase, ExactName, ExactValue, c, start)
					if result != -1:
						return result
				else:
					return -1

		def SearchUp(self,item):
			global tags
			if item == -1:
				return -1
			parent = tags[item]["parent"]
			if parent == None or parent == "":
				return -1
			if tags[parent]["children"].index(item) != len(tags[parent]["children"])-1:
				return tags[parent]["children"][tags[parent]["children"].index(item)+1]
			else:
				return self.SearchUp(parent)

def GetPosition(value):
	global tags
	newlist = []
	x = y = z = 0
	if tags[value]["type"] == COMPOUND:
		for a in tags[value]["children"]:
			if tags[a]["name"] == "x":
				x = tags[a]["value"]
			elif tags[a]["name"] == "y":
				y = tags[a]["value"]
			elif tags[a]["name"] == "z":
				z = tags[a]["value"]
			elif tags[a]["name"] == "Pos":
				(x,y,z) = GetPosition(a)
	elif tags[value]["type"] == LIST:
		x = tags[tags[value]["children"][0]]["value"]
		y = tags[tags[value]["children"][1]]["value"]
		z = tags[tags[value]["children"][2]]["value"]
	return (x,y,z)

def perform(level, box, options):
	global idcounter, clipboard, tags, FindHandle, TreeHandle

	tileentstodelete = []
	entstodelete = []
	tickstodelete = []
	tags = {}
	if options["Edit..."] == "Selection":
		tags[1] = deepcopy(template)
		tags[1]["type"] = COMPOUND
		tags[1]["name"] = "Selection: ("+str(box.minx)+", "+str(box.miny)+", "+str(box.minz)+") to ("+str(box.maxx-1)+", "+str(box.maxy-1)+", "+str(box.maxz-1)+")"
		tags[1]["children"] = [2,3,4]
		tags[1]["id"] = 1
		
		tags[2] = deepcopy(template)
		tags[2]["type"] = LIST
		tags[2]["name"] = "TileEntities"
		tags[2]["parent"] = 1
		tags[2]["id"] = 2
		
		tags[3] = deepcopy(template)
		tags[3]["type"] = LIST
		tags[3]["name"] = "Entities"
		tags[3]["parent"] = 1
		tags[3]["id"] = 3
		
		tags[4] = deepcopy(template)
		tags[4]["type"] = LIST
		tags[4]["name"] = "TileTicks"
		tags[4]["parent"] = 1
		tags[4]["id"] = 4
		idcounter = 4

		for (chunk, _, _) in level.getChunkSlices(box):
			for e in chunk.TileEntities:
				x = e["x"].value
				y = e["y"].value
				z = e["z"].value
				if (x,y,z) in box:
					tileentstodelete.append((chunk,e))
					new_tag = GetID()
					tags[new_tag] = NewTag(0,None,new_tag,COMPOUND,2,[])
					tags[2]["children"].append(new_tag)
					Deserialize(e, new_tag)
			for e in chunk.Entities:
				x = e["Pos"][0].value
				y = e["Pos"][1].value
				z = e["Pos"][2].value
				if (x,y,z) in box:
					entstodelete.append((chunk,e))
					new_tag = GetID()
					tags[new_tag] = NewTag(0,None,new_tag,COMPOUND,3,[])
					tags[3]["children"].append(new_tag)
					Deserialize(e, new_tag)
			if "TileTicks" in chunk.root_tag["Level"]:
				for e in chunk.root_tag["Level"]["TileTicks"]:
					x = e["x"].value
					y = e["y"].value
					z = e["z"].value
					if (x,y,z) in box:
						tickstodelete.append((chunk,e))
						new_tag = GetID()
						tags[new_tag] = NewTag(0,None,new_tag,COMPOUND,4,[])
						tags[4]["children"].append(new_tag)
						Deserialize(e, new_tag)
						
		tags[2]["children"] = sorted(tags[2]["children"], key=lambda x: GetPosition(x))
		tags[3]["children"] = sorted(tags[3]["children"], key=lambda x: GetPosition(x))
		tags[4]["children"] = sorted(tags[4]["children"], key=lambda x: GetPosition(x))

		picklefile = open(temppath,"w")
		pickle.dump(tags,picklefile) #not using cPickle because there are unicode objects in the dictionary
		picklefile.close()
		if sys.platform == "win32":
			os.system("python.exe \""+os.path.join(mcplatform.filtersDir, "NBT_Multi.py\""))
		else:
			os.system("env -i /usr/bin/python \""+os.path.join(mcplatform.filtersDir, "NBT_Multi.py\""))

		picklefile = open(temppath,"r")
		tags = pickle.load(picklefile) #not using cPickle because there are unicode objects in the dictionary
		picklefile.close()

		if "Cancelled" in tags:
			raise Exception("Edit operation was canceled; no changes were made.")

		if 2 in tags:
			tileentities = GetNBT(tags[2])
		else:
			tileentities = []
		if 3 in tags:
			entities = GetNBT(tags[3])
		else:
			entities = []
		if 4 in tags:
			tick = GetNBT(tags[4])
		else:
			tick = []

		for (chunk, entity) in tileentstodelete:
			chunk.TileEntities.remove(entity)
			chunk.dirty = True
		for (chunk, entity) in entstodelete:
			chunk.Entities.remove(entity)
			chunk.dirty = True
		for (chunk, entity) in tickstodelete:
			chunk.root_tag["Level"]["TileTicks"].remove(entity)
			chunk.dirty = True
			
		for te in tileentities:
			if "x" in te and "y" in te and "z" in te:
				x = te["x"].value
				z = te["z"].value
				chunk = level.getChunk(x>>4, z>>4)
				chunk.TileEntities.append(te)
				chunk.dirty = True
		for e in entities:
			if "Pos" in e:
				if len(e["Pos"]) >= 3:
					x = e["Pos"][0].value
					z = e["Pos"][2].value
					x = int(x)>>4
					z = int(z)>>4
					chunk = level.getChunk(x, z)
					chunk.Entities.append(e)
					chunk.dirty = True
		for t in tick:
			if "x" in t and "y" in t and "z" in t:
				x = t["x"].value
				z = t["z"].value
				chunk = level.getChunk(x>>4, z>>4)
				if "TileTicks" not in chunk.root_tag["Level"]:
					chunk.root_tag["Level"]["TileTicks"] = TAG_List()
				chunk.root_tag["Level"]["TileTicks"].append(t)
				chunk.dirty = True
	elif options["Edit..."] == "File":
		if sys.platform == "win32":
			os.system("python.exe \""+os.path.join(mcplatform.filtersDir, "NBT_Multi.py\" open "+(mcplatform.lastSchematicsDir or mcplatform.schematicsDir)))
		else:
			os.system("env -i /usr/bin/python \""+os.path.join(mcplatform.filtersDir, "NBT_Multi.py\" open "+(mcplatform.lastSchematicsDir or mcplatform.schematicsDir)))

		filename = GetValue()
		if filename == "Error":
			filename = mcplatform.askOpenFile(title="Select a Schematic or Dat File...", schematics=False)
		if filename == None or filename == "":
			raise Exception("No file name provided.")

		if filename:
			buf = file(filename, "rb")
		if hasattr(buf, "read"):
			buf = buf.read()

		compressed = True
		try:
			buf = gzip.GzipFile(fileobj=StringIO(buf)).read()
		except IOError, zlib.error:
			compressed = False

		if isinstance(buf, str):
			buf = numpy.fromstring(buf, 'uint8')
		data = buf

		if not len(data):
			raise nbt.NBTFormatError("Asked to load root tag of zero length")

		tag_type = data[0]
		if tag_type != 10:
			raise nbt.NBTFormatError("Incorrectly formatted data file!")
			
		tags[1] = deepcopy(template)
		tags[1]["type"] = COMPOUND
		tags[1]["name"] = filename
		idcounter = 1
		Deserialize(nbt.load(filename), 1)
		
		picklefile = open(temppath,"w")
		pickle.dump(tags,picklefile) #not using cPickle because there are unicode objects in the dictionary
		picklefile.close()
		if sys.platform == "win32":
			os.system("python.exe \""+os.path.join(mcplatform.filtersDir, "NBT_Multi.py\""))
		else:
			os.system("env -i /usr/bin/python \""+os.path.join(mcplatform.filtersDir, "NBT_Multi.py\""))

		picklefile = open(temppath,"r")
		tags = pickle.load(picklefile) #not using cPickle because there are unicode objects in the dictionary
		picklefile.close()

		if "Cancelled" in tags:
			raise Exception("Edit operation was canceled; no changes were made.")
			
		tags[1]["name"] = 0
		
		if sys.platform == "win32":
			os.system("python.exe \""+os.path.join(mcplatform.filtersDir, "NBT_Multi.py\" save "+filename))
		else:
			os.system("env -i /usr/bin/python \""+os.path.join(mcplatform.filtersDir, "NBT_Multi.py\" save "+filename))

		filename = GetValue()
		
		if filename == "Error":
			filename = mcplatform.askSaveFile(os.path.split(filename)[0], "Save File...", "", "File\0*.*\0\0", os.path.basename(filename))
		if filename == None or filename == "":
			raise Exception("No file name provided.")
		data_file = deepcopy(Serialize(tags,1,TAG_Compound()))
		data_file.save(filename,compressed)
		raise Exception("File Saved.")

	elif options["Edit..."] == "level.dat":
		tags[1] = deepcopy(template)
		tags[1]["type"] = COMPOUND
		tags[1]["name"] = "level.dat"
		idcounter = 1
		Deserialize(level.root_tag, 1)

		picklefile = open(temppath,"w")
		pickle.dump(tags,picklefile) #not using cPickle because there are unicode objects in the dictionary
		picklefile.close()

		if sys.platform == "win32":
			os.system("python.exe \""+os.path.join(mcplatform.filtersDir, "NBT_Multi.py\""))
		else:
			os.system("env -i /usr/bin/python \""+os.path.join(mcplatform.filtersDir, "NBT_Multi.py\""))

		picklefile = open(temppath,"r")
		tags = pickle.load(picklefile) #not using cPickle because there are unicode objects in the dictionary
		picklefile.close()

		if "Cancelled" in tags:
			raise Exception("Edit operation was canceled; no changes were made.")
		
		level.root_tag = deepcopy(Serialize(tags,2,TAG_Compound()))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		if len(sys.argv) > 2:
			path = sys.argv[2]
		else:
			path = ""

		if sys.argv[1] == "open":
			SetValue(tkf.askopenfilename(title="Open NBT data file...", filetypes = (("Schematic", "*.schematic"),("NBT Dat", "*.dat"),("All files", "*.*")), initialdir=path))
		elif sys.argv[1] == "save":
			if path != "":
				file_name = os.path.basename(path)
			else:
				file_name = ""
			path = os.path.split(path)[0]
			SetValue(tkf.asksaveasfilename(title="Save file as...", filetypes = (("Schematic", "*.schematic"),("NBT Dat", "*.dat"),("All files", "*.*")), initialfile=file_name, initialdir=path))
		exit()
	else:
		picklefile = open(temppath,"r")
		tags = pickle.load(picklefile) #not using cPickle because there are unicode objects in the dictionary
		picklefile.close()

		app = NBT_Editor(None)
		app.title("NBT Editor")
		app.mainloop()

		picklefile = open(temppath,"w")
		pickle.dump(tags,picklefile) #not using cPickle because there are unicode objects in the dictionary
		picklefile.close()

