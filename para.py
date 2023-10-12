
# parameter file for create_posn_file.py

'''
source = '3C286'
date = (14,2,2017)      # dd, mm, yy
time0 = 11.25            # IST hh.hh
grid1d = 9             # num of points one each side, create_posn_file_2d generates a grid of grid1d x grid1d (320 arcmin for 90cm)
total_dist = 156.0      # total distance in arcmin from end to end
tot_time_per = 60.0     # total time in seconds for pointing + slew in seconds for each grid point
ncal = 2		# number of times tot_time_per in seconds for calibration
axis1d = 'az'		# if doing create_posn_file_1d, ignored by create_posn_file_2d
cmdfile = 'dummy-1.cmd'
'''

source = '3C147'
date = (16,9,2021)      # dd, mm, yy
time0 = 02.00           # IST hh.hh
grid1d = 15             # num of points one each side
total_dist = 310.0      # total distance in arcmin from end to end (~75' for L-band; 324' for 325 MHz)
tot_time_per = 59.999     # total time for pointing + slew in seconds
ncal = 2		# number of times tot_time_per in seconds for calibration
axis1d = 'alt'		# if doing create_posn_file_1d
cmdfile = "16sep-310a-3c147a-0200hrs.cmd"
'''
'''

'''
source = '3C48'
date = (5,2,2020)      # dd, mm, yy
time0 = 17.5           # IST hh.hh
grid1d = 17            # num of points one each side 
total_dist = 480.0      # total distance in amin from end to end (90 for first null to first null, = 324' for 90cm, use 448 for 90cm)
tot_time_per = 60.0001     # total time for pointing + slew in seconds
ncal = 2		# number of times tot_time_per in seconds for calibration
axis1d = 'az'		# if doing create_posn_file_1d
cmdfile = "3c48-17g-1730hrs.cmd"
'''

# cmdfile1 has 14 points, 200' on each side
# 448' is used for band-3
