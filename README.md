
Creating i3 shortcuts
---------------------
Interaction with the chatgif.py script uses empty tmp files to trigger emojis
``` bash
bindsym $mod+p exec touch /tmp/chatgif.thumb
bindsym $mod+l exec touch /tmp/chatgif.smile
```

Creating run the script
-----------------------
`./bitizen_kam.py`


TODOS
-----
* Make it stable. It crashes almost every time I trigger an emoji while the other one is not finished. I guess it should not be possible to touch a file if another is present.
* Make it nice.
* Make it smart.

Requires
--------
* linux
* videoforlinux
* pyalsaaudio: `pip install pyalsaaudio`
* ffmpeg-python: `pip install ffmpeg-python`
* numpy: `pip install numpy`
