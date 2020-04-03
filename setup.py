# -*- coding: utf-8 -*-

import sys
from distutils.core import setup

from src import image_background, image_icon, image_logo


def is_python3():
    """ 是否Python3 """
    return sys.version_info >= (3,)


# this allows to run it with a simple double click.
sys.argv.append('py2exe')

build_options = {
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
    name='PyGo Demo',
    version='1.1',
    windows=[{"script": 'main.py', "icon_resources": [(1, image_icon)]}],
    zipfile=None,
    options={'py2exe': build_options},
    data_files=[
        ("images", [image_background, image_icon, image_logo]),
        ("screens", []),
    ],
)
