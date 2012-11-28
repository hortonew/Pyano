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

#piano input device
i = pygame.midi.Input(yamaha)

screen = pygame.display.set_mode((WINDOW_SIZE))
screen.fill((126,126,126))
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
	screen.fill((126,126,126))
	#text y location
	for text in t:
		s = "%s" % text
		width_mod = t[text][2] * 50
		height_mod = t[text][1] * 25
		size_mod = t[text][4] % 10
		font_color = t[text][3]
		data = get_text(s, font_color, (126,126,126), width_mod, height_mod, 20 + size_mod)
		screen.blit(data[0], data[1])
		
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

#loop
while going:
	events = event_get()
	for e in events:
		#exit
		if e.type in [pgl.QUIT]:
			going = False
		#exit
		if e.type in [pgl.KEYDOWN]:
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
				
		#print data
		print "Note: %s, Volume: %s, Time: %s" % (n, v, mt)
		print "Playing: %s" % playing

		setText(playing)
		pygame.display.flip()
	
#remove midi object			
del i
pygame.midi.quit()