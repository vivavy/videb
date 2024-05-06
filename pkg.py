import os, ctrl, shutil, logging


logging.basicConfig(level=logging.INFO)

basedir = os.path.dirname(os.path.realpath(__file__))


class Pkg:
    def __init__(self, config, ctrl: ctrl.Ctrl):
        self.config = config
        self.ctrl = ctrl
        self.ctrl.set_pkg(self)
        self.size = 0
        self.create_packdir()

    def set_size(self, size):
        self.size = size

    def create_packdir(self):
        os.system(f"rm -rf {basedir}/packdir")
        os.makedirs(basedir + "/packdir")
    
    def create_fs(self):
        # read every file from control and copy it to packdir
        file: list[str]
        for file in self.ctrl.files:
            src = file[0]
            dst = os.path.join(basedir, "packdir", file[1].removeprefix("/"))
            logging.info("Copying " + src + " to " + dst)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy(src, dst, follow_symlinks=True)

        os.makedirs(basedir + "/packdir/DEBIAN", exist_ok=True)
    
    def create_control(self):
        self.ctrl.generate()
    
    def sign(self):
        os.system(f"md5deep -r {basedir}/packdir > {basedir}/packdir/DEBIAN/md5sums")

    def create_package(self, move=True):
        os.system(f"fakeroot dpkg-deb --build {basedir}/packdir")
        if move:
            shutil.move(basedir + "/packdir.deb", self.ctrl.name + "_" + self.ctrl.version + "_" + self.ctrl.arch + ".deb")
