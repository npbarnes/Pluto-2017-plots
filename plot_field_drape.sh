#!/bin/bash
hvar -p /home/nathan/data/2017-Mon-Nov-13/pluto-7/data -v bt x --norm linear --mccomas --streamlines --colormap PRGn --separate-figures --vmin -2 --vmax 2  --units nT --xlim -20 auto --ylim -40 40 --title "IMF Folding" --save $1/drape.png --save2 temporary.png

rm temporary.png
