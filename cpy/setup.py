# from setuptools import setup
# from Cython.Build import cythonize

# setup(
#     ext_modules = cythonize("utils.pyx")
# )
from distutils.core import setup, Extension

module1 = Extension('cpyutils',
                    include_dirs = ["C:/Users/omine/Documents/programs/customBlender/lib/win64_vc15/python/39/include","C:/Users/omine/Documents/programs/customBlender/lib/win64_vc15/python/39/libs"],
                    library_dirs = ['C:/Users/omine/Documents/programs/customBlender/lib/win64_vc15/python/39/libs'],
                    sources = ['cpyutils.c'])

setup (name = 'PackageName',
       version = '1.0',
       description = 'This is a demo package',
       ext_modules = [module1])