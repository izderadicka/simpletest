Simple testing tool for programs interacting via terminal. Runs program,  feeds inputs and tests that output matches expected lines in test script.

usage: stest test_script.txt [program [arguments]]

test script (note **space** between first character and rest of line_:
```
# Any Comment
# Program to execute - can have parameters
$ tests/test1.sh
# Expected output lines
> Hey you
> What's your name?
# Feed input
< Ivan
> Hello Ivan
# Tests return code
? 0
# End of test case can start next one
---
$ tests/test1.sh
> Hey you
> What's your name?
< Gustav
> To hell with you
? 1 
```

Two \ at the end of output check will match incomplete line:
```
$ tests/test2.sh
> Your wish:\\
< mys
> mys
? 0
---
```

Also one might need input without EOL.  Or input of  of control characters (Crtl-d, Ctrl-c  ...).  
There is also shortcut for for closing stdin (aka Ctrl-d) - its line x:
```
$ tests/test3.sh
> Enter empty:\\
< \\Ctrl-d
? 0
---
$ tests/test3.sh
> Enter empty:\\
x
? 0
---
```

Program to test is either in script on $ line or can be passed as parameter to stest.

To install:

```
pip install git+https://github.com/izderadicka/simpletest.git#egg=simpletest
```