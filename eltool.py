#!/usr/bin/env python3
import tkinter
import requests
from bs4 import BeautifulSoup
from gifplayer import GIFPlayer
from functools import partial as bind
from tkinter import filedialog, colorchooser

try:
	import winsound
except:
	winsound = None


class ELTool:
	partID = 176925
	donations = []
	donationsQueue = []
	player_win = None
	player = None
	wav_file = None
	total = 0.0
	text_color = "#ffffff"
	back_color = "#00ff00"
	is_started = False

	def __init__( self ):
		self.root = tkinter.Tk()
		self.root.wm_title( "ELTool Control" )

		self.pick_gif_button = tkinter.Button( self.root, text="Pick GIF", command=self.pick_gif, width=10 )
		self.pick_wav_button = tkinter.Button( self.root, text="Pick WAV", command=self.pick_wav, width=10 )
		self.back_color_button = tkinter.Button( self.root, text="Back Color", command=self.pick_back_color, width=10 )
		self.text_color_button = tkinter.Button( self.root, text="Text Color", command=self.pick_text_color, width=10 )
		self.player_id_label = tkinter.Label( self.root, text="ID:" )
		self.player_id_entry = tkinter.Entry( self.root, width=20 )
		self.font_name_label = tkinter.Label( self.root, text="Font Name:" )
		self.font_name_entry = tkinter.Entry( self.root, width=20 )
		self.font_size_label = tkinter.Label( self.root, text="Font Size:" )
		self.font_size_entry = tkinter.Entry( self.root, width=20 )
		self.start_button = tkinter.Button( self.root, text="Start", command=self.start, state=tkinter.DISABLED, width=20, height=2 )
		self.test_button = tkinter.Button( self.root, text="Test", state=tkinter.DISABLED, command=bind( self.play_anim, "Goku donated $9000.01" ), width=20, height=2 )

		self.player_id_entry.insert( 0, str( self.partID ) )
		self.font_name_entry.insert( 0, "Arial" )
		self.font_size_entry.insert( 0, "20" )

		self.pick_gif_button.grid( column=0, row=0 )
		self.pick_wav_button.grid( column=0, row=1 )
		self.back_color_button.grid( column=0, row=2 )
		self.text_color_button.grid( column=0, row=3 )
		self.player_id_label.grid( column=3, row=0, sticky=tkinter.E )
		self.player_id_entry.grid( column=4, row=0 )
		self.font_name_label.grid( column=3, row=1, sticky=tkinter.E )
		self.font_name_entry.grid( column=4, row=1 )
		self.font_size_label.grid( column=3, row=2, sticky=tkinter.E )
		self.font_size_entry.grid( column=4, row=2 )
		self.start_button.grid( column=5, row=0, rowspan=2 )
		self.test_button.grid( column=5, row=2, rowspan=2 )

		self.root.mainloop()

	def check_donations( self ):
		self.partID = self.player_id_entry.get()
		r = requests.get( "http://www.extra-life.org/index.cfm?fuseaction=donorDrive.participantDonations&participantID={}".format( self.partID ) )

		bs = BeautifulSoup( r.text, "html.parser" )

		ds = bs.find_all( class_ = "donor-detail" )

		for d in ds:
			text = d.strong.string.strip()
			date = d.small.string

			if not text in self.donations:
				print( text + " on " + date )
				self.donations.append( text )
				self.donationsQueue.append( text )

				try:
					parts = text.partition( "$" )
					self.total += float( parts[2] )
				except:
					pass

		self.root.after( 10000, self.check_donations )

	def create_player_win( self ):
		if self.player_win:
			self.player_win.destroy()

		self.player_win = tkinter.Toplevel( self.root )
		self.player_win.wm_title( "ELTool Display" )
		self.player_win.grid_columnconfigure( 0, weight=1 )
		self.player_win.grid_rowconfigure( 0, weight=1 )

		self.player = GIFPlayer( self.player_win, self.gif_file )
		self.player.set_background_color( self.back_color )
		self.player.set_text_color( self.text_color )

	def start( self ):
		if self.is_started:
			self.is_started = False
			self.start_button.config( text="Start" )
		else:
			self.is_started = True
			self.start_button.config( text="Stop" )

			self.root.after( 1000, self.check_donations )
			self.root.after( 1000, self.check_queue )

	def play_anim( self, text ):
		if self.player:
			self.player.set_font( self.font_name_entry.get(), self.font_size_entry.get() )
			self.player.play( text, self.check_queue )

		if winsound and self.wav_file:
			winsound.PlaySound( self.wav_file, winsound.SND_ASYNC )
	
	def check_queue( self ):
		if not self.is_started:
			return

		if len( self.donationsQueue ) > 0:
			self.play_anim( self.donationsQueue.pop(0) )
		else:
			self.root.after( 1000, self.check_queue )

	def pick_gif( self ):
		self.gif_file = filedialog.askopenfilename( filetypes=[("GIF", "*.gif"), ], initialdir="." )
		if self.gif_file:
			self.start_button.config( state=tkinter.NORMAL )
			self.test_button.config( state=tkinter.NORMAL )
			self.create_player_win()
		else:
			self.start_button.config( state=tkinter.DISABLED )
			self.test_button.config( state=tkinter.DISABLED )

			if self.is_started:
				self.start() # Should toggle to stopped

	def pick_wav( self ):
		self.wav_file = filedialog.askopenfilename( filetypes=[("WAV", "*.wav"), ], initialdir="." )

	def pick_back_color( self ):
		self.back_color = colorchooser.askcolor()[1]
		if self.player:
			self.player.set_background_color( self.back_color )

	def pick_text_color( self ):
		self.text_color = colorchooser.askcolor()[1]
		if self.player:
			self.player.set_text_color( self.text_color )

tool = ELTool()
