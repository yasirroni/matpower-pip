# Contributing to matpower-pip

## Notebook example

1. Use `nb-clean` to clean the notebook.

    ```shell
    pip install nb-clean
    nb-clean add-filter -M --preserve-cell-outputs
    ```

1. Make sure to make the example compatible with `google-colab==1.0.0`. You can use below commands (optional).

    ```ipython
    # install octave
    !sudo apt-get -qq update
    !sudo apt-get -qq install octave octave-signal liboctave-dev

    # # install oct2py that compatible with colab
    import os
    from pkg_resources import get_distribution

    os.system(f"pip install -qq"
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
