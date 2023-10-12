
import ephem, time
import numpy as N
from math import pi
import pylab as pl
import time

def parse(hh, mm, ss, dd, ma, sa, epoch):

    rastr = str(hh)+':'+str(mm)+':'+str(ss)
    decstr = str(dd)+':'+str(ma)+':'+str(sa)
    if epoch==None: epoch=2000.0
    epoch = str(epoch)

    return rastr, decstr, epoch


def main(hh, mm, ss, dd, ma, sa, t_hh, t_mm, t_ss, date):
    """
    Usage : 
    ra hours 
    ra min
    ra sec
    dec deg
    deg ma
    deg sa
    UT time hr
    UT time min
    UT time sec
    date is (dd, mm, yyyy), int

    returns alt and az in deg
    """
 
    epoch=2000.0
    rastr, decstr, epoch = parse(hh, mm, ss, dd, ma, sa, epoch)

    gatech = ephem.Observer()
    ncra_lat = 18.+33./60+35.99/3600
    ncra_lon = 73.82
    ncra_ele = 562.0

    gmrt_lat = 19.0906528
    gmrt_lon = 74.0499722
    gmrt_ele = 640.0

    #gatech.lon, gatech.lat, gatech.elev = str(ncra_lon), str(ncra_lat), ncra_ele
    gatech.lon, gatech.lat, gatech.elev = str(gmrt_lon), str(gmrt_lat), gmrt_ele
  
    alts = []; azs = []
    yh = ephem.readdb("SRC,f,"+rastr+','+decstr+',0,'+epoch)
    
    hour = str(t_hh)
    minute = str(t_mm)
    second = str(t_ss)

    date = [date[2], date[1], date[0]]
    dates = str(date[0])+'/'+str(date[1])+'/'+str(date[2])+' '+hour+':'+minute+':'+second

    gatech.date = dates
    yh.compute(gatech)
  
    alt, az = yh.alt*180.0/pi, yh.az*180.0/pi

    return alt, az


          
      
  
