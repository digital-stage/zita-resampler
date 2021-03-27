#if WIN32

#pragma once

// https://stackoverflow.com/questions/5404277/porting-clock-gettime-to-windows
#define WIN32_LEAN_AND_MEAN
#include <windows.h>

// Unused first parameter
#define CLOCK_REALTIME 1 
int clock_gettime(int, struct timespec* spec)      //C-file part
{
	__int64 wintime; GetSystemTimeAsFileTime((FILETIME*)&wintime);
	wintime -= 116444736000000000i64;  //1jan1601 to 1jan1970
	spec->tv_sec = wintime / 10000000i64;           //seconds
	spec->tv_nsec = wintime % 10000000i64 * 100;      //nano-seconds
	return 0;
}
#endif
