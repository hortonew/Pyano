import pygame
import pygame.locals as pgl
import pygame.midi

#ID for piano
yamaha = 1

pygame.init()
pygame.fastevent.init()
event_get = pygame.fastevent.get
event_post = pygame.fastevent.post

#current notes being played
playing = dict()

pygame.midi.init()

#size of pyano window
WINDOW_SIZE = (800, 600)
SCREEN_COLOR = (126,126,126)
STARTED = False

#piano input device
i = pygame.midi.Input(yamaha)

screen = pygame.display.set_mode((WINDOW_SIZE))

screen.fill(SCREEN_COLOR)
pygame.display.flip()

#time
mt = None
#piano loop
going = True
		
#get text pair for drawing
def get_text(text, color, bgcolor, cx, cy, size):
		font = pygame.font.Font(None, size)
		t = font.render(text, True, color, bgcolor)
		t_rect = t.get_rect()
		t_rect.centerx = cx
		t_rect.centery = cy

		return t, t_rect

#draw all the text to the screen
def setText(t):
	screen.fill(SCREEN_COLOR)
	#text y location
	for text in t:
		s = "%s" % text
		width_mod = t[text][2] * 50
		height_mod = t[text][1] * 25
		size_mod = t[text][4] % 10
		font_color = t[text][3]
		
		data = get_text(s, font_color, SCREEN_COLOR, width_mod, height_mod, 20 + size_mod)
		screen.blit(data[0], data[1])

def songText(t):
	for line in t:
		for note in line:
			print note

# convert integer into note/octave
def getNote(i):
	notes = ['A', 'A#/Bb', 'B', 'C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab']
	#Low A starts on 21
	note = i-20
	count = 1
	
	#Calculate octave
	while note > 12:
		note -= 12
		count += 1
	
	#if note is a white key
	if note in [1,3,4,6,8,9,11]:
		color = (255,255,255)
	else:
		color = (0,0,0)
	name = "%s%s" % (notes[note-1], count)
	return [name, notes[note-1], note, count, color]

def loadFile(song):
	import os
	music_dir = 'music/'
	mypath = os.path.dirname( os.path.realpath( __file__) )
	f = open(os.path.join(mypath, music_dir + song))
	return f

def playMidi():
	global STARTED
	song_notes = []
	if STARTED:
		print "Game Stop"
	else:
		print "Game Started"
		f = loadFile('1.txt')
		for line in f:
			song_notes.append(line.strip().split(','))
		songText(song_notes)
	STARTED = not STARTED
	
#loop
while going:
	events = event_get()
	for e in events:
		#exit
		if e.type in [pgl.QUIT]:
			going = False
		#exit
		if e.type in [pgl.KEYDOWN]:
			if e.unicode == 'p':
				playMidi()
			else:
				going = False
			
	if i.poll():
		midi_events = i.read(10)
		mt = pygame.midi.time()
		
		# Note / Octave
		n = getNote(midi_events[0][0][1])
		
		# Volume
		v = midi_events[0][0][2]
		
		if v != 0:
			playing[n[0]] = [n[1],n[2],n[3],n[4],v, mt]
		else:
			#caused errors without catch (because of playing too fast)
			try:
				del playing[n[0]]
			except:
				pass

		#Console output		
		print "Note: %s, Volume: %s, Time: %s" % (n, v, mt)
		print "Playing: %s" % playing
	else:
		to_delete = []
		if len(playing) > 0:
			for item in playing:
				if (pygame.midi.time()-playing[item][5]) > 1000:
					to_delete.append(item)
					print "Stuck note: %s" % item
		for item in to_delete:
			print "Deleting %s due to being stuck." % item
			del playing[item]
			
	setText(playing)
	pygame.display.flip()
	
#remove midi object			
del i
pygame.midi.quit()