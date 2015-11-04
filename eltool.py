#!/usr/bin/env python3
import tkinter
import requests
from bs4 import BeautifulSoup
from gifplayer import GIFPlayer
from functools import partial as bind
from tkinter import filedialog

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

	def __init__( self ):
		self.root = tkinter.Tk()

		self.start_button = tkinter.Button( self.root, text="Start", command=self.start, state=tkinter.DISABLED )
		self.test_button = tkinter.Button( self.root, text="Test", command=bind( self.play_anim, "Goku donated $9000.01" ) )
		self.player_id_label = tkinter.Label( self.root, text="ID" )
		self.player_id_entry = tkinter.Entry( self.root, width=10 )
		self.pick_gif_button = tkinter.Button( self.root, text="Pick GIF", command=self.pick_gif )
		self.pick_wav_button = tkinter.Button( self.root, text="Pick WAV", command=self.pick_wav )

		self.player_id_entry.insert( 0, str( self.partID ) )

		self.pick_gif_button.grid( column=0, row=0 )
		self.pick_wav_button.grid( column=1, row=0 )
		self.player_id_label.grid( column=0, row=1 )
		self.player_id_entry.grid( column=1, row=1 )
		self.test_button.grid( column=0, row=2 )
		self.start_button.grid( column=1, row=2 )

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

	def start( self ):
		if self.player_win:
			self.player_win.destroy()

		self.player_win = tkinter.Toplevel( self.root )
		self.player_win.grid_columnconfigure( 0, weight=1 )
		self.player_win.grid_rowconfigure( 0, weight=1 )

		self.player = GIFPlayer( self.player_win, self.gif_file )

		self.check_donations()
		self.check_queue()

	def play_anim( self, text ):
		if self.player:
			self.player.play( text, self.check_queue )

		if winsound and self.wav_file:
			winsound.PlaySound( self.wav_file, winsound.SND_ASYNC )
	
	def check_queue( self ):
		if len( self.donationsQueue ) > 0:
			self.play_anim( self.donationsQueue.pop(0) )
		else:
			self.root.after( 1000, self.check_queue )

	def pick_gif( self ):
		self.gif_file = filedialog.askopenfilename( filetypes=[("GIF", "*.gif"), ], initialdir="." )
		if self.gif_file:
			self.start_button.config( state=tkinter.NORMAL )

	def pick_wav( self ):
		self.wav_file = filedialog.askopenfilename( filetypes=[("WAV", "*.wav"), ], initialdir="." )


tool = ELTool()
