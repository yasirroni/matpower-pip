import os
import inspect
import shutil
import urllib.request

def download(matpower_version='7.1', destination=None, force=False, rename=True):
    if destination is None:
        matpower_dir = os.path.dirname(os.path.abspath(inspect.getfile(download)))
    else:
        matpower_dir = destination

    file_name = os.path.join(matpower_dir, "matpower.zip")
    
    if os.path.exists(file_name):
        print("matpower.zip already exist in destionation.")
        if force is True:
            print("Force is True, delete old zip file.")
            shutil.rmtree(file_name)
        else:
            print("Force is False, cancel download. Set force=True to force download.")
            return
    
    matpower_url = "https://github.com/MATPOWER/matpower/archive/refs/tags/" + matpower_version + ".zip"

    print("Downloading MATPOWER...")
    print(matpower_url)
    urllib.request.urlretrieve(matpower_url, file_name) # source, dest

    shutil.unpack_archive(file_name, matpower_dir, 'zip')
    
    os.remove(file_name) # remove zipfile
    
    default_matpower_dir = os.path.join(matpower_dir,'matpower-' + matpower_version)
    if rename:
        renamed_name = os.path.join(matpower_dir,'matpower')
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

def create_init(dir_path=None, matpower_version='7.1'):
    if dir_path is None:
        matpower_dir = os.path.dirname(os.path.abspath(inspect.getfile(download)))
        dir_path = os.path.join(matpower_dir,'matpower-' + matpower_version)
    
    init_path = os.path.join(dir_path, '__init__.py')
    if not os.path.exists(init_path):
        with open(init_path, 'w') as fp:
            pass

if __name__ == "__main__":
    matpower_dir = download()
    create_init(dir_path=matpower_dir)
