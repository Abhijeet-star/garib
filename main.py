import numpy as np
import astropy.units as u
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
import healpy as hp



class GalaxyElimination(object):
    def __init__(self, time, site_latitude, site_longitude, elevation, nside, l, b, radius):
        self.time = time
        self.site_latitude = site_latitude
        self.site_longitude = site_longitude
        self.elevation = elevation
        self.nside = nside
        self.l = l
        self.b = b
        self.radius = radius
        
        self.coordinate_generation()
        self.set_location()
        self.find_nearest()

    def coordinate_generation(self): 
        npix = hp.nside2npix(self.nside)
        pixels = np.arange(npix)
        theta, phi = hp.pix2ang(self.nside, pixels, nest=True)

        ll_coordinate = phi
        bb_coordinate = np.pi/2. - theta

        self.ll_coordinate = ll_coordinate
        self.bb_coordinate = bb_coordinate


    def set_location(self):
        location = EarthLocation(lat=self.site_latitude*u.deg, lon=self.site_longitude*u.deg, height=self.elevation*u.m)
        gc       = SkyCoord(l=self.ll_coordinate*u.radian, b=self.bb_coordinate*u.radian,\
                    frame='galactic')
        self.gc  = gc
        self.location = location


    def find_nearest(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]



    def inside_rectangle_np(points, rect_bottom_left, rect_top_right, include_boundary=True):
        x1, y1 = rect_bottom_left
        x2, y2 = rect_top_right
        xmin, xmax = min(x1, x2), max(x1, x2)
        ymin, ymax = min(y1, y2), max(y1, y2)

        px, py = points[:, 0], points[:, 1]
        if include_boundary:
            mask = (xmin <= px) & (px <= xmax) & (ymin <= py) & (py <= ymax)
        else:
            mask = (xmin < px) & (px < xmax) & (ymin < py) & (py < ymax)
        return mask
    

    # l = 45
    # b = 10

    # rbl = (-l,-b)
    # rtr = (+l,+b)

    # lb = np.stack((lon,lat), axis=1)

    def fixed_radius(self, tt):
        # mn = lss.LunarTopo(obstime=obstimes[tt], location=location)
        # trans_local = gc.transform_to(mn)
        trans_local             = self.gc.transform_to(AltAz(obstime=tt, location=self.location))
        az, alt                     = trans_local.az.degree, trans_local.alt.degree
        az, alt     = trans_local.az.degree, trans_local.alt.degree
        beam_gen = np.zeros_like(tsky)

        rogue_phi  = []

        for iangle, (alt_value, az_value) in enumerate(zip(alt,az)):
            if az_value > phi_array.max():
                rogue_phi.append(az_value)
                az_value = 360 - az_value
            beam_gen[iangle,0] = beam_val([alt_value, az_value])

        hf_bm = find_nearest(beam_gen[:,0], 0.5)
        idx_hf = np.where(beam_gen[:,0] == hf_bm)

        idx = np.where(beam_gen[:,0] == max(beam_gen[:,0]))
        theta_c, phi_c = hp.pix2ang(16, idx[0][0], nest=True)

        theta_hf, phi_hf = hp.pix2ang(16, idx_hf[0][0], nest=True)

        vec_c  = hp.ang2vec(theta_c, phi_c)
        vec_hf = hp.ang2vec(theta_hf, phi_hf)
        radius = np.arccos(np.clip(np.dot(vec_c, vec_hf), -1.0, 1.0))
        return radius
