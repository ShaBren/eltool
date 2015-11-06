#!/usr/bin/env python3
from tkinter import * 
from PIL import Image, ImageTk


class GIFPlayer( Canvas ):
	on_complete = None

	def __init__( self, parent, filename ):
		im = Image.open(filename)
		seq =  []
		self.frames = []

		try:
			while 1:
				seq.append(im.convert('RGB'))
				im.seek(len(seq))
		except EOFError:
			pass

		for image in seq:
			self.frames.append(ImageTk.PhotoImage(image))

		try:
			self.delay = im.info['duration']
		except KeyError:
			self.delay = 100

		width, height = im.size

		parent.geometry( "{}x{}".format( width, height ) )

		Canvas.__init__( self, parent, width=width, height=height, background='green' )
		self.grid( row=0, column=0, sticky=NSEW )

		self.image_id = self.create_image( ( width/2, height/2 ), image=self.frames[0], state=HIDDEN )
		self.text_id = self.create_text( ( width/2, height/2 ), state=HIDDEN, font=( "Arial", 20 ), fill='#ffffff', width=width, justify=CENTER )

		self.idx = 0

	def play( self, text, on_complete ):
		self.itemconfig( self.image_id, state=NORMAL )
		self.itemconfig( self.text_id, state=NORMAL, text=text )
		self.cancel = self.after( self.delay, self.next_frame )
		self.on_complete = on_complete

	def next_frame( self ):
		self.itemconfig( self.image_id, image=self.frames[ self.idx ] )
		self.idx += 1

		if self.idx == len( self.frames ):
			self.stop()
		else:
			self.cancel = self.after( self.delay, self.next_frame )

	def set_font( self, name, size ):
		self.itemconfig( self.text_id, font=( name, size ) )

	def set_text_color( self, color ):
		self.itemconfig( self.text_id, fill=color )

	def set_background_color( self, color ):
		self.config( background=color )

	def stop( self ):
		self.idx = 0
		self.after_cancel( self.cancel )
		self.itemconfig( self.image_id, state=HIDDEN )
		self.itemconfig( self.text_id, state=HIDDEN )

		if self.on_complete:
			self.on_complete()



