================
Yaybu on Windows
================

This process has been observed to work on 32-bit Windows XP.

Getting this repository
=======================

We originally tested with GitHub's GUI, which comes with some POSIXy tools in a directory like this::

    C:\Documents and Settings\SomeUser\Local Settings\Application Data\GitHub\PortableGit_015aa71ef18c047ce8509ffb2f9e4bb0e3e73f13\bin

Putting this on PATH allows pip to work with git:// based eggs.

An alternative is the proper Git installer https://msysgit.googlecode.com/files/Git-1.8.3-preview20130601.exe

Once you have working git you can just::

    git clone git://github.com/isotoma/Yaybu.exe C:\Yaybu.exe


Set up your build environment
=============================

Install python2.7, py2exe, pycrypto from installers:

 * http://www.python.org/ftp/python/2.7.5/python-2.7.5.msi
 * http://downloads.sourceforge.net/project/py2exe/py2exe/0.6.9/py2exe-0.6.9.win32-py2.7.exe
 * http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win32-py2.7.exe

Install mingw32 using the installer (http://sourceforge.net/projects/mingw/files/Automated%20MinGW%20Installer/mingw-get/)::

    mingw-get install gcc
    mingw-get install mingw-utils

At the time of writing this seems to yield a broken environment - so copy some DDL's around. To fix cc1plus::

    copy bin\libgmp-10.dll libexec\gcc\mingw32\4.7.2\
    copy bin\libmpc-2.dll libexec\gcc\mingw32\4.7.2\
    copy bin\libmpfr-1.dll libexec\gcc\mingw32\4.7.2\

It might be that ``libgcc_s_dw2-1.dll``, ``libiconv-2.dll`` or ``libintl-8.dll`` need similar.

We need to generate a def file and then a ``a`` file before we'll be able to build against our Python install::

    cd c:\Python27\libs
    pexports c:\windows\system32\python27.dll > python26.def 
    dlltool -C -d python27.def -l libpython27.a

You can check the exported symbols with nm (look for ``I`` for import symbol)::

    nm libpython27.a

Python needs to be told to use mingw32. You can do this with a ``C:\Python27\Lib\distutils\distutils.cfg``::

    [build]
    compiler=mingw32

The default site.py has an abs_file that seems to break when using py2exe. Patch abs_file to catch ImportErrors::

     def abs__file__():
         """Set all module' __file__ attribute to an absolute path"""
         for m in sys.modules.values():
             if hasattr(m, '__loader__'):
                 continue   # don't mess with a PEP 302-supplied __file__
             try:
                 m.__file__ = os.path.abspath(m.__file__)
    -        except (AttributeError, OSError):
    +        except (AttributeError, OSError, ImportError):
                 pass

Install setuptools using the ez_setup.py script provided::

    C:\Python27\python ez_setup.py

py2exe will break with setuptools because it is compressed. A better way to deal with it is needed, but for now::

    C:\Python27\python -m easy_install --always-unzip --upgrade "setuptools<1.0"

(You can upgrade to the active version because it detects it is already the latest version).

Then install pip and get the requirements::

    C:\Python27\python -m easy_install pip
    C:\Python27\python -m pip install -r requirements.txt


Building an exe
===============

Run ``py2exe``::

    C:\Python27\python setup.py py2exe

This will create a directory with python extensions, a library.zip and a ``YaybuShell.exe``. This binary is equivalent to the ``yaybu`` command on a unix system.
