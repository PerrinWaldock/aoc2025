import os
import shutil

def main():
    rootdir = os.path.dirname(__file__)
    dirs = os.listdir(rootdir)
    thisday = max([int(d) for d in dirs if os.path.isdir(os.path.join(rootdir, d)) and d[0] != "."])+1
    nextDir = os.path.join(rootdir, f"{thisday:02d}")
    os.mkdir(nextDir)
    with open(os.path.join(nextDir, "input.txt"), "w") as f:
        f.write("")
    with open(os.path.join(nextDir, "sample.txt"), "w") as f:
        f.write("")
    shutil.copy(os.path.join(rootdir, "d0p0.py"), os.path.join(nextDir, f"d{thisday}p1.py"))

if __name__ == "__main__":
    main()