#!/usr/bin/env python3
# See LICENSE file for copyright and license details.

import sys, os, pwd, time
import solar_python as sol


loc = None
stop_date = None
human = False
noon = False
blue = False
gold = False
unblue = False
ungold = False
morning = []
evening = []
deriv = []


## Parse command line
argv0 = sys.argv[0] if len(sys.argv) > 0 else 'blue'
def usage():
    opts = '[-e elev]* [-m elev]* [-d delev]* [-l lat:lon | -l loc] [-s year-month-day | -s -] [-bBgGhn]'
    print('Usage: %s %s' % (argv0, opts), file = sys.stderr)
    sys.exit(1)
i, n = 1, len(sys.argv)
def getarg():
    global i, j, n, m
    if j < m:
        rc = arg[j]
        j = m
        return rc
    else:
        j = m
        i += 1
        if i == n:
            usage()
        return sys.argv[i]
while i < n:
    arg = sys.argv[i]
    if arg == '--':
        i += 1
        break
    elif arg.startwith('-'):
        j, m = 1, len(arg)
        while j < m:
            c = arg[j]
            j += 1
            if c == 'd':
                deriv.append(getarg())
            elif c == 'e':
                evening.append(getarg())
            elif c == 'm':
                morning.append(getarg())
            elif c == 'l':
                loc = getarg()
            elif c == 's':
                stop_date = getarg()
            elif c == 'b':
                blue = True
            elif c == 'B':
                unblue = True
            elif c == 'g':
                gold = True
            elif c == 'G':
                ungold = True
            elif c == 'h':
                human = True
            elif c == 'n':
                noon = True
            else:
                usage()
            j += 1
        i += 1
    else:
        break
if i != n:
    usage()


## Parse elevations
try:
    evening = [float(e) for e in evening]
    morning = [float(e) for e in morning]
    deriv   = [float(e) for e in deriv]
    for e in evening + morning:
        if abs(e) > 90:
            usage()
except:
    usage()


## Parse -bBgGn
if blue:
    morning.append(sol.SOLAR_ELEVATION_RANGE_BLUE_HOUR[0])
    evening.append(sol.SOLAR_ELEVATION_RANGE_BLUE_HOUR[1])
if unblue:
    morning.append(sol.SOLAR_ELEVATION_RANGE_BLUE_HOUR[1])
    evening.append(sol.SOLAR_ELEVATION_RANGE_BLUE_HOUR[0])
if gold:
    morning.append(sol.SOLAR_ELEVATION_RANGE_GOLDEN_HOUR[0])
    evening.append(sol.SOLAR_ELEVATION_RANGE_GOLDEN_HOUR[1])
if ungold:
    morning.append(sol.SOLAR_ELEVATION_RANGE_GOLDEN_HOUR[1])
    evening.append(sol.SOLAR_ELEVATION_RANGE_GOLDEN_HOUR[0])
if noon:
    deriv.append(0.0)


## Fallback options
if len(morning) == 0 and len(evening) == 0 and len(deriv) == 0:
    morning.append(sol.SOLAR_ELEVATION_RANGE_BLUE_HOUR[0])
    evening.append(sol.SOLAR_ELEVATION_RANGE_BLUE_HOUR[1])


## Get geolocation
def get_geolocation_from_conf(filename, ispath = False):
    filenames, lat, lon = [], None, None
    if ispath:
        filenames.append(filename)
    else:
        if 'HOME' in os.environ and len(os.environ['HOME']) > 0:
            filenames.append(os.environ['HOME'] + '/.config/' + filename)
        try:
            filenames.append(pwd.getpwuid(os.getuid()).pw_dir + '/.config/' + filename)
        except:
            pass
        filenames.append('/etc/' + filename)
    for filename in filenames:
        try:
            with open(filename, 'rb') as file:
                loc = file.read().decode('utf-8', 'replace').split('\n')[0]
            (lat, lon) = loc.split(' ')
            lat, lon = float(lat), float(lon)
            break
        except:
            lat, lon = None, None
    return (lat, lon)
if loc is not None:
    try:
        (lat, lon) = loc.split(':')
        lat = float(lat)
        lon = float(lon)
        if (abs(lat) > 90 or abs(lon) > 180):
            lat = None
    except:
        lat = None
    if lat is None:
        if loc.startswith('./') or loc.startswith('../') or loc.startswith('/'):
            locfile = loc
        else:
            locfile = 'geolocation.d/' + loc
        (lat, lon) = get_geolocation_from_conf(locfile, locfile is loc)
    if lat is None:
        print('%s: bad location: %s' % (argv0, loc), file = sys.stderr)
        sys.exit(1)
else:
    (lat, lon) = get_geolocation_from_conf('geolocation')
    if lat is None:
        print('%s: no geolocation set' % argv0, file = sys.stderr)
        sys.exit(1)


## Parse stop date
if stop_date is not None:
    if stop_date == '-':
        stop_date = ...
    else:
        try:
            tm = time.strptime(stop_date, '%Y-%m-%d')
            stop_date = (tm.tm_year, tm.tm_mon, tm.tm_mday)
        except:
            usage()
else:
    tm = time.localtime()
    if tm.tm_mon < 12:
        stop_date = (tm.tm_year, tm.tm_mon + 1, tm.tm_mday)
    else:
        stop_date = (tm.tm_year + 1, 1, tm.tm_mday)


## Get stop time
if stop_date is ...:
    stop_time = None
else:
    stop_time = '%i-%02i-%02i 12:00:00' % stop_date
    guessed = time.mktime(time.strptime(stop_time, '%Y-%m-%d %H:%M:%S'))
    is_summer = False
    for tzname, summer in zip(time.tzname, (False, True)):
        if time.mktime(time.strptime('%s %s' % (stop_time, tzname), '%Y-%m-%d %H:%M:%S %Z')) == guessed:
            is_summer = summer
            break
    (y, m, d) = stop_date
    days = 29 if y % 400 == 0 or (y % 4 == 0 and not y % 100 == 0) else 28
    days = [31, days, 31, 30, 31, 30, 30, 31, 30, 31, 30, 31]
    stop_time = d - 1
    for i in range(m - 1):
        stop_time += days[i]
    y -= 1
    stop_time +=    y * 365 +    y // 4 -    y // 100 +    y // 400
    stop_time -= 1969 * 365 + 1969 // 4 - 1969 // 100 + 1969 // 400
    stop_time *= 24 * 60 * 60
    stop_time += 24 * 60 * 60
    stop_time -= (time.altzone if is_summer else time.timezone)

