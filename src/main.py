import shutil
import os
import sys
from functions import generate_pages_recursive


def copy_static(src, dest):
    os.mkdir(dest)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        else:
            copy_static(src_path, dest_path)

    

def main():
    basepath = sys.argv[0] or "/"

    #clean public folder
    src = "static"
    dest = 'public'

    if os.path.exists(dest):
        shutil.rmtree(dest)

    copy_static(src, dest)

    generate_pages_recursive("content/", "template.html", "docs/", basepath)

if __name__ == "__main__":
    main()