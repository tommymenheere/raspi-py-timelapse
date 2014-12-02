Timelapse module written in Python or the Raspberry Pi.


## Configuration

Configuration is handled in the _config.ini_ file. The following sections exist:

### files

The section is used to configure all file system related settings.

root = /vol/data/tl/%Y/%m/%d

### capture

The section is used to configure all capturing related settings.

width=1920
height=1080
interval=10
format=jpeg
vertical_flip = true
horizontal_flip = false

### overlay

The section is used to configure all overlay related settings.

enable=true
font_name=/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf
font_size=88
font_color=yellow
text=Nijmegen %Y-%m-%dT%H:%M:%S%z
offset_x=8
offset_y=990
