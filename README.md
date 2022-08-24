# errno_converter & signal_converter & http_converter
As simple command line tool to convert error numbers (of **C errno.h**), **signal**
numbers and HTTP-Status-Codes to human readable strings or back to numbers.
This tool makes use of `errno`, `signal` and `http` module of Python 3.8 
standard library (Python 3.8 added support for verbose signal descriptions).

## Example usage of `errno_converter`:
```bash
$ errno_converter.py
./dev/errno_converter/errno_converter.py [-v] list|<errno-number>|<errno-name>

$ errno_converter.py ENOENT
2

$ errno_converter.py -v ENOENT
  2 - ENOENT         : No such file or directory

$ errno_converter.py 2
ENOENT

$ errno_converter.py -v 2
  2 - ENOENT         : No such file or directory

$ errno_converter.py ENOE
  2 - ENOENT
  8 - ENOEXEC

$ errno_converter.py -v ENOE
No errno matched the input 'ENOE' (module 'errno' has no attribute 'ENOE'). Try to match as re:
  2 - ENOENT         : No such file or directory
  8 - ENOEXEC        : Exec format error

$ errno_converter.py list
  1 - EPERM
  2 - ENOENT
…
130 - EOWNERDEAD
131 - ENOTRECOVERABLE

$ errno_converter.py -v list
  1 - EPERM          : Operation not permitted
  2 - ENOENT         : No such file or directory
…
130 - EOWNERDEAD     : Owner died
131 - ENOTRECOVERABLE: State not recoverable
invalids: {41, 58}
```

## Example usage of `signal_converter`:
```bash
$ signal_converter.py
signal_converter.py [-v] list|<errno-number>|<errno-name>

$ signal_converter.py SIGINT
2

$ signal_converter.py -v SIGINT
  2 - SIGINT         : Interrupt

$ signal_converter.py 2
SIGINT

$ signal_converter.py -v 2
  2 - SIGINT         : Interrupt

$ signal_converter.py SIGIO.*
 29 - SIGIO
  6 - SIGIOT

~$ signal_converter.py -v SIGIO.*
No signal matched the input 'SIGIO.*' (module 'signal' has no attribute 'SIGIO.*'). Try to match as re:
 29 - SIGIO          : I/O possible
  6 - SIGIOT         : Aborted

$ signal_converter.py list
  1 - SIGHUP
  2 - SIGINT
…
 34 - SIGRTMIN
 64 - SIGRTMAX

$ signal_converter.py -v list
  1 - SIGHUP         : Hangup
  2 - SIGINT         : Interrupt
…
 34 - SIGRTMIN       : Real-time signal 0
 64 - SIGRTMAX       : Real-time signal 30
invalids: {16, 32, 33, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63}
```

# Installation
```bash
pip install errno-converter
```
