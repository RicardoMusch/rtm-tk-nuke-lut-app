# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.


from sgtk.platform import Application

import os
import shutil
import nuke

import sgtk



class StgkStarterApp(Application):
    """
    The app entry point. This class is responsible for initializing and tearing down
    the application, handle menu registration etc.
    """
    
    def init_app(self):
        """
        Called as the application is being initialized
        """
        
        # first, we use the special import_module command to access the app module
        # that resides inside the python folder in the app. This is where the actual UI
        # and business logic of the app is kept. By using the import_module command,
        # toolkit's code reload mechanism will work properly.
        #app_payload = self.import_module("app")

        # now register a *command*, which is normally a menu entry of some kind on a Shotgun
        # menu (but it depends on the engine). The engine will manage this command and 
        # whenever the user requests the command, it will call out to the callback.

        # Get Current Shotgun Toolkit path
        #tk = sgtk.sgtk_from_entity(context.project["type"], context.project["id"])
        #sgtk_path = str(tk).split(" ")[-1]
        sgtk_python_path = sgtk.get_sgtk_module_path()
        sgtk_config_path = os.path.join(sgtk_python_path.split("install")[0], "config")
        
        # Check if hook folder exists, this app will not work without making a bespoke lut gizmo and script.
        app_hook_path = os.path.join(sgtk_config_path, "hooks", "tk-nuke", "tk-nuke-lut-app")
        if not os.path.exists(app_hook_path):
            os.makedirs(app_hook_path)
            self.logger.info("Created Hooks folder: tk-nuke/tk-nuke-lut-app")

        # Copy over the update_lut.py
        callback_script = "update_lut.py"
        src = os.path.join(os.path.dirname(__file__), "resources", callback_script)
        dst = os.path.join(app_hook_path, callback_script)
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
            self.logger.info("Copied "+callback_script+" script to hooks folder because it did not exist yet.")

        # Copy over the example init.py
        resource = "init.py"
        src = os.path.join(os.path.dirname(__file__), "resources", resource)
        dst = os.path.join(app_hook_path, resource)
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
            self.logger.info("Copied "+resource+" script to hooks folder because it did not exist yet.")


        # Adding hook folder to Nuke Path so the custom gizmo and script can be picked up
        nuke.pluginAddPath(app_hook_path)
        self.logger.error("Adding "+app_hook_path+" to nuke plugin path")

        # first, set up our callback, calling out to a method inside the app module contained
        # in the python folder of the app
        menu_callback = lambda : loadLut()

        # now register the command with the engine
        self.engine.register_command("Load LUT...", menu_callback)

        # Callbacks
        nuke.addOnScriptSave(loadLut())
        nuke.addOnScriptLoad(loadLut())


def loadLut():
    """
    Callback which runs evere script load and save and calls the update_lut.update() function
    """

    try:
        import update_lut
        update_lut.update()

    except Exception as e:
        print "\n\n"
        print "ERROR IN LOADLUT!"
        print e
        print "\n\n"
        pass
    

