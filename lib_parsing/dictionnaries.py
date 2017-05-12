# lower-case keys correspond to existing .dat files. 
# This dictionnary provides the corresponding rootnames of those files
#
# upper-case keys do not correspond to existing .dat files but rather
# are computed using $RECIPES defined in the following

TAGS = {
        # post-processed ----
        "d"  : "dens",
        "t"  : "temperature",
        "p"  : "Pressure",
        "vr" : "vrad",
        "vt" : "vtheta",
        "df" : "epsilon",
        "l"  : "label",
        "do" : "dustdens",
        "go" : "gasonlydens",
        # post-processed ----
        "rf" : "radialFlow",
        "f"  : "FLI",
        # recipes -----------
        "PHI": "flow"#deprecated
       }

Centered  = ["dens", "temperature", "Pressure",
             "espilon", "label", "dustdens", "gasonlydens",
             "vtheta"]

Staggered = ["vrad", "flow", "radialFlow"]

AxLabels = {'d'   : r"$\Sigma$",
            'l'   : r"$\eta$",
            'rf'  : r"$\dot{M}$",
            'f'   : "FLI"}

CMAPS = { 'd' : 'viridis',
          'l' : 'plasma',
          'rf': 'inferno',
          'f' : 'magma'}

SPOTOUTCOLORS = { 'd'  : 'red',
                  'l'  : 'springgreen',
                  'rf' : 'springgreen',
                  'f'  : 'springgreen'}#todo : check if that works
