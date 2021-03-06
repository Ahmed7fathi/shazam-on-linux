# Description
Shazam runs on mobile device. No Shazam application runs on non Android linux based devices. This project uses [ACRCloud](https://www.acrcloud.com) services to detect played sound on a Linux machine.  Why is this application useful?
 * you can customize triggers that launch sound detection, e.g. : use [slack messenging](www.slack.com) bots to enable detection when you write a slack specific maessage
 * you can customize actions on music recognition: add recognized music to your playlist, share on facebook...
 * you do not have, or you cannot use your smartphone to shazam a sound
 * you are using earphone to listen your music on a device not supported by Shazam application (running Shazam on a smartphone with earphone is possible)
 * you can add this service to your preferred music server (mpd, logitechmediaserver)...

# Prerequisities
## ACRCLoud project creation
* create an account on ACRCLoud. Go to your profile -> Projects -> "Audio & Video Recognition Projects" -> "Create project". You will get a (url, key access, key secret) for . This service is FREE. 
* add (url, key access, key secret) to `./shazam_on_linux.conf`

## configure alsa / pulseaudio
Sound detection is done on current played track. In order to record (internal software record) it when it is played, without using any microphone, alsa loop module or pulse monitor must be previously configured. 
### Alsa
[Alsa loop module](https://www.alsa-project.org/main/index.php/Matrix:Module-aloop) is used to record played sound on a linux machine.
Install and configure it.

After, you will have to add an asoundrc that :
* by default, route played sound to a loop device and to your soundcard output device
* enables dmix on both loop device and soundcard output device

You will find an example configuration under `./alsa/asound_loop_dmix.conf`, use it and adapt it to your needs.
Load new settings using :

    alsactl kill rescan

Check alsa is correctly configured playing several sounds at same time:

    # use sox to play sound, force it using alsa
    export AUDIODRIVER=alsa 
    (play your_sound_1 &)  && play your_sound_2

    # record sound  
    arecord -c 2  -D loopout /tmp/test.wav
    # stop recording

    # check played sound is a mix of both sounds
    play /tmp/test.wav

# Run sound detection

    ./shazam.sh ./shazam_on_linux.conf
    # script takes more than 5s to detect sound
    # it returns info about currently played track
    Track : Do That Dance
    Artist Shit Robot feat. Nancy Whang
    Album : Do That Dance

# Use cases
## Add played music to your playlist 
Your music server runs on a linux machine (e.g. raspberry). Shazam is triggered on a user specific action. 
TODO add ring bell description
Played music is addded to mpd playlist.

# References
[alsa dmix config failing](http://raspberrypi.stackexchange.com/questions/57787/using-the-alsa-dmix-plugin-on-raspbian-jessie/61974#61974)

[alsa dmix conifg failing -> solution](http://stackoverflow.com/questions/42202282/alsa-loop-with-dmix)
