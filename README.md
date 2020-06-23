Creating ffmpeg daemon
======================

* Create and start the dummy_cam.service with 
.. code-block:: bash
    sudo cp dummy_cam.service /usr/lib/systemd/system/.
    sudo systemctl enable dummy_cam.service - or - sudo systemctl daemon-reload
    sudo systemctl start dummy_cam.service

Creating i3 shortcuts
=====================
Interaction with the chatgif.py script uses empty tmp files to trigger emojis
.. code-block:: bash
    bindsym $mod+p exec touch /tmp/chatgif.thumb
    bindsym $mod+l exec touch /tmp/chatgif.smile

Launching the script
====================
I did not manage to launch this one as a daemon, probably because of permissions for using the audio input. Too lazy to dig in.

TODOS
=====
* Make it stable. It crashes almost every time I trigger an emoji while the other one is not finished. I guess it should not be possible to touch a file if another is present.
* Make it nice.
* Make it smart.

Requires
========
* linux
* videoforlinux
* pyalsaaudio: `pip install pyalsaaudio`
