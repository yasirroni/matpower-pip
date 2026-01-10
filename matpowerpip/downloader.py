import inspect
import os
import shutil
import urllib.request


def download_matpower(
    matpower_version="8.1", destination=None, force=False, rename=True, backup=None
):
    """
    Download MATPOWER from GitHub.

    Args:
        matpower_version: Version tag (e.g., "8.1") or "master" for development version
        destination: Download destination path
        force: Force overwrite existing files
        rename: Rename extracted folder to "matpower"
        backup: Backup directory path
    """
    if destination is None:
        matpowerpip_dir = os.path.dirname(
            os.path.abspath(inspect.getfile(download_matpower))
        )
        destination = os.path.dirname(matpowerpip_dir)

    file_name = os.path.join(destination, "matpower.zip")

    if os.path.exists(file_name):
        print("matpower.zip already exist in destination.")
        if force is True:
            print("Force is True, delete old zip file.")
            shutil.rmtree(file_name)
        else:
            print("Force is False, cancel download. Set force=True to force download.")
            return

    # Check if development version is requested
    if matpower_version.lower() == "master":
        matpower_url = (
            "https://github.com/MATPOWER/matpower/archive/refs/heads/master.zip"
        )
        folder_name = "matpower-master"
    else:
        matpower_url = f"https://github.com/MATPOWER/matpower/archive/refs/tags/{matpower_version}.zip"
        folder_name = f"matpower-{matpower_version}"

    print("Downloading MATPOWER...")
    print(matpower_url)

    # TODO: use tempfile
    zip_file = urllib.request.urlopen(matpower_url).read()
    with open(file_name, "wb") as f:
        f.write(zip_file)

    shutil.unpack_archive(file_name, destination, "zip")
    os.remove(file_name)  # remove zipfile

    default_matpower_dir = os.path.join(destination, folder_name)

    if backup is not None:
        backup_dest = os.path.join(backup, folder_name)
        shutil.copytree(default_matpower_dir, backup_dest)
        print(f"Backed up to: {os.path.abspath(backup_dest)}")

    if rename:
        renamed_name = os.path.join(destination, "matpower")
        if os.path.exists(renamed_name):
            print("Matpower folder already exist in path")
            if force is True:
                print("Force is True, delete old folder.")
                shutil.rmtree(renamed_name)
            else:
                print("Force is False, cancel rename. Set force=True to force rename.")
                return

        os.rename(default_matpower_dir, renamed_name)
        print(f"matpower saved on {renamed_name}")
        return renamed_name
    else:
        print(f"matpower saved on {default_matpower_dir}")
        return default_matpower_dir


def copy_init(destination=None):
    matpowerpip_dir = os.path.dirname(
        os.path.abspath(inspect.getfile(download_matpower))
    )
    source = os.path.join(matpowerpip_dir, "__init__.py")

    if destination is None:
        root_dir = os.path.dirname(matpowerpip_dir)
        destination = os.path.join(root_dir, "matpower")

    destination_ = os.path.join(destination, "__init__.py")
    if not os.path.exists(destination_):
        shutil.copy2(source, destination_)


if __name__ == "__main__":
    destination = download_matpower(force=True, backup="backups")
    copy_init()
