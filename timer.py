#!/usr/bin/env python3
import tkinter
import time
from gifplayer import GIFPlayer
from functools import partial as bind
from tkinter import filedialog, colorchooser

try:
	import winsound
except:
	winsound = None


class ELTimer:
	player_win = None
	wav_file = None
	font_color = "#ffffff"
	current_time = 1800
	start_time = None

	def __init__( self ):
		self.root = tkinter.Tk()
		self.root.wm_title( "ELTimer Control" )

		self.pick_wav_button = tkinter.Button( self.root, text="Pick WAV", command=self.pick_wav )
		self.time_label = tkinter.Label( self.root, text="Time:" )
		self.time_entry = tkinter.Entry( self.root, width=10 )

		self.start_button = tkinter.Button( self.root, text="Start", command=self.start )
		self.stop_button = tkinter.Button( self.root, text="Stop", command=self.stop )

		self.time_entry.insert( 0, self.format_time( self.current_time ) )

		self.pick_wav_button.grid( column=0, row=0 )
		self.time_label.grid( column=0, row=1 )
		self.time_entry.grid( column=1, row=1 )
		self.start_button.grid( column=1, row=2 )
		self.stop_button.grid( column=0, row=2 )

		self.timer_win = TimerWin( self.root )
		self.timer_win.wm_title( "ELTimer" )
		self.timer_win.grid_columnconfigure( 0, weight=1 )
		self.timer_win.grid_rowconfigure( 0, weight=1 )

		self.root.mainloop()

	def start( self ):
		self.current_time = self.deformat_time( self.time_entry.get() )
		self.start_time = int( time.monotonic() )
		self.timer_win.show_time()
		self.timer_win.set_time( self.format_time( self.current_time ) )

		self.root.after( 1000, self.update_time )

	def update_time( self ):
		if not self.start_time:
			return

		ltime = self.current_time - ( int( time.monotonic() ) - self.start_time )

		self.timer_win.set_time( self.format_time( ltime ) )

		if ltime > 0:
			self.root.after( 1000, self.update_time )
		else:
			if winsound and self.wav_file:
				winsound.PlaySound( self.wav_file, winsound.SND_ASYNC )

	def stop( self ):
		self.timer_win.hide_time()
		self.start_time = None

	def deformat_time( self, time ):
		parts = time.partition( ":" )
		seconds = 0

		if len( parts[1] ):
			seconds = int( parts[0] ) * 60
			seconds += int( parts[2] )
		else:
			seconds += int( time )

		return seconds

	def format_time( self, time ):
		seconds = time % 60
		minutes = ( time / 60 ) % 60
		return "%02d:%02d" % ( minutes, seconds )

	def pick_wav( self ):
		self.wav_file = filedialog.askopenfilename( filetypes=[("WAV", "*.wav"), ], initialdir="." )
	

class TimerWin( tkinter.Toplevel ):

	def __init__( self, parent ):
		width = 400
		height = 200

		tkinter.Toplevel.__init__( self, parent, width=width, height=height, background='green' )

		self.canvas = tkinter.Canvas( self, background='green' )
		self.canvas.grid( row=0, column=0, sticky=tkinter.NSEW )

		self.text_id = self.canvas.create_text( ( width/2, height/2 ), state=tkinter.HIDDEN, font=( "Arial", 40 ), fill='#ffffff', justify=tkinter.CENTER )

	def set_time( self, time ):
		self.canvas.itemconfig( self.text_id, text=time )

	def hide_time( self ):
		self.canvas.itemconfig( self.text_id, state=tkinter.HIDDEN )

	def show_time( self ):
		self.canvas.itemconfig( self.text_id, state=tkinter.NORMAL )

tool = ELTimer()
