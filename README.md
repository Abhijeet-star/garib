# GARIB - Galactic Avoidance for RadIo antenna Beams

This package is useful for radio astronomy experiments where you need to select/avoid particular regions of the sky. 

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