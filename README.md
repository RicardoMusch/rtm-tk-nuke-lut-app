# rtm-tk-nuke-lut-app
 

## Installation

# 1) Add to app_locations.yml

    apps.rtm-tk-nuke-lut-app.location:
      type: git
      version: v0.1
      path: https://github.com/RicardoMusch/rtm-tk-nuke-lut-app.git

# 2) Add to tk-nuke.yml settings

    settings.tk-nuke.shot_step:
      apps:
        rtm-tk-nuke-lut-app:
          location: "@apps.rtm-tk-nuke-lut-app.location"

# 3) Cache app
Run the following tank command:

    tank cache_apps


