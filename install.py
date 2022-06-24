# This script is called on `rez build`
import os
import shutil
print("Running install.py...")
root = os.path.dirname(__file__)
build_dir = os.environ["REZ_BUILD_PATH"]
install_dir = os.environ["REZ_BUILD_INSTALL_PATH"]
print("Copying payload to %s.." % build_dir)
for folder in ("bin", "python"):
    dst = os.path.join(build_dir, folder)
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(os.path.join(root, folder), dst)
if int(os.getenv("REZ_BUILD_INSTALL")):
    # This part is called with `rez build --install`
    print("Installing payload to %s..." % install_dir)
    for folder in ("bin", "python"):
        dst = os.path.join(install_dir, folder)
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(build_dir, folder), dst)