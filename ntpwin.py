"""
    set_systemtime_from_ntp.py

    Copyright (c) 2016, Masatsuyo Takahashi


### Jsonify it!

"""
import ntplib
import datetime
from ctypes             import Structure, windll, pointer
from ctypes.wintypes    import WORD

NTPSERVER = 'ntp.br'



class SYSTEMTIME(Structure):
  _fields_ = [
      ( 'wYear',            WORD ),
      ( 'wMonth',           WORD ),
      ( 'wDayOfWeek',       WORD ),
      ( 'wDay',             WORD ),
      ( 'wHour',            WORD ),
      ( 'wMinute',          WORD ),
      ( 'wSecond',          WORD ),
      ( 'wMilliseconds',    WORD ),
    ]
SetLocalTime = windll.kernel32.SetLocalTime

c = ntplib.NTPClient()
response = c.request(NTPSERVER, version=3)

# print("---")
# print(response.dest_time)
# print("---")

dt_ = datetime.datetime.fromtimestamp( response.tx_time )
print( 'Got time as', dt_.strftime( '%Y-%m-%d %H:%M:%S'), 'from NTP Server', NTPSERVER)

dt_tuple = dt_.timetuple()
st = SYSTEMTIME()
st.wYear            = dt_tuple.tm_year
st.wMonth           = dt_tuple.tm_mon
st.wDayOfWeek       = ( dt_tuple.tm_wday + 1 ) % 7
st.wDay             = dt_tuple.tm_mday
st.wHour            = dt_tuple.tm_hour + 4 # America/Manaus
st.wMinute          = dt_tuple.tm_min
st.wSecond          = dt_tuple.tm_sec
st.wMilliseconds    = 0

ret = SetLocalTime(pointer(st))
if ret == 0:
    print('ERROR: Setting failed. Try as administrator.')
    print('ERROR: 11')
    exit(11)
else:
    print( 'LOG: 00100 - Successfully set the systemtime from %s.' % NTPSERVER)
