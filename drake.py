import pyaudio
import wave
import time
import sys
import socket

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

wf = wave.open(sys.argv[1], 'rb')

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# define callback (2)
def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)

current_rate = wf.getframerate()
delta_rates = [-1000, 1000]

# open stream using callback (3)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=current_rate,
                output=True,
                stream_callback=callback)
                
#create an INET, STREAMing socket
serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
#bind the socket to a public host,
# and a well-known port
print socket.gethostname()
serversocket.bind(("18.111.104.154", 5001))
#become a server socket
serversocket.listen(1)
(clientsocket, address) = serversocket.accept()

while True:
    returned = clientsocket.recv(1)
    print len(returned)
    print repr(returned)
    stream.close()
    current_rate += delta_rates[int(returned)]
    print current_rate
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                #rate=wf.getframerate(),
                rate=current_rate,
                output=True,
                stream_callback=callback)

#cleanup, cleanup

# stop stream (6)
stream.stop_stream()

stream.close()
wf.close()

# close PyAudio (7)
p.terminate()