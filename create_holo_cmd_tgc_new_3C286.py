#New TGC
"""
Uniform grid in alt-az in antenna frame
"""

import numpy as N
import matplotlib
#matplotlib.use("Agg")
import pylab as pl
import a2r, r2a, libs, math, ephem, pickle, time
from libs import rotation
import para

pl.ion()

def antennaframe(freq=330.e6):
  """ 
  Usage : main((dd, mm, yyyy), hh.hh, hh.hh, n)
          Date is dd, mm, yyyy
          Start and end times are hh.hh in IST
    	  Number of grid points in 1d is n
          freq in Hz
          limit = 4.0 # times hwhm, on one side

          main((18,1,2016), 11.3, 21.6, 15)
  """

  radecs= {}
  radecs['3C48'] = ((1, 37, 41.1), (+33, 9, 32.0))
  radecs['3C147'] = ((5, 42, 36.1), (+49, 51, 7.0))
  radecs['3C147A'] = ((5, 41,  7.5), (+49, 40, 2.8))
  radecs['3C286'] = ((13, 31, 8.3), (+30, 30, 33))

  dia = 45.	# m
  c=2.99792458e8	# m s^-1

  gmrt_lat = 19.0905	# deg
  gmrt_lon = 74.0506	# deg
  gmrt_ele = 640.0	# m

  # read para
  source = para.source
  date = para.date
  time0 = para.time0
  grid1d = para.grid1d 
  total_dist = para.total_dist
  tot_time_per = para.tot_time_per
  ncal = para.ncal
  cmdfile = para.cmdfile

  # convert stuff
  time0 = time0 - 5.5	# IST to UT conversion
  t0 = libs.convert_time(time0)
  ra_s, dec_s = radecs[source]
  ra_3C286, dec_3C286 = radecs['3C286']

  # get obs times
  # grid1d pts in 1d, times has all the times at each grid location
  npoints = 211
  total_time_hr = npoints*tot_time_per/3600.0
  print('Start time = ', libs.convert_time(time0+5.5))	# In IST
  print('End time = ', libs.convert_time(time0+5.5+total_time_hr + (grid1d+1)*tot_time_per*ncal/3600.0))  # last for calib (in IST)
  t_step = tot_time_per/3600.0	# In hours
  print("Interval between each pointing is %.1f s" %(t_step*3600.))

  time1 = time0+total_time_hr #+ tot_time_per*ncal/3600.0 #+ (grid1d+1)*tot_time_per*ncal/3600.0   # +1 because of initial cal scan
  times_all = N.arange(time0, time1, t_step)   # in UT; array of all the start times of new scans
  #times_all = times_all[:-1] # NIRUJ HACK
  timeflag = N.ones(len(times_all))   # 1 if calc az el and 0 if not (cal scan) - per minute
  timeflag[:ncal] = 0
  print(timeflag)
  print(len(timeflag))
  # for i in range(1,grid1d+1):
  #   timeflag[(grid1d+ncal)*i:(grid1d+ncal)*i+ncal] = 0
  
