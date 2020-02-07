import nuke
import update_lut

nuke.ViewerProcess.register("SHOW LUT", nuke.createNode, ("SHOW_LUT", ""))
nuke.ViewerProcess.register("SHOT LUT", nuke.createNode, ("SHOT_LUT", ""))

