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

def adjust_handlers_module():
    if os.path.exists('handlers') and os.path.isdir('handlers'):
        all_list =  [item.split('.')[0] for item in os.listdir('handlers') if item.endswith('.py') and ( item not in ['__init__.py'])]
        fp = file('handlers/__init__.py', 'w')
        fp.write('__all__ = %s' %str(all_list))
        fp.close()


def get_revision_number():
    global version
    version = re.findall('Rev: (\\d+)',os.popen('svn info').read())[0]

if 'py2exe' in sys.argv:
    get_revision_number()
    adjust_handlers_module()

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
    {'icon_resources': [(0, "yivo.ico")],
     'script': 'yivo_run.py'}
    ],
      options={'py2exe' : {"bundle_files": 1, 
			   "dll_excludes": dll_excludes,
			   "packages": ["handlers"],
			   "excludes": excludes}},
      zipfile = None,
      version='0.%s' %str(version),
      description='Yivo - mapi properties collecting tool',      
      author='alex.ieshin@gmail.com'
)    

for f in post_build_files:
    shutil.copyfile(f,os.path.join('dist',f))
for f in delete_list:
    if os.path.exists(os.path.join('dist',f)):
	os.unlink(os.path.join('dist',f))

fp = file('handlers/__init__.py', 'w')
fp.close()
