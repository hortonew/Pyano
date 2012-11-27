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
playing = []

pygame.midi.init()

#size of pyano window
WINDOW_SIZE = (800, 600)

#piano input device
i = pygame.midi.Input(yamaha)

screen = pygame.display.set_mode((WINDOW_SIZE))
screen.fill((255,255,255))
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
	screen.fill((255,255,255))
	#text y location
	ht = 15
	for text in t:
		#text
		s = "%s" % [text[0], text[1]]
		data = get_text(s, (255,0,0), (255,255,255), 15, ht, 20)
		screen.blit(data[0], data[1])
		ht += 25
		
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
	
	return [notes[note-1], count]

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
			playing.append(n)
		else:
			#caused errors without catch (because of playing too fast)
			try:
				#allows for hitting a stuck note to remove all instance out of playing list
				#still need to figure out how to make sure 
				while n in playing:
					playing.remove(n)
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