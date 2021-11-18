#!/bin/bash
#hvar -p /home/nathan/data/2017-Mon-Nov-13/pluto-7/data -v bt x --norm linear --mccomas --streamlines --colormap PRGn --separate-figures --vmin -2 --vmax 2  --units nT --xlim -20 auto --ylim -40 40 --title $'IMF Draping\nIMF:0.3 nT, with IPUIs' --save $1/drape.png --save2 temporary.png --plutostyle
hvar -p /home/nathan/data/2017-Mon-Nov-13/pluto-7/data -v bt x --norm linear --mccomas --streamlines --colormap PRGn --separate-figures --vmin -2 --vmax 2  --units nT --xlim -20 auto --ylim -40 40 --save $1/drape.png --save2 temporary.png --plutostyle --title "IMF:0.3 nT, with IPUIs" --titlesize 12

rm temporary.png
