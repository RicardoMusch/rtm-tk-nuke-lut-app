# Installation

## 1) Add to app_locations.yml  
Make sure to check for the latest git release and change the version tag accordingly!

    apps.rtm-tk-nuke-lut-app.location:
      type: git
      version: v0.1
      path: https://github.com/RicardoMusch/rtm-tk-nuke-lut-app.git

## 2) Add to tk-nuke.yml settings

    settings.tk-nuke.shot_step:
      apps:
        rtm-tk-nuke-lut-app:
          location: "@apps.rtm-tk-nuke-lut-app.location"

## 3) Cache app
Run the following tank command:

    tank cache_apps



# Hooks
For this app to work, you will need to creathe the following files in it's hook folder.
You can take the files from the app's hooks folder and edit as your see fit.
The folder is automatically created under hooks/tk-nuke/tk-nuke-lut-app.

## - init.py
This should contain code to register your Viewer lut Gizmo's in Nuke. 
Example:

    import nuke
    import update_lut

    nuke.ViewerProcess.register("SHOW LUT", nuke.createNode, ("SHOW_LUT", ""))
    nuke.ViewerProcess.register("SHOT LUT", nuke.createNode, ("SHOT_LUT", ""))

## - update_lut.py
This script contains several functions, most important is the "update()" function which triggers on nuke script load and save.
In this example the update() function finds the registered viewer LUTs and runs the "update" python button on these.

    import nuke
    import os
    import sgtk

    # List of Luts to Update. Last one will be the default.
    luts = ["SHOW LUT", "SHOT LUT"]

    def update():

        for lut in luts:
                
            # Get the Just Created Viewer Process
            lut_name = lut
            lut = nuke.ViewerProcess.node(lut_name)

            for viewer in nuke.allNodes("Viewer"):
                viewer["viewerProcess"].setValue(lut["name"].getValue())

            # Run LUT Button
            lut["update"].execute()
            print "Running 'update' knob on the '"+lut_name+"' node"


## - LUT Gizmo's
You can create your own gizmo's and place them in the hooks folder (or anywhere in NUKE_PATH).
The Gizmo must have a "update" python button to be able to be executed and change context.
If it doesn't have this the gizmo will be assumed to be a static gizmo in cases there is just one LUT.
The example from the app's hooks folder is a more complicated gizmo that accounts for CDL values per shot, a show lut and a sRGB transform.
