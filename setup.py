from os.path import os
import re
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
   
    
pkg_file= os.path.join(os.path.split(__file__)[0],  'simpletest', '__init__.py')

m=re.search(r"__version__\s*=\s*'([\d.]+)'", open(pkg_file).read())
if not m:
    print >>sys.stderr, 'Cannot find version of package'
    sys.exit(1)

version= m.group(1)



setup(name='simpletest',
      version=version,
      description='Tool to test programs interacting via terminal',
      url='http://zderadicka.eu/projects/python/imap_detach-tool-download-email-attachments/',
      package_dir={'':'.'},
      packages=['simpletest', ],
      scripts=['stest'],
      author='Ivan Zderadicka',
      author_email='ivan.zderadicka@gmail.com',
      license = 'GPL v3',
      install_requires=['pexpect>=4.0.1',
                        ],
      provides=['simpletest'],
      keywords=['testing',],
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                   'Natural Language :: English',
                   'Operating System :: POSIX',
                   'Programming Language :: Python :: 2.7',
                   ]
      
      )