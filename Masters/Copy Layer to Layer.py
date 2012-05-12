#MenuTitle: Copy Layer to Layer
"""Copies one master to another master in selected glyphs."""

#import GlyphsApp
import vanilla

class MasterFiller(object):

	def __init__(self):
		self.w = vanilla.FloatingWindow((300, 60), "Copy layer to layer")

		self.w.text_1 = vanilla.TextBox((15, 12+2, 120, 14), "Copy paths from", sizeStyle='small')
		self.w.master_from = vanilla.PopUpButton((120, 12, 80, 17), self.GetMasterNames(), sizeStyle='small', callback=self.MasterChangeCallback)
		
		self.w.text_2 = vanilla.TextBox((15, 32+2, 120, 14), "into selection of", sizeStyle='small')
		self.w.master_into = vanilla.PopUpButton((120, 32, 80, 17), self.GetMasterNames(), sizeStyle='small', callback=self.MasterChangeCallback)
		#self.w.anchor_value.bind( "+", self.ValuePlus1 )

		self.w.copybutton = vanilla.Button((-80, 32, -15, 17), "Copy", sizeStyle='small', callback=self.buttonCallback)
		self.w.setDefaultButton( self.w.copybutton )

		self.w.open()
		self.w.master_into.set(1)
	
	def GetMasterNames(self):
		myMasterList = []

		for i in range(len(Glyphs.currentDocument.font.masters)):
			x = Glyphs.currentDocument.font.masters[i]
			myMasterList.append( '%i: %s' % (i, x.name) )
		
		return myMasterList
	
	def MasterChangeCallback(self, sender):
		if self.w.master_from.get() == self.w.master_into.get():
			self.w.copybutton.enable(False)
		else:
			self.w.copybutton.enable(True)

	def buttonCallback(self, sender):
		Doc = Glyphs.currentDocument
		selectedGlyphs = [ x.parent for x in Doc.selectedLayers() ]

		index_from = self.w.master_from.get()
		index_into = self.w.master_into.get()
				
		for thisGlyph in selectedGlyphs:
			num_from = len(thisGlyph.layers[index_from].paths)
			num_into = len(thisGlyph.layers[index_into].paths)
			
			if num_into != 0:
				print "Emptying layer"
				for i in range(len(thisGlyph.layers[index_into].paths))[::-1]:
					del thisGlyph.layers[index_into].paths[i]

			if num_from > 0:
				for thisPath in thisGlyph.layers[index_from].paths:
					newPath = GSPath()

					for n in thisPath.nodes:
						newNode = GSNode()
						newNode.type = n.type
						newNode.setPosition_((n.x, n.y))
						newPath.addNode_( newNode )

					newPath.closed = thisPath.closed
					thisGlyph.layers[index_into].paths.append( newPath )
		
		self.w.close()

MasterFiller()
