
# parameter file for create_posn_file.py
source = '3C286'
date = (15,9,2024)      # dd, mm, yy
time0 = 9.5      # IST hh.hh
grid1d = 15             # num of points one each side
total_dist = 310.0      # total distance in arcmin from end to end (~75' for L-band; 324' for 325 MHz)
tot_time_per = 120     # total time for pointing + slew in seconds
ncal = 2		# number of times tot_time_per in seconds for calibration
axis1d = 'alt'		# if doing create_posn_file_1d
cmdfile = "15sep-3c286b_subarray2-9_30hrs.txt"
'''

source = '3C147'
date = (15,9,2024)      # dd, mm, yy
time0 = 1.912      # IST hh.hh
grid1d = 15             # num of points one each side
total_dist = 310.0      # total distance in arcmin from end to end (~75' for L-band; 324' for 325 MHz)
tot_time_per = 120     # total time for pointing + slew in seconds
ncal = 2		# number of times tot_time_per in seconds for calibration
axis1d = 'alt'		# if doing create_posn_file_1d
cmdfile = "15sep-3c147b_subarray2-1:55hrs.txt"

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
