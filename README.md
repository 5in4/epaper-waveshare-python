# README #

Python implementation to make waveshare 4.3inch e-Paper display work on Raspberry Pi

[Waveshare Wiki](http://www.waveshare.com/wiki/4.3inch_e-Paper)

### Functions implemented ###
* clear
* refresh
* text
* set_font_size
* triangle
* circle
* rectangle
* line
* point

### Quickstart ###

```
#!python
from epaper import Epaper
e = Epaper(debug=True)
e.clear()
e.write_text(600, 400, 'test 0001')
e.refresh()
```

#### Connections ####
[raspberry connections]: https://github.com/5in4/epaper-waveshare-python/blob/master/connections.jpg


### Todo ###
* set_colors
* image
* import_image
