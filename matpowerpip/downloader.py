import inspect
import os
import shutil
import urllib.request


def download_matpower(
        matpower_version='7.1',
        destination=None,
        force=False,
        rename=True):
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

    matpower_url = (f"https://github.com/MATPOWER/matpower/archive/refs/tags/"
                    f"{matpower_version}.zip")

    print("Downloading MATPOWER...")
    print(matpower_url)
    urllib.request.urlretrieve(matpower_url, file_name)  # source, dest

    shutil.unpack_archive(file_name, destination, 'zip')

    os.remove(file_name)  # remove zipfile

    default_matpower_dir = os.path.join(destination, 'matpower-' + matpower_version)
    if rename:
        renamed_name = os.path.join(destination, 'matpower')
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


def copy_init(destination=None, matpower_version='7.1'):
    matpowerpip_dir = os.path.dirname(
        os.path.abspath(inspect.getfile(download_matpower))
    )
    source = os.path.join(matpowerpip_dir, "__init__.py")

    if destination is None:
        root_dir = os.path.dirname(matpowerpip_dir)
        destination = os.path.join(root_dir, 'matpower-' + matpower_version)

    destination_ = os.path.join(destination, '__init__.py')
    if not os.path.exists(destination_):
        shutil.copy2(source, destination_)


if __name__ == "__main__":
    destination = download_matpower()
    copy_init(destination=destination)
