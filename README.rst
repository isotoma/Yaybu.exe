================
Yaybu on Windows
================

This process has been observed to work on 32-bit Windows XP and Windows 7.

Let's set up a nice ``PATH``::

    set PATH=C:\Git\bin;C:\Python27;C:\MinGW\bin;%PATH%

Install msysgit (the official windows port of Git):

 * URL is https://msysgit.googlecode.com/files/Git-1.8.3-preview20130601.exe
 * Install to C:\Git
 * Default line ending mode (converts to windows on checkout / to unix on commit)
 * Don't bother with any shell integration, but the font is nice.

Install python2.7, py2exe, pycrypto from installers:

 * http://www.python.org/ftp/python/2.7.5/python-2.7.5.msi
 * http://downloads.sourceforge.net/project/py2exe/py2exe/0.6.9/py2exe-0.6.9.win32-py2.7.exe
 * http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win32-py2.7.exe

Install MinGW Installation Manager Setup Tool:

 * http://sourceforge.net/projects/mingw/files/Installer/mingw-get-setup.exe/download

There is no need to let it do GUI stuff. You can then install gcc and tools::

    mingw-get install gcc mingw-utils

At the time of writing this seems to yield a broken environment - so copy some DDL's around. To fix cc1plus::

    cd C:\MinGW
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

Out of the box python2.7 will not be able to use this version of mingw32. Edit ``C:\Python27\Lib\distutils\cygwinccompiler.py`` and remove all mentions of ``-mno-cygwin``.

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

You are now ready to get the code::

    git clone https://github.com/yaybu/Yaybu.exe C:\Yaybu.exe
    cd C:\Yaybu.exe

Install setuptools using the ez_setup.py script provided::

    python ez_setup.py

py2exe will break with setuptools because it is compressed. A better way to deal with it is needed, but for now::

    python -m easy_install --always-unzip --upgrade "setuptools<1.0"

(You can upgrade to the active version because it detects it is already the latest version).

Then install pip and get the requirements::

    python -m easy_install pip
    python -m pip install -r requirements.txt

This doesn't actually install any yay/yaybu code (for which you have a few choices)::

    python -m pip install git+git://github.com/yaybu/yay.git#egg=yay
    python -m pip install git+git://github.com/yaybu/yaybu.git#egg=yaybu

or (if you check out the code by hand or with buildbot)::

    python -m pip install -e src/yay
    python -m pip install -e src/yaybu


Running tests
=============

There are extra deps for the tests::

    python -m pip install nose2 unittest2 mock fakechroot
    python -m nose2 yay yaybu
    

Building an exe
===============

Run ``py2exe``::

    python setup.py py2exe

This will create a directory with python extensions, a library.zip and a ``YaybuShell.exe``. This binary is equivalent to the ``yaybu`` command on a unix system.
