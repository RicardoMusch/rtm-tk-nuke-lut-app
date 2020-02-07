# Installation

## 1) Add to app_locations.yml

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
The folder is automatically created under hooks/tk-nuke/tk-nuke-lut-app.

## - init.py
This should contain code to register your Viewer lut Gizmo's in Nuke. 
Example:

    import nuke
    import update_lut

    nuke.ViewerProcess.register("SHOW LUT", nuke.createNode, ("SHOW_LUT", ""))
    nuke.ViewerProcess.register("SHOT LUT", nuke.createNode, ("SHOT_LUT", ""))