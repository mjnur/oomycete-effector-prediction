# Taken from http://web.expasy.org/protscale/pscale/Hphob.Doolittle.html
GRAVY_DIC = {
'A': 1.8, 
'R': -4.5,
'N': -3.5,
'D': -3.5,  
'C':  2.5,  
'Q': -3.5,  
'E': -3.5,  
'G': -0.4,  
'H': -3.2,  
'I':  4.5,  
'L':  3.8,  
'K': -3.9,  
'M':  1.9,  
'F':  2.8,  
'P': -1.6,  
'S': -0.8,  
'T': -0.7,  
'W': -0.9,  
'Y': -1.3,  
'V':  4.2}

## get Hydrophobicity
## https://web.expasy.org/protscale/pscale/Hphob.Fauchere.html
## (Fauchere and Pliska, 1983)

HYDRO_DIC = {
'R': -1.01,
'K': -0.99,  
'D': -0.77,  
'E': -0.64,  
'N': -0.6,
'Q': -0.22,  
'S': -0.04,  
'G': -0.0,  
'H': 0.13,  
'T': 0.26,  
'A': 0.31, 
'P': 0.72,  
'Y': 0.96,  
'V': 1.22,
'C': 1.54,  
'L': 1.7,  
'F': 1.79,  
'I': 1.8,  
'M': 1.23 ,  
'W': 2.25,  
}

# Taken from http://www.cprofiler.org/help.html
# Surface exposure (Janin, 1979), these are free energy values
EXPOSED_DIC = {
'A': 0.3, 
'R': -1.4,
'N': -0.5,
'D': -0.6,  
'C': 0.9,  
'Q': -0.7,  
'E': -0.7,  
'G': 0.3,  
'H': -0.1,  
'I': 0.7,  
'L': 0.5,  
'K': -1.8,  
'M': 0.4,  
'F': 0.5,  
'P': -0.3,  
'S': -0.1,  
'T': -0.2,  
'W': 0.3,  
'Y': -0.4,  
'V': 0.6
}

# Disorder propensity (Dunker et al., 2001)
DISORDER_DIC = {
'A': 1.0,
'R': 1.0,
'S': 1.0,
'Q': 1.0,
'E': 1.0,
'G': 1.0,
'K': 1.0,
'P': 1.0,
'D': 0.0,
'H': 0.0,
'M': 0.0,
'T': 0.0,
'N': -1.0,
'C': -1.0,
'I': -1.0,
'L': -1.0,
'F': -1.0,
'W': -1.0,
'Y': -1.0,
'V': -1.0,
}


# Bulkiness (Zimmerman et al., 1968)
BULKY_DIC = {
'G' : 3.4,
'S' : 9.47,
'A' : 11.5, 
'D' : 11.68,
'N' : 12.82,
'C' : 13.46,
'E' : 13.57,
'H' : 13.69,
'R' : 14.28,
'Q' : 14.45,
'K' : 15.71,
'T' : 15.77,
'M' : 16.25,
'P' : 17.43,
'Y' : 18.03,
'F' : 19.8,
'I' : 21.4,
'L' : 21.4, 
'V' : 21.57,
'W' : 21.67 
}


# Interface propensity (Jones and Thornton, 1997)
INTERFACE_DIC = {
'A': -0.17, 
'R': 0.27,
'N': 0.12,
'D': -0.38,  
'C': 0.43,  
'Q': -0.11,  
'E': -0.13,  
'G': -0.07,  
'H': 0.41,  
'I': 0.44,  
'L': 0.4,  
'K': -0.36,  
'M': 0.66,  
'F': 0.82,  
'P': -0.25,  
'S': -0.33,  
'T': -0.18,  
'W': 0.83,  
'Y': 0.66,  
'V': 0.27}
