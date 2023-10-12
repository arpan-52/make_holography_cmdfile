

import numpy as N
import pylab as pl
import ephem, libs
from math import pi

_lat = 19.0906528
_lon = 74.0499722
_ht = 640.0

def _goodtimes(date, time_ut):
  """ Ephem does it correctly when time<0 or time>24 so no problem """

  dd, mm, yy = date
  hr, mn, sec = time_ut

  str1 = str(yy)+'/'+str(mm)+'/'+str(dd)+' '+str(hr)+':'+str(mn)+':'+str(sec)
  d = ephem.Date(str1)

  return d


def _azel2radec(el_d, az_d, date):

  obs = ephem.Observer()
  obs.lon = str(_lon)
  obs.lat = str(_lat)
  obs.elevation = _ht
  obs.date = date

  az = az_d/180.*pi
  el = el_d/180.*pi
  ra, dec = obs.radec_of(az, el)  # is J2000 epoch

  return float(ra), float(dec)

def main(alt_d, az_d, t_hh, t_mm, t_ss, date):
  """ Alt and Az in degrees, times t_hh, t_mm, t_ss is hr, min, sec in UT
      date is tuple of (date, month, year)
      returns ra, dec in deg
  """

  time_ut = (t_hh, t_mm, t_ss)
  dates = _goodtimes(date, time_ut)
  
  dum1, dum2, = _azel2radec(alt_d, az_d, dates) 
  ra, dec = dum1*180./pi, dum2*180/pi # in deg
  
  return ra, dec



