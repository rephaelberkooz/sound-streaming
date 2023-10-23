# Sound Streaming
A repository for experiments on streaming audio signals to various output modalities. 

## Contents (outdated)
 - `ln_Savanne.wav`: symlinked soundfile
 - `experiments.ipynb`: notebook for experimenting with sound manipulation
 - `server.py`: TCP socket sending audio signal to a local port
 - `client.py`: TCP socket recieving audio signal from a local port
 - `exmaple_resources/`: copied directly from elsewhere (soundfile exmaples)
 - 

## Environment
Currently using my local `franclNN` python env. Will extend soon

## For Sam
branch of main pls

Run `music_playback.py` and then `simulate_unity_tcp.py` for testing. line 45 in `music_playback.py` has a note of where I'm stuck, maybe I'm not encoding/unencoding the wav files correctly, it sounds like it's got the wrong sample rate, but 48000 is there all across the board

To Do:

Once the sounds are mixed, I'll need to make separate streams for each channel of the speaker array, and do some geometry/ambisonics to make new mixing for each of the speakers based on the coordinates that are coming in from the Unity TCP connection. 