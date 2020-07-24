from Katana import NodegraphAPI

def getMergeGrp(gnode):
    for i in gnode.getChildren():
        if '_MERGE_SETUP_' in i.getName():
            MergeGrp = i

            return MergeGrp


