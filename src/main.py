import sys
import os
import shutil


def main() -> None:
    abs_path = os.getcwd()

    if os.path.exists(f"{abs_path}/public"):
        shutil.rmtree(f"{abs_path}/public")

    sourcedir = os.path.join(abs_path, "static")
    if not os.path.exists(sourcedir):
        raise NotADirectoryError("static directory does not exist in src")
    destination = os.path.join(abs_path, "public")
    listdirs = os.listdir(sourcedir)
    copy_contents(sourcedir, destination)


def copy_contents(source: str, destination: str) -> None:
    listdirs = os.listdir(
        source
    )  # list all items in the source directory for processing

    for item in listdirs:
        # join paths for static and public folders
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)

        if os.path.isfile(source_path):
            # copy static file to public directory
            shutil.copyfile(source_path, destination_path)
        else:
            if not os.path.exists(destination_path):
                # create directory
                os.makedirs(destination_path)
            # recursively copy nested directories and their contents
            copy_contents(source_path, destination_path)


if __name__ == "__main__":
    main()
