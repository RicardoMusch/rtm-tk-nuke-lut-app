import nuke
import os
import sgtk

# List of Luts to Update. Last one will be the default.
luts = ["SHOW LUT", "SHOT LUT"]

def update():
    # # get the engine we are currently running in
    # try:
    #     current_engine = sgtk.platform.current_engine()
    # except:
    #     current_engine = self.engine

    # # get hold of the shotgun api instance used by the engine, (or we could have created a new one)
    # sg = current_engine.shotgun

    # # Get current Context
    # context = current_engine.context

    for lut in luts:
            
        # Get the Just Created Viewer Process
        lut_name = lut
        lut = nuke.ViewerProcess.node(lut_name)

        for viewer in nuke.allNodes("Viewer"):
            viewer["viewerProcess"].setValue(lut["name"].getValue())

        # Run LUT Button
        #self.logger.error("Running LUT Update Button...")
        lut["update"].execute()
        print "Running 'update' knob on the '"+lut_name+"' node"


def loadLut():
    logBig("Loading: "+os.path.basename(__file__))

    try:
        # Get a Shotgun Connection
        sg = _getShotgunConnection()

        # Get a Shotgun Context
        context = _getShotgunEntityContext(sg)

        # Get the Just Created Viewer Process
        lut = nuke.thisNode()

        ############# ADD SHOW FUNCTION CODE HERE ########################
        """
        Use the 'lut' var to acces the created gizmo and its knobs.
        """

        # Get Shot Data
        filters = [ ["id", "is",  context["id"]] ]
        fields = ["sg_cdl_asc_sat", "sg_cdl_asc_sop", "sg_lut"]
        sg_shot = sg.find_one("Shot", filters, fields)
        log(sg_shot)

        dataField = "sg_cdl_asc_sop"
        if sg_shot[dataField] != None:
            lut["slope"].setValue(_filterSatSop("slope", sg_shot[dataField]))
            lut["offset"].setValue(_filterSatSop("offset", sg_shot[dataField]))
            lut["power"].setValue(_filterSatSop("power", sg_shot[dataField]))
        lut["working_space"].setValue("AlexaV3LogC")
        
        dataField = "sg_cdl_asc_sat"
        if sg_shot[dataField] != None:
            lut["saturation"].setValue(_filterSatSop("saturation", sg_shot[dataField]))

        
        # Disable CDl if Show LUT
        if lut.Class() == "SHOW_LUT":
            lut["disable_OCIOCDLTransform"].setValue(True)
        else:
            lut["disable_OCIOCDLTransform"].setValue(False)



        ############# END SHOW FUNCTION CODE ##############################

        # Set Current and more Viewers to LUT we Created
        #node = nuke.activeViewer().node()['viewerProcess'].setValue(lut_name)
        log("Setting all Viewers to use the Lut")
        for node in nuke.allNodes("Viewer"):
            node["viewerProcess"].setValue(lut_name)

    except Exception as e:
        print "\n\n"
        print "ERROR loading Shot Lut!"
        print e
        print "\n\n"

    
def _filterSatSop(datatype, data):
    data = data.replace("(", "")

    if datatype == "slope":
        data = data.split(")")[0]
        data = data.split(" ")
        vals = [float(data[0]), float(data[1]), float(data[2])]
        msg = datatype, vals
        log(msg)
        return data

    if datatype == "offset":
        data = data.split(")")[1]
        data = data.split(" ")
        vals = [float(data[0]), float(data[1]), float(data[2])]
        msg = datatype, vals
        log(msg)
        return data

    if datatype == "power":
        data = data.split(")")[2]
        data = data.split(" ")
        vals = [float(data[0]), float(data[1]), float(data[2])]
        msg = datatype, vals
        log(msg)
        return data
    
    if datatype == "saturation":
        data = data.replace("(", "")
        data = data.replace(")", "")
        msg = datatype, data
        log(msg)
        return float(data)


def _findTopNode():
    """
    Returns the Top Node connection, usually a Read node.
    """
    node = nuke.thisNode()

    parent_node = node
    while parent_node != None:
        last_node = parent_node
        parent_node = parent_node.input(0)
    return last_node


def _extractVersionName(path):
    path = os.path.basename(path)
    path = path.lower()
    
    parts = path.split(".")

    version_name = None

    for part in parts:
        if not "#" in part:
            if not "%" in part:
                if version_name == None:
                    version_name = part
                else:
                    version_name += "."+part  

    return version_name


def _getShotgunConnection():
    try:
        #### Get Shotgun Connection and Context when in SGTK session

        # get the engine we are currently running in
        current_engine = sgtk.platform.current_engine()

        # get hold of the shotgun api instance used by the engine, (or we could have created a new one)
        sg = current_engine.shotgun
        return sg

    except:
        #### Get Shotgun Connection and Context when not in SGTK session (example: farm)
        
        #####################################################
        logBig("Importing Shotgun API3")
        #####################################################
        shotgun_api3_location = os.environ["SHOTGUN_API3"]
        sys.path.append(shotgun_api3_location)
        import shotgun_api3
        log("Imported the Shotgun Standalone API3")


        #####################################################
        logBig("Connecting to Shotgun API")
        #####################################################
        sg = shotgun_api3.Shotgun(os.environ["SHOTGUN_API_SERVER_PATH"], os.environ["SHOTGUN_API_SCRIPT_NAME"], os.environ["SHOTGUN_API_SCRIPT_KEY"])
        log("Connected to Shotgun!")
        return sg



def _getShotgunEntityContext(sg):
    
    try:
        #### SGTK SESSION
        # get the engine we are currently running in
        current_engine = sgtk.platform.current_engine()

        # Get current Context
        context = current_engine.context
        return context.entity
    
    except:
        #### STANDALONE SESSION (example: farm)

        # Find Top node to get a path from
        topNode = _findTopNode()

        try:
            filepath = topNode["file"].getValue().replace("\\", "/")
            
            # Find Version that links to Entity
            filters = [ ["sg_path_to_frames", "is", filepath] ]
            version_fields = ["entity"]
            sg_version = sg.find_one("Version", filters, version_fields)
            
            if sg_version == None:
                # Find Version that links to Entity - Reverse path separators
                filters = [ ["sg_path_to_frames", "is", filepath.replace("/", "\\")] ]
                sg_version = sg.find_one("Version", filters, version_fields)

            if sg_version == None:
                # Find Version that links to Entity - Version code Match (least precise)
                filters = [ ["sg_path_to_frames", "is", _extractVersionName(filepath) ] ]
                sg_version = sg.find_one("Version", filters, version_fields)

            return sg_version["entity"]
        
        except Exception as e:
            log("Error Finding Entity Context")
            log(e)


def log(msg):
    print "    "+str(msg)


def logBig(msg):
    print "\n\n"
    print "############################################################"
    print msg
    print "############################################################"
    

# Run Main Function
loadLut()
log(" ")