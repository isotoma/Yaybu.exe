import os
from setuptools import setup
import py2exe
import py2exe.build_exe
import pkg_resources

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


setup(
    console=['YaybuShell.py'],
    cmdclass = {
            'py2exe': BuildExe,
    },
    options = {
        "py2exe": {
            "bundle_files": 1,
            "includes": [
                'pkg_resources',
                #'email.image',
                ],
            },
        },
    )
