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

#piano input device
i = pygame.midi.Input(yamaha)
#window = pygame.display.set_mode((468,60))

#time
mt = None
#piano loop
going = True

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
				playing.remove(n)
			except:
				pass
				
		#print data
		print "Note: %s, Volume: %s, Time: %s" % (n, v, mt)
		print "Playing: %s" % playing
		#midi_evs = pygame.midi.midis2events(midi_events, i.device_id)
		
		#for m_e in midi_evs:
			#event_post( m_e )

#remove midi object			
del i
pygame.midi.quit()