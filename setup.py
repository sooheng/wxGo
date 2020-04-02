# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe
import sys
 
#this allows to run it with a simple double click.
sys.argv.append('py2exe')
 
py2exe_options = {
        "includes": ["wx"],
        "compressed": 1,
        "optimize": 2,
        "ascii": 0,
        "bundle_files": 3,
        "dll_excludes": [
            "MSVCP90.dll",
            'api-ms-win-core-atoms-l1-1-0.dll',
            'api-ms-win-core-com-midlproxystub-l1-1-0.dll',
            'api-ms-win-core-debug-l1-1-0.dll',
            'api-ms-win-core-delayload-l1-1-0.dll',
            'api-ms-win-core-delayload-l1-1-1.dll',
            'api-ms-win-core-errorhandling-l1-1-0.dll',
            'api-ms-win-core-errorhandling-l1-1-1.dll',
            'api-ms-win-core-file-l1-2-1.dll',
            'api-ms-win-core-handle-l1-1-0.dll',
            'api-ms-win-core-heap-l2-1-0.dll',
            'api-ms-win-core-heap-l1-2-0.dll',
            'api-ms-win-core-heap-obsolete-l1-1-0.dll',
            'api-ms-win-core-interlocked-l1-1-0.dll',
            'api-ms-win-core-memory-l1-1-0.dll',
            'api-ms-win-core-libraryloader-l1-2-0.dll',
            'api-ms-win-core-libraryloader-l1-2-1.dll',
            'api-ms-win-core-localization-l1-2-0.dll',
            'api-ms-win-core-localization-l1-2-1.dll',
            'api-ms-win-core-profile-l1-1-0.dll',
            'api-ms-win-core-processthreads-l1-1-0.dll',
            'api-ms-win-core-processthreads-l1-1-1.dll',
            'api-ms-win-core-processthreads-l1-1-2.dll',
            'api-ms-win-core-psapi-l1-1-0.dll',
            'api-ms-win-core-registry-l1-1-0.dll',
            'api-ms-win-core-string-l1-1-0.dll',
            'api-ms-win-core-string-l2-1-0.dll',
            'api-ms-win-core-string-obsolete-l1-1-0.dll',
            'api-ms-win-core-synch-l1-1-0.dll',
            'api-ms-win-core-synch-l1-2-0.dll',
            'api-ms-win-core-sysinfo-l1-1-0.dll',
            'api-ms-win-core-sysinfo-l1-2-1.dll',
            'api-ms-win-core-threadpool-legacy-l1-1-0.dll',
            'api-ms-win-crt-private-l1-1-0.dll',
            'api-ms-win-crt-runtime-l1-1-0.dll',
            'api-ms-win-crt-string-l1-1-0.dll',
            'api-ms-win-eventing-provider-l1-1-0.dll',
            'api-ms-win-security-base-l1-1-0.dll',
            'api-ms-win-security-base-l1-2-0.dll'
          ],
        }
 
setup(
      name = 'PyGo Demo',
      version = '1.0',
      windows = [{ "script":'main.py',"icon_resources":[(1,"panda.ico")]}], 
      zipfile = None,
      options = {'py2exe': py2exe_options},
      data_files = ['back.png', 'logo.jpg', 'panda.ico']
      )