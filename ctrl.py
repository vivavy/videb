import os, sys, shutil, logging


logging.basicConfig(level=logging.INFO)

basedir = os.path.dirname(os.path.realpath(__file__))


# made to prevent cyclic imports
class pkg:
    size: int = 0


class Ctrl:
    package: pkg = pkg()

    def __init__(self, config):
        self.config = config
        self.name = config["package"]
        self.version = config["version"]
        self.provides = config["provides"]
        self.mainer = config["mainer"]
        self.arch = config["arch"]
        self.category = config["category"]
        self.desc = config["desc"]
        self.deps = config["deps"]
        self.predeps = config["predeps"]
        self.priority = config["priority"]
        self.origin = config["origin"]
        self.files = config["files"]
    
    def set_pkg(self, pkg):
        self.package = pkg
    
    def generate(self):
        # generate control file
        data = ""
        data += "Package: " + self.name + "\n"
        data += "Version: " + self.version + "\n"
        data += "Provides: " + self.provides + "\n"
        data += "Maintainer: " + self.mainer + "\n"
        data += "Architecture: " + self.arch + "\n"
        data += "Section: " + " ".join(self.category) + "\n"
        data += "Priority: " + self.priority + "\n"
        data += "Description: " + self.desc + "\n"
        data += "Depends: " + ", ".join(self.deps) + "\n"
        data += "Pre-Depends: " + ", ".join(self.predeps) + "\n"
        data += "Origin: " + self.origin + "\n"
        data += "Installed-Size: " + str(self.package.size) + "\n"
        
        with open(basedir + "/packdir/DEBIAN/control", "wt") as f:
            f.write(data)
        
        # copy postinst and preinst
        if self.config["postinst"] is not None:
            shutil.copy(self.config["postinst"], basedir + "packdir/DEBIAN/postinst")
        if self.config["preinst"] is not None:
            shutil.copy(self.config["preinst"], basedir + "packdir/DEBIAN/preinst")
        
        # copy postrm and prerm
        if self.config["postrm"] is not None:
            shutil.copy(self.config["postrm"], basedir + "packdir/DEBIAN/postrm")
        if self.config["prerm"] is not None:
            shutil.copy(self.config["prerm"], basedir + "packdir/DEBIAN/prerm")
        
        # copy changelog
        if self.config["changelog"] is not None:
            shutil.copy(self.config["changelog"], basedir + "/packdir/DEBIAN/changelog")

        # generate dirs file

        data = ""
        for dir in self.config["dirs"]:
            data += dir + "\n"

        with open(basedir + "/packdir/DEBIAN/dirs", "wt") as f:
            f.write(data)
