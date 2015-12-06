Simple testing tool for programs interacting via terminal. Runs program,  feeds inputs and tests that output matches expected lines in test script.

usage: stest test_script.txt [program [arguments]]

test script:
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

Program to test is either in script on $ line or can be passed as parameter to stest.

To install:

```
pip install https://github.com/izderadicka/simpletest.git#egg=simpletest
```