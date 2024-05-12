import os, ctrl, shutil, logging


logging.basicConfig(level=logging.INFO)

cwd = os.getcwd().removesuffix("/")


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
        os.system(f"rm -rf {cwd}/packdir")
        os.makedirs(cwd + "/packdir")
    
    def create_fs(self):
        file: list[str]

        for file in self.ctrl.files:
            src = file[0]
            dst = cwd + "/packdir/" + file[1].removeprefix("/")
            logging.info("Copying " + src + " to " + dst)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy(src, dst, follow_symlinks=True)

        os.makedirs(cwd + "/packdir/DEBIAN", exist_ok=True)
    
    def create_control(self):
        self.ctrl.generate()
    
    def sign(self):
        print(f"$ md5deep -r {cwd}/packdir > " +
                  f"{cwd}/packdir/DEBIAN/md5sums")
        os.system(f"md5deep -r {cwd}/packdir > " +
                  f"{cwd}/packdir/DEBIAN/md5sums")

    def create_package(self, move=True):
        print(f"$ fakeroot dpkg-deb --build {cwd}/packdir")
        os.system(f"fakeroot dpkg-deb --build {cwd}/packdir")
        if move:
            print("move", cwd + "/packdir.deb",
                        cwd + "/" + self.ctrl.name + "_" +
                        self.ctrl.version + "_" + self.ctrl.arch + ".deb")
            shutil.move(cwd + "/packdir.deb",
                        cwd + "/" + self.ctrl.name + "_" +
                        self.ctrl.version + "_" + self.ctrl.arch + ".deb")
