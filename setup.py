import os
from setuptools import setup
import py2exe
import py2exe.build_exe
import pkg_resources
import ctypes.util


class BuildExe(py2exe.build_exe.py2exe):

    def create_binaries(self, py_files, extensions, dlls):
        py2exe.build_exe.py2exe.create_binaries(self, py_files, extensions, dlls)

        print "*** generate fake egg metadata ***"

        eggs = pkg_resources.require("Yaybu")
        for egg in eggs:
            print '%s == %s' % (egg.project_name, egg.version)
            path = os.path.join(self.exe_dir, '%s.egg-info' % egg.project_name)
            with open(path, "w") as fp:
                fp.write("Metadata-Version: 1.0\n")
                fp.write("Name: %s\n" % egg.project_name)
                fp.write("Version: %s\n" % egg.version)

        print "*** bundling cacert.pem ***"
        self.copy_file(
            os.path.join(os.getcwd(), "cacert.pem"),
            os.path.join(self.exe_dir, "cacert.pem"),
            )

        print "*** bundling python dll ***"
        self.copy_file(
            ctypes.util.find_library('python27.dll'),
            os.path.join(self.exe_dir, 'python27.dll'),
            )


setup(
    console=['YaybuShell.py'],
    cmdclass = {
            'py2exe': BuildExe,
    },
    options = {
        "py2exe": {
            "includes": [
                'pkg_resources',
                #'email.image',
                ],
            },
        },
    )
