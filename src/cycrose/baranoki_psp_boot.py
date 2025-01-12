"""
    for rebuilding boot size index in BaranoKiniBaranoSaku
    v0.1, developed by devseed
"""
import os
import sys

def rebuild_filesize_table(data_boot, orgafsdir, rebuildafsdir):
    orgafs = []
    rebuildafs = []
    for file in os.listdir(orgafsdir): 
        size = os.path.getsize(os.path.join(orgafsdir, file))
        orgafs.append([file, size])
    for file in os.listdir(rebuildafsdir): 
        size = os.path.getsize(os.path.join(rebuildafsdir, file))
        rebuildafs.append([file, size])
    if len(orgafs) != len(rebuildafs):
        print("error, orgafs and rebuildafs files different length!", len(orgafs), len(rebuildafs))
        return None
    for org, rebuild in zip(orgafs, rebuildafs):
        if org[0] != rebuild[0]:
            print("error, orgafs and rebuildafs files different item!", org[0] , rebuild[0])
            return None
        if org[1] !=  rebuild[1]:
            idx = data_boot.find(int.to_bytes(org[1], 4, 'little'))
            data_boot[idx:idx+4] =  int.to_bytes(rebuild[1], 4, 'little')
            print(org, " -> ", rebuild) 
    return data_boot

def debug():
    pass

def main():
    basedir = r"./build/intermediate"
    if len(sys.argv) > 1: basedir = sys.argv[1]
    orgbootpath = os.path.join(basedir, r"./origin/BOOT.BIN")
    rebuildbootpath = os.path.join(basedir, r"./../repatch/SYSDIR/BOOT.BIN")
    orgafsdir =  os.path.join(basedir, r"./afs01")
    rebuildafsdir = os.path.join(basedir,  r"./afs01_rebuild")

    with open(orgbootpath, 'rb') as fp:
        data_boot = bytearray(fp.read())
    data_boot = rebuild_filesize_table(data_boot, orgafsdir, rebuildafsdir)
    with open(rebuildbootpath, 'wb') as fp:
        fp.write(data_boot)
    pass

if __name__ == "__main__":
    main()
    #debug()
    pass