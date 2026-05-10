import os
import shutil


def copy_dir_contents(src, dst, first_run=True):
    if not os.path.exists(src):
        raise Exception(f"Error: {src} is not a valid path")

    if first_run:
        if os.path.exists(dst):
            print(f"Removing files in {dst}...")
            shutil.rmtree(dst)
            os.makedirs(dst)
            print(f"Files in {dst} removed\n")
        else:
            print(f"Path {dst} does not exist. Continuing to create {dst} and copy items...")
            os.makedirs(dst)

    nested_items = os.listdir(src)
    for item in nested_items:
        item_src = os.path.join(src, item)
        if os.path.isfile(item_src):
            shutil.copy(item_src, dst)
            item_dst = os.path.join(dst, item)
            print(f"Copied (file): {item_src}  ->  {item_dst}")
        elif os.path.isdir(item_src):
            new_dst = os.path.join(dst, item)
            os.makedirs(new_dst)
            print(f"Created (dir): {dst}  ->  {new_dst}")
            copy_dir_contents(item_src, new_dst, False)
        else:
            raise Exception(f"Error: {item_src} is of unknown file type")

    return
