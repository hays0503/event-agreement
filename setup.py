import sys
import os
import requests
from cx_Freeze import setup, Executable


dll = [('addlibs/msvcp_win.dll', os.path.join('lib', 'msvcp_win.dll')),
       ('addlibs/msvcp60.dll', os.path.join('lib', 'msvcp60.dll')),
       ('addlibs/msvcp100.dll', os.path.join('lib', 'msvcp100.dll')),
       ('addlibs/msvcp110_win.dll', os.path.join('lib', 'msvcp110_win.dll')),
       ('addlibs/msvcp110.dll', os.path.join('lib', 'msvcp110.dll')),
       ('addlibs/msvcp120.dll', os.path.join('lib', 'msvcp120.dll')),
       ('addlibs/msvcp120_clr0400.dll', os.path.join('lib', 'msvcp120_clr0400.dll')),
       ('addlibs/msvcp140.dll', os.path.join('lib', 'msvcp140.dll')),
       ('addlibs/msvcp140_1.dll', os.path.join('lib', 'msvcp140_1.dll')),
       ('addlibs/msvcp140_1d.dll', os.path.join('lib', 'msvcp140_1d.dll')),
       ('addlibs/msvcp140_2.dll', os.path.join('lib', 'msvcp140_2.dll')),
       ('addlibs/msvcp140_2d.dll', os.path.join('lib', 'msvcp140_2d.dll')),
       ('addlibs/msvcp140_atomic_wait.dll',
        os.path.join('lib', 'msvcp140_atomic_wait.dll')),
       ('addlibs/msvcp140_clr0400.dll', os.path.join('lib', 'msvcp140_clr0400.dll')),
       ('addlibs/msvcp140_codecvt_ids.dll',
        os.path.join('lib', 'msvcp140_codecvt_ids.dll')),
       ('addlibs/msvcp140d.dll', os.path.join('lib', 'msvcp140d.dll')),
       ('addlibs/msvcp140d_atomic_wait.dll',
        os.path.join('lib', 'msvcp140d_atomic_wait.dll')),
       ('addlibs/msvcp140d_codecvt_ids.dll',
        os.path.join('lib', 'msvcp140d_codecvt_ids.dll')),
       ('addlibs/ucrtbased.dll', os.path.join('lib', 'ucrtbased.dll')),
       ('addlibs/vcruntime140.dll', os.path.join('lib', 'vcruntime140.dll')),
       ('addlibs/vcruntime140_1.dll', os.path.join('lib', 'vcruntime140_1.dll')),
       ('addlibs/vcruntime140_1d.dll', os.path.join('lib', 'vcruntime140_1d.dll')),
       ('addlibs/vcruntime140_clr0400.dll',
        os.path.join('lib', 'vcruntime140_clr0400.dll')),
       ('addlibs/vcruntime140d.dll', os.path.join('lib', 'vcruntime140d.dll')),
       ('addlibs/ws2_32.dll', os.path.join('lib', 'ws2_32.dll')),
       ('addlibs/ws2_32.dll.mui', os.path.join('lib', 'ws2_32.dll.mui'))]

icon = [('icon/info_msg_works.png', os.path.join('icon', 'info_msg_works.png')),
        ('icon/info_msg_warning.png', os.path.join('icon', 'info_msg_warning.png')),
        ('icon/info_icon.png', os.path.join('icon', 'info_icon.png')),
        ('icon/icon.png', os.path.join('icon', 'icon.png')),
        ]

# создаем список модулей и файлов для включения в сборку
include_files = [('ControllerIronLogic.dll', os.path.join('lib', 'ControllerIronLogic.dll')),
                 ('ZGuard.dll', os.path.join('lib', 'ZGuard.dll')),
                 ('config.ini', os.path.join('.', 'config.ini')),
                 *icon,
                 *dll]


build_exe_options = {"includes": ["IronLogic",
                                  "ControllerInstance",
                                  "ConverterInstance",
                                  "IronLogicApiDll",
                                  "os",
                                  "psycopg2",
                                  "threading",
                                  "queue",
                                  "aiohttp",
                                  "asyncio",
                                  "json",
                                  "pytz"],
                     "zip_include_packages": ["PySide6"],
                     'include_files': include_files,
                     "excludes": ["tkinter", "unittest", "PySide6.examples"],
                     "include_msvcr": True}

base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

target = Executable(
    script="IronLogic.py",
    base=base,
    icon="terminal.ico"
)


setup(name="ЭмуляторСетевыхКонтролеровIronLogic",
      version="0.1",
      requires=["requests"],
      description="ЭмуляторСетевыхКонтролеровIronLogic",
      options={"build_exe": build_exe_options},
      executables=[target])
