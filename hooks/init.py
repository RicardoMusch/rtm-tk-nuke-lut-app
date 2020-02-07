"""
Code by Ricardo Musch - February 2020

Get the latest release at:
https://github.com/RicardoMusch/rtm-tk-nuke-lut-app
"""


import nuke
import update_lut

nuke.ViewerProcess.register("SHOW LUT", nuke.createNode, ("SHOW_LUT", ""))
nuke.ViewerProcess.register("SHOT LUT", nuke.createNode, ("SHOT_LUT", ""))

