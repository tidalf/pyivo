import sys

try:
    try:
        import py2exe.mf as modulefinder
    except ImportError:
        import modulefinder
    import win32com
    for p in win32com.__path__[1:]:
        modulefinder.AddPackagePath("win32com", p)
    for extra in ["win32com.mapi"]:
        __import__(extra)
        m = sys.modules[extra]
        for p in m.__path__[1:]:
            modulefinder.AddPackagePath(extra, p)
except ImportError:
    pass

from distutils.core import setup
import py2exe
import sys
import os
import shutil
import re

version = 0
post_build_files = ['msvcr90.dll', 'Microsoft.VC90.CRT.manifest', 'config.yaml']
delete_list = []

def get_revision_number():
    global version
    version = re.findall('Rev: (\\d+)',os.popen('svn info').read())[0]

if 'py2exe' in sys.argv:
    get_revision_number()

excludes = [
   "Tkinter",
   "doctest",
   "unittest",
   "pydoc",
   "pdb",
   "win32ui"
]

dll_excludes = [
   "API-MS-Win-Core-LocalRegistry-L1-1-0.dll",
   "MPR.dll",
   "MSWSOCK.DLL",
   "POWRPROF.dll",
   "profapi.dll",
   "userenv.dll",
   "w9xpopen.exe",
   "wtsapi32.dll",
   "Secure32.dll",
   "SHFOLDER.dll",
   "MAPI32.dll"
]
setup(console=[
    {'icon_resources': [(0, "mapi_calc.ico")],
     'script': 'mapi_calc.py'}
    ],
      options={'py2exe' : {"bundle_files": 1, 
			   "dll_excludes": dll_excludes,
			   "excludes": excludes}},
      zipfile = None,
      version='0.%s' %str(version),
      description='MapiCalc - simple mailbox statistics tool',      
      author='alex.ieshin@gmail.com'
)    

for f in post_build_files:
    shutil.copyfile(f,os.path.join('dist',f))
for f in delete_list:
    if os.path.exists(os.path.join('dist',f)):
	os.unlink(os.path.join('dist',f))
