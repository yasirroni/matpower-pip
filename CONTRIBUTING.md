# Contributing to matpower-pip

## Environment

To install Python 3.12 environment, use:

```shell
python3.12 -m venv env
```

To activate Python environment, use:

   Linux and macOS:

   ```bash
   source env/bin/activate
   ```

   Windows - PowerShell

   ```bash
   env\Scripts\Activate.ps1
   ```

   Windows - Command Prompt

   ```bash
   env\Scripts\activate
   ```

To deactivate the Python environment, use:

```shell
deactivate
```

## Install requirements

```shell
pip install -r requirements.txt
```

## Notebook example

1. Use `nb-clean` to clean the notebook.

    ```shell
    pip install nb-clean
    nb-clean add-filter
    ```

    for single run:

    ```shell
    nb-clean clean PATH
    ```

1. Make sure to make the example compatible with `google-colab==1.0.0`. You can use below commands (optional).

    ```ipython
    # install octave
    !sudo apt-add-repository -y ppa:ubuntuhandbook1/octave > /dev/null 2>&1
    !sudo apt -qq update > /dev/null 2>&1
    !sudo apt -y -qq install liboctave-dev octave > /dev/null 2>&1

    # install oct2py that compatible with colab
    import os

    from pkg_resources import get_distribution

    os.system(
        f"pip install -qq"
        f" ipykernel=={get_distribution('ipykernel').version}"
        f" ipython=={get_distribution('ipython').version}"
        f" tornado=={get_distribution('tornado').version}"
        f" oct2py"
    )

    # install packages
    !pip install -qq matpower matpowercaseframes
    ```

    > *NOTE*
    >
    > If using `octave`, make sure to delete the output of the installation cell.

1. Print `matpower` version. If used, also print the version of `oct2py`.

    ```python
    import oct2py
    import matpower

    print(f"oct2py version: {oct2py.__version__}")
    print(f"matpower version: {matpower.__version__}")
    ```

## Print README.md

Use pandoc and wkhtmltopdf to create README.pdf

```shell
pandoc --pdf-engine=wkhtmltopdf README.md -o README.pdf
```
