
import sys
_ = int("%s%s" % (sys.version_info[0], sys.version_info[1]))
        
            
if _ == 27:    
    from .__hybrid__.attributeSpaceSwitcher27 import *
            
if _ == 37:    
    from .__hybrid__.attributeSpaceSwitcher37 import *
