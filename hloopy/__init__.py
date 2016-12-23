from . import extract
from . import util
from . import plotters
from hloopy.hloop import HLoop
import os
from os import path as _path
import sys
from importlib import import_module

# def getClasses(directory):
#     classes = {}
#     oldcwd = os.getcwd()
#     os.chdir(directory)   # change working directory so we know import will work
#     for filename in os.listdir(directory):
#         if filename.endswith(".py"):
#             modname = filename[:-3]
#             classes[modname] = getattr(__import__(modname), modname)
#     os.setcwd(oldcwd)
#     return classes

# homepath = os.getenv('HOME')
# configpath = join(homepath, '.config', 'hloopy')
# sys.path.append(configpath)
# if _path.exists(configpath):
#     oldpath = os.get_cwd() 
#     os.chdir(configpath)
#     contents = os.listdir(configpath)
#     for c in contents:
#         try:
#             module = __import__(c, globals(), locals())
#             globals().update(module.__dict__)
#         except:
#             pass
#     os.chdir(oldpath)



