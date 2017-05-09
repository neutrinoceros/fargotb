# lower-case keys correspond to existing .dat files. 
# This dictionnary provides the corresponding rootnames of those files
#
# upper-case keys do not correspond to existing .dat files but rather
# are computed using $RECIPES defined in the following

TAGS = {"d"  : "dens",
        "t"  : "temperature",
        "p"  : "Pressure",
        "vr" : "vrad",
        "vt" : "vtheta",
        "df" : "epsilon",
        "l"  : "label",
        "do" : "dustdens",
        "go" : "gasonlydens",
        #--------------------exp
        "rf" : "radialFlow",
        "PHI": "flow"
       }

Centered  = ["dens", "temperature", "Pressure",
             "espilon", "label", "dustdens", "gasonlydens",
             "vtheta"]

Staggered = ["vrad", "flow"]
