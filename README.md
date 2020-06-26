
Creating i3 shortcuts
---------------------
Interaction with the chatgif.py script uses empty tmp files to trigger emojis
``` bash
bindsym $mod+p exec touch /tmp/chatgif.thumb
bindsym $mod+l exec touch /tmp/chatgif.smile
```

Load v4l2loopback so it is working with google chrome
-----------------------------------------------------
clone and install v4l2loopback (centos7 example)
```
$ git clone https://github.com/umlaeute/v4l2loopback.git
$ make && sudo make install
$ sudo depmod -
$ sudo echo "v4l2loopback" > /etc/modules-load.d/v4l2loopback.conf
$ sudo echo "options v4l2loopback video_nr=0 card_label='Bitizen Kam' exclusive_caps=1" > /etc/modprobe.d/v4l2loopback.conf
```


Run the script
---------------
`./bitizen_kam.py`


TODOS
-----
* Make it nicer: add threading and change the option to interact with it without having to youch file.
* Make it smart.

Requires
--------
* linux
* videoforlinux utils `v4l-utils`
* v4l2loopback `https://github.com/umlaeute/v4l2loopback`
* pyalsaaudio: `pip install pyalsaaudio`
* ffmpeg-python: `pip install ffmpeg-python`
* numpy: `pip install numpy`
