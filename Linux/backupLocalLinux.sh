#!/bin/bash
# -a: archive, this is equivalent to -rlptgoD, where -r is recursive copy
# -u: skips files that are newer on the receiver
# --progress: shows transaction percentage for each copied file. Useful when dealing with big files
# -v: verbose, only tells what file is being copied without showing percentage
# see more option using man rsync in Linux terminal or in https://www.computerhope.com/unix/rsync.htm
rsync -au --progress /home/user/X /destinationFolder