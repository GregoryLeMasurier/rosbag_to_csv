import sys
import os
import glob

if len(sys.argv) != 2:
    print("ERROR EXPECT /path/to/checker/root/dir")
    exit(0)

for file in glob.glob(sys.argv[1] + "/*/*/*"):
    base_name = os.path.basename(file)
    dir_name = os.path.dirname(file)
    base_dir_name = os.path.basename(dir_name)

    base_name = base_name.replace(base_dir_name + "-checker-", '')

    checker_path = os.path.join(dir_name, "checkers")
    if not os.path.exists(checker_path):
        os.makedirs(checker_path)

    if "-result" in base_name:
        base_name = base_name.replace("-result", '')
        if "head3DCamera" in base_name:
            os.rename(file, os.path.join(checker_path, "head3DCamera_updated.csv"))
        else:
            os.rename(file, os.path.join(checker_path, base_name))

    else:
        os.rename(file, os.path.join(dir_name,base_name))
