import nuke
import os

def loadShotLut():
    logBig("Loading: "+os.path.basename(__file__))

    try:
        import sgtk

        # get the engine we are currently running in
        current_engine = sgtk.platform.current_engine()

        # get hold of the shotgun api instance used by the engine, (or we could have created a new one)
        sg = current_engine.shotgun

        # Get current Context
        context = current_engine.context

        # Get the Just Created Viewer Process
        lut = nuke.thisNode()

        ############# ADD SHOW FUNCTION CODE HERE ########################
        """
        Use the 'lut' var to acces the created gizmo and its knobs.
        """

        # Get Shot Data
        filters = [ ["id", "is", context.entity["id"]] ]
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
        msg = datatype, vals
        log(msg)
        return float(data)

def log(msg):
    print "    "+str(msg)

def logBig(msg):
    print "\n\n"
    print "############################################################"
    print msg
    print "############################################################"
    

# Run Main Function
loadShotLut()
log(" ")