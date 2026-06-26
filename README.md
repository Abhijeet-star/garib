# GARIB - Galactic Avoidance for RadIo antenna Beams

This package is useful for radio astronomy experiments where you need to select/avoid particular regions of the sky. 

## Motivation

Any radio antenna has a beam pattern which is the response of the antenna as a function of theta and phi. For simplicity, we consider an azimuthally symmetric beam pattern which follows sine-squared function. When this beam pattern is projected onto the sky, we have a circular projection. Now the measurement is the summation of this disc with sky intensity which is predominately diffuse galactic emission caused by synchrotron radiation. The emissions from the galactic plane are difficult to model as there are various physical processes happening along with synchrotron process. 

So it is always better to avoid these regions. This is the motivation for this package. 

## How it works

We chose a circle with radius corresponding to the Full Width at Half Maxima (FWHM) of the beam. A rectangular Galactic region is chosen for now which extends 45 degrees in latitude and 10 degrees in longitude. At a particular time, if the circle touches/crosses the rectangle, the time of observation is noted. In the end, we get a "badtimes.txt" file which has all the times for which the beam intersects the galacic region.

## Installation

```
pip install garib
```

## Example file

```
import numpy as np
from astropy.time import Time, TimeDelta
from GARIB.garib import GalaxyElimination
```

```
## SPECIFY PATH TO THE FILE
file = "./SINESQ_500times_EARTH_jun26.h5"

## SPECIFY LOCATION ON EARTH
SITE_LATITUDE       = 32.81444444
SITE_LONGITUDE      = 78.85555556
ELEVATION           = 4500

## Number of observations and start of observing time
dt = TimeDelta(np.linspace(0.,24.*3600, 500), format='sec')
obstimes = Time('2019-4-12 23:00:00')  + dt

## FREQUENCY OF THE BEAM
chosen_frequency = 65

## RESOLUTION OF THE SKY MAP
nside = 16

## EXTENT OF THE GALATIC REGION
lmax  = 45
bmax  = 10
```

```
param_obs = {'file': file,\
            'chosen_frequency': chosen_frequency,\
            'site_latitude': SITE_LATITUDE,\
            'site_longitude': SITE_LONGITUDE,\
            'elevation': ELEVATION,\
            'nside': nside,\
            'l':lmax,\
            'b':bmax}
```

```
# Galaxy Avoidance for RadIo antenna Beams: GARIB

GE = GalaxyElimination(**param_obs)
GE.time_elimination()
```