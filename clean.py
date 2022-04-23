'''
清理临时文件夹和工作空间，用来打包发给大家（）
'''
import os
import shutil

pydir = os.path.dirname(os.path.abspath(__file__))

shutil.rmtree(os.path.join(pydir, '_build'), ignore_errors=True)
shutil.rmtree(os.path.join(pydir, '_temp'), ignore_errors=True)
shutil.rmtree(os.path.join(pydir, '_workspace'), ignore_errors=True)