#   print(timeflag)
  scannames = []
  scannames.append(source)
  times = []
  ctr=0

  cons = 1
  t = N.linspace(0,72*N.pi,900)
  x = cons*N.radians(t)*N.cos(N.radians(t))
  y = cons*N.radians(t)*N.sin(N.radians(t))
  altaz_grids= []
  altaz_grids.append([0., 0.])
  for j in range(0,360,30):
      print(j)
      x_rot, y_rot = rotation(x,y,j)
      pl.plot(x_rot,y_rot)
      temp_list = []
      for i in range(0,len(x_rot),50):
          pl.scatter(x_rot[i],y_rot[i],alpha=1)
          if (j/30)%2 == 0:
              altaz_grids.append([x_rot[i], y_rot[i]])
          else:
              temp_list.append([x_rot[i],y_rot[i]])
      if (j/30)%2 != 0:
          temp_list.pop(0)
          altaz_grids.extend(temp_list[::-1]) 
  
  print(len(altaz_grids))
  print(len(times_all))
   
  for i in range(1,len(times_all)):
        print(i)
        if (altaz_grids[i] == [0.0,0.0]):
            scannames.append('3C286')
            ctr +=1
        else:
            scannames.append('PN0'+'0'*(3-len(str(ctr)))+str(ctr))
            ctr+=1  
  times = N.asarray(times_all)
  print(len(times))
  print(times)
  print("Number of scan names = ",len(scannames))
  print(scannames)

  pl.figure()
  pl.plot(times,'*')

  print("Number of grid pointings = ", npoints)
  print("Number of scans = ", npoints + grid1d + 1)
  print("Total time taken ", time1-time0, (npoints+(grid1d+1)*ncal)*tot_time_per/3600.0)
  print("Step size is ", total_dist/(grid1d-1), " amin")
  stepsize = total_dist/(grid1d-1)  # amin

  # format
  dec0 = N.sum(N.asarray(radecs[source][1])*N.asarray([1., 1./60, 1./3600]))  # dec in deg
  ra0 = 15.0*N.sum(N.asarray(radecs[source][0])*N.asarray([1., 1./60, 1./3600]))  # ra in deg

  ## angular extent of gridding
  #limit_deg = c/freq/dia*180./math.pi/2.0*limit # is distance bet centre and edge of grid in deg
  #limit_deg1 = limit_deg/math.cos(dec0/180.*math.pi)  # in RA direction


  # # calc uniform antenna frame alt az grid
  # altaz_grids = []
  # altaz_grids.append([0., 0.])
  # for ialt in range(grid1d):
  #   alt = total_dist/(grid1d-1)*(ialt-(grid1d-1)/2)/60.0  # deg   # changed sign inside because just after transit, offset was across meridian
  #   for iaz in range(grid1d):   # this is pure angle, no need for cos
  #     az = total_dist/(grid1d-1)*(iaz-(grid1d-1)/2)/60.0  # NIRUJ SHI
  #     altaz_grids.append([alt, az])
  #   altaz_grids.append([0, 0])



  pl.figure(figsize=(16,14))
  altaz_grids = N.transpose(N.asarray(altaz_grids))
  ntimes = len(altaz_grids[0])
  print(len(times), ntimes, ' do they match')

  pl.subplot(331)
  pl.plot(altaz_grids[0], altaz_grids[1], '.', ms=3.0)
  pl.plot([0], [0], '*g', ms=15)
  pl.xlabel('Alt (deg)'); pl.ylabel('Az (deg)')

  # now de-rotate for PA but since you need to know the HA first which needs the actual coords of each pointing, 
  # do it over n iterations
  # can always check if this works by doing the inverse of the final ra-dec positions
  # first calculate alt az for centre for times
  altaz0_grid = [] # this is alt az for 3c 48 for obs times
  for i in range(len(times)):
    hh, mm, ss = ra_s
    dd, ma, sa = dec_s
    if times[i]<0:
      date1 = (date[0]-1, date[1], date[2])
      t_hh, t_mm, t_ss = libs.convert_time(24.0+times[i])
    else:
      date1 = date
      t_hh, t_mm, t_ss = libs.convert_time(times[i])
    altaz0_grid.append(r2a.main(hh, mm, ss, dd, ma, sa, t_hh, t_mm, t_ss, date1))
    print((hh,mm,ss,dd,ma,sa), r2a.main(hh, mm, ss, dd, ma, sa, t_hh, t_mm, t_ss, date1), times[i], date1)
  altaz0_grid = N.transpose(N.asarray(altaz0_grid))
  
  # then calculate LST
  sidtimes = N.zeros(len(times))
  for i in range(len(times)):
    if times[i]<0:
      t_hh, t_mm, t_ss = libs.convert_time(times[i]+24.0+40./3600)   # 40 secs after beginning of slew. 20 sec for slew and midpoint of next 40 sec NIRUJ assume 1 min
      hour, minute, second = str(t_hh), str(t_mm), str(t_ss)
      dates = str(date[2])+'/'+str(date[1])+'/'+str(date[0]-1)+' '+hour+':'+minute+':'+second
    else:
      t_hh, t_mm, t_ss = libs.convert_time(times[i]+40./3600)   # 40 secs after beginning of slew. 20 sec for slew and midpoint of next 40 sec NIRUJ assume 1 min
      hour, minute, second = str(t_hh), str(t_mm), str(t_ss)
      dates = str(date[2])+'/'+str(date[1])+'/'+str(date[0])+' '+hour+':'+minute+':'+second
    gatech = ephem.Observer()
    gatech.lon, gatech.lat, gatech.elev = str(gmrt_lon), str(gmrt_lat), gmrt_ele
    gatech.date = dates
    sidtim = (gatech.sidereal_time())
    sidtimes[i] = N.sum(N.asarray(str(sidtim).split(':'), float)*N.asarray([1, 1./60, 1./3600]))

  # now calc HA for centre, use that to derotate pointing
  # iterate
  cols = ['b', 'c', 'k', 'r', 'm']
  radec_ini = N.asarray([N.ones(len(times))*ra0, N.ones(len(times))*dec0])
  niter = 1#4
  for ictr in range(niter):
    if ictr == 0:
      ra_use, dec_use = radec_ini
    else:
      ra_use, dec_use = radec_grids

    HAs, pas = N.zeros(len(times)), N.zeros(len(times))
    radec_grids = N.zeros(altaz_grids.shape)
    dum = N.zeros(altaz_grids.shape)

    HAs = (sidtimes - ra_use/15.)
    cosd = N.cos(dec_use/180.*math.pi)
    sind = N.sin(dec_use/180.*math.pi)
    tanp = N.tan(gmrt_lat/180.*math.pi)
    cosH = N.cos(HAs*15/180.*math.pi)
    sinH = N.sin(HAs*15/180.*math.pi)
    for i in range(len(times)):
      pas[i] = math.atan2(sinH[i], cosd[i]*tanp - sind[i]*cosH[i])*180./math.pi
    pas = -pas  # derotate

    # derotate alt and az differences wrt centre
    x = N.asarray(altaz_grids[1]); y = N.asarray(altaz_grids[0])   # 0,1 = alt, az
    # *** Div 26Apr2019 ***
    # IF THE OFFSETS ARE BEING PROVIDED IN az,alt, THEY ARE ALREADY IN THE ANTENNA FRAME AND SHOULD NOT BE DE-ROTATED BY THE PARALLACTIC ANGLE.
    # The simplest way to do this in the script is by simply setting the angle of rotation to 0 for all x and y.
    drot_az = x
    drot_alt = y
    #drot_az = N.cos(pas*math.pi/180)*x - N.sin(pas*math.pi/180)*y
    #drot_alt = N.sin(pas*math.pi/180)*x + N.cos(pas*math.pi/180)*y
    # *** Div 26Apr2019 ***

    pl.subplot(334)
    pl.plot(times, HAs, '.', ms=3.0, color=cols[ictr])
    pl.xlabel('Time'); pl.ylabel('HA (hrs)')
    pl.subplot(335)
    pl.plot(times, pas, '.', ms=3.0, color=cols[ictr])
    pl.xlabel('Time'); pl.ylabel('PA (deg)')

    pl.subplot(337)
    pl.plot(drot_alt, drot_az, '.', ms=3.0, color=cols[ictr])
    pl.axis([-5,4,-5,4])
    pl.xlabel('PA derot alt diff (deg)'); pl.ylabel('PA derot az diff (deg)') 

    # now get actual alt-az values (uncorrect for cos factor)
    rot_alt = drot_alt + altaz0_grid[0]
    rot_az = drot_az/N.cos((rot_alt)/180.*math.pi) + altaz0_grid[1]   # NIRUJ COS OF ALT0 OR THIS ????  # PUT PROPER SPHERICAL DIST HERE   FOR NOW DIVIDE AND NOT MULTIPLY

