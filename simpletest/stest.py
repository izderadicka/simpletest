# Simple test utility for command line programs
from __future__ import print_function
import sys
import os.path
import pexpect
import re

def main():
    if len(sys.argv) < 2:
        print('Usage: %s test_script [program [program_arguments]]' % os.path.split(sys.argv[0])[-1], file=sys.stderr)
        sys.exit(1)
        
    test_file= sys.argv[1]
    if not os.access(test_file, os.R_OK):
        print("File %s does not exists or is not readable"% test_file)
        sys.exit(1)
        
        
    prog=sys.argv[2] if len(sys.argv)>2 else None
    if prog and not os.access(prog, os.X_OK):
        print("Program %s does not exists or is not executable"% prog)
        sys.exit(1)
        
    with open(test_file) as f:
        try:
            run_tests(prog, sys.argv[2:], f)
        except (ScriptError, ProgramError) as e:
            print(str(e), file=sys.stderr)
            print()
            sys.exit(2)
        print('\nAll OK :-)')


class TestError(Exception):
    def __str__(self):
        if hasattr(self, 'msg') and self.msg:
            return self.msg
        else:
            return repr(self)
        
class ScriptError(TestError):
    def __init__(self, line_no, line, msg):
        self.msg='SCRIPT ERROR at line %d (%s): %s'% (line_no, line.rstrip(), msg)

class ProgramError(TestError):
    def __init__(self, line_no,line,  msg):
        self.msg='PROGRAM ERROR at line %d (%s): %s'% (line_no, line.rstrip(), msg)
    

PEXPECT_KWARGS=dict(timeout=5, echo=False)
def run_tests(prog, prog_args, f): 
    p=None  
    if prog:
        p=pexpect.spawn(prog, prog_args, **PEXPECT_KWARGS) 
    for i,l in enumerate(f):
        if l.startswith('#'):
            continue
        print(i,l,end='')
        
        if l.startswith('---'):
            if p:
                p.terminate(force=True)
            if prog:
                p=pexpect.spawn(prog, prog_args, **PEXPECT_KWARGS) 
            continue
        try:
            s=l.split(' ',1)
            c=s[0].strip()
            t=s[1] if len(s)>1 else ''
        except ValueError:
            raise ScriptError(i,l, 'Invalid line')
        
        if c=='$':
            if p:
                p.terminate(force=True)
            prog=t.split()[0]
            prog=pexpect.which(prog)
            if not os.access(prog, os.X_OK):
                raise ScriptError(i,l, 'Program %s not found or not executable' % prog)
            p =  pexpect.spawn(t, **PEXPECT_KWARGS) 
        
        elif c =='>':
            
            if not p:
                raise ScriptError(i,l, 'No program defined')
            if t.endswith('\\\\\n'):
                t=t[:-3]
            else:
                t=re.sub(r'(?<!\r)\n$', '\r\n', t)
            try:
                p.expect_exact(t)
            except pexpect.EOF:
                raise ProgramError(i,l,'Program ended before expected output, with this output: %s' % p.before)
            except pexpect.TIMEOUT:
                raise ProgramError(i,l, 'Program does not provided expected output but this %s' % p.before)
            if p.before:
                raise ProgramError(i,l,'Program provided additional output %s' % p.before)
            
        elif c =='<':
            if not p:
                raise ScriptError(i,l, 'No program defined')
            if t.endswith('\\\\\n'):
                t=t[:-3]
            ctl= re.match(r'\\\\Ctrl-(\w)\n$', t, re.IGNORECASE) 
            if ctl:
                p.sendcontrol(ctl.group(1))
            else:    
                p.send(t)
        elif c=='x' or c=='X':
            if not p:
                raise ScriptError(i,l, 'No program defined')
            p.sendcontrol('d')
        elif c=='?':
            try:
                exp_code=int(t)
            except ValueError:
                raise ScriptError(i,l, 'Invalid return code')
            try:
                p.expect(pexpect.EOF)
            except pexpect.TIMEOUT:
                raise ProgramError(i,l,'Program should finish')
            if p.before:
                raise ProgramError(i,l,'Program provided additional output %s' % p.before)
            ret=p.wait()
            if ret != exp_code:
                raise ProgramError(i,l, 'Return code %d is different from expected %d' % (ret, exp_code))
            
        else:
            raise ScriptError(i,l, 'Invalid line, cmd is "%s"'%c)
  

if __name__=='__main__' :
    main()     