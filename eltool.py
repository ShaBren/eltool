#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests

partID = 176925

r = requests.get( "http://www.extra-life.org/index.cfm?fuseaction=donorDrive.participantDonations&participantID={}".format( partID ) )

bs = BeautifulSoup( r.text, "html.parser" )

ds = bs.find_all( class_ = "donor-detail" )

dl = []
for d in ds:
	t = d.strong.string
	date = d.small.string

	t = t.strip()

	dl.append( t )

	print( t + " on " + date )

total = 0.0
for d in dl:
	parts = d.partition( "$" )
	total += float( parts[2] )

print( "\nTotal: $%.02f" % total )