#cos (rot_alt_ has some diff with sim but of altaz_grid doesnt - why is that 
#k both are wrong u need sph geom dist  do that and u will be fine

    pl.subplot(338)
    pl.plot(rot_alt, rot_az, '.', ms=3.0, color=cols[ictr])
    pl.xlabel('Sky alt (deg)'); pl.ylabel('Sky az (deg)')

    # calculate ra-dec
    for i in range(len(times)):
      if times[i] >0:
        t_hh, t_mm, t_ss = libs.convert_time(times[i])
        radec_grids[0][i], radec_grids[1][i] = a2r.main(rot_alt[i], rot_az[i], t_hh, t_mm, t_ss, date)  
        dum[0][i], dum[1][i] = a2r.main(altaz0_grid[0][i], altaz0_grid[1][i], t_hh, t_mm, t_ss, date)  
      else:
        t_hh, t_mm, t_ss = libs.convert_time(times[i]+24.0)
        date1 = (date[0]-1, date[1], date[2])
        radec_grids[0][i], radec_grids[1][i] = a2r.main(rot_alt[i], rot_az[i], t_hh, t_mm, t_ss, date1)  
        dum[0][i], dum[1][i] = a2r.main(altaz0_grid[0][i], altaz0_grid[1][i], t_hh, t_mm, t_ss, date1)  
    
    # plot actual ra and dec grid 
    pl.subplot(332)
    #if ictr in [0, niter-1]:
    if 1:
      pl.plot(radec_grids[0], radec_grids[1], '.', ms=4.0, color=cols[ictr])
    pl.plot(dum[0], dum[1], '*g', ms=8.0)
    pl.xlabel('RA (deg)'); pl.ylabel('Dec (deg)')

    # plot ra and dec vs time
    pl.subplot(333)
    pl.plot(times, radec_grids[0], '.', ms=3.0, color=cols[ictr])
    pl.xlabel('Time UT (hrs)'); pl.ylabel('RA (deg)')
    pl.subplot(336)
    pl.plot(times, radec_grids[1], '.', ms=3.0, color=cols[ictr])
    pl.xlabel('Time UT (hrs)'); pl.ylabel('Dec (deg)')

    pl.subplot(339)
    pl.plot(times, rot_alt, '.', ms=3.0, color=cols[ictr])
    pl.xlabel('Time UT (hrs)'); pl.ylabel('Sky alt (deg)')

  pl.suptitle('Grid positions for IST='+str(time0+5.5)+'-'+str(time1+5.5)+' on '+str(date)+', for '+str(grid1d)+' points per line')
  pl.savefig('grid_positions_IST'+str(time0+5.5)+'-'+str(time1+5.5)+'_'+str(date)+'_'+str(grid1d)+'pts.png')
 
  pickle.dump([radec_grids[0], radec_grids[1], times/24., rot_alt, rot_az, drot_alt, drot_az, altaz_grids, pas], open('testdata_aa2rd', 'wb'))
  # list of ra, list of dec, time in UT, etc
  # rot_alt and rot_az are actual alt az positions of grid
  # altaz0_grid is 2X1 (alt, az) array of 3C 48's alt and az at the observed times. Subtract for rot_alt and rot_az with cos factor
  # correctly figured out for offset
 

  #for i in range(len(times)):
  #  tt = libs.convert_time(times[i])
  #  print "%i %i %i %i %.2f %.2f" %(i, tt[0], tt[1], int(round(tt[2])), drot_alt[i], drot_az[i]/N.cos((rot_alt[i])/180.*math.pi)) 

  fn = open(cmdfile, "w")
  fn.write("#!/usr/bin/python\n")
  fn.write("# holography command file\n\n")

  fn.write("# import required libraries for TGC\n")
  fn.write("from tgcall import *\n")
  fn.write("import time\n")
  fn.write("import userproc\n")
  fn.write("from userproc import rfi_fil_sleep\n")
  fn.write("import corrapi_fstrt\n")
  fn.write("from gwbproc import *\n\n")

  fn.write("# setup\n")
  fn.write("CORR='GWB'\n")
  fn.write("trk_sub=1\n")
  fn.write("cor_sub=0\n")
  fn.write("src='"+source+"'\n")
  fn.write("trk=1 # 1-out, 0-in\n\n")

  fn.write("# add source catalog/list\n")
  fn.write("add_user_catalog('/data1/gtac/cmd/holo/src_3c286.csv','type1')\n")
  fn.write("use_catalog('src_3c286','type1')\n\n")

  fn.write("# track source/cal\n")

  fn.write("load_source(src)\n")
  fn.write("track_array(trk_sub,timeout=10)\n")
  fn.write("set_srv_time(trk_sub)\n")
  fn.write("mon_script()\n\n")


  for i in range(len(times)):
    tt = times[i]+5.5
    tt = libs.convert_time(tt)
    if any(N.array(tt) < 0) : raise RuntimeError("Please fix")
    newtime = int(time.mktime((date[2], date[1], date[0], tt[0], tt[1], int(tt[2]), 0, 0, 0)))  # Since "epoch"  

    fn.write('# '+str(i)+' '+scannames[i]+'\n')
    dum = N.asarray(tt, int)
    #fn.write("/nextposn "+str(newtime)+" * "+str(date[0])+" "+str(date[1])+" "+str(date[2])+" * " + str(dum[0])+" "+str(dum[1])+" "+str(dum[2])+"\n")
    fn.write("wait('"+str(dum[0])+":"+str(dum[1])+":"+str(dum[2])+"','"+str(date[0])+"/"+str(date[1])+"/"+str(date[2])+"')\n")
    if i>0:fn.write("stpndas(CORR,cor_sub,timeout=0)\n")
    name = scannames[i]
    fn.write("load_source('"+name+"')\n")
    fn.write("track_off(trk_sub,"+str(drot_az[i]/N.cos((rot_alt[i])/180.*math.pi))+","+str(drot_alt[i])+",timeout=5)")
    fn.write("   #  " + str(int(drot_az[i]/N.cos((rot_alt[i])/180.*math.pi)*3600))+'", '+str(int(drot_alt[i]*3600))+'"\n')
    fn.write("corrapi_fstrt.fstart_proj(CORR,cor_sub,'"+name+"')\n")

    # Changed from individual commands for Azimtuth and Elevation(altitude) offset to a common command for both, which
    # being used earlier as well. This saves some execution time.
    # *** Div 30Apr2019 ***
    #fn.write("trkazoff(" + str(int(drot_az[i]/N.cos((rot_alt[i])/180.*math.pi)*3600)) +'")\n')
    #fn.write("trkeloff(" + str(int(drot_alt[i]*3600))+'")\n')
    # *** Div 30Apr2019 ***
    #fn.write("sndsacsrc(1,12h)\n")
    #fn.write("time 10s\n")
    #fn.write("stabct\n")
    #fn.write("enacmd\n")
    #fn.write("strtndas\n\n")

    #tt = libs.convert_time(times[i])
    #print "%i %i %i %i %.2f %.2f" %(i, tt[0], tt[1], int(round(tt[2])), drot_alt[i], drot_az[i]/N.cos((rot_alt[i])/180.*math.pi))

  #fn.write("time 120s\n")
  fn.write("# end\n")
  #fn.write("stpndas\n")
  #fn.write("end\n")

  fn.close()

#if __name__ == "antennaframe":
antennaframe(freq=330.e6)

