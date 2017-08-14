from distutils.core import setup, Extension
setup(name='pyptrace', version='1.0',  \
      ext_modules=[Extension('pyptrace', ['pyptrace.c'])])
