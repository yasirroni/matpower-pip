# Contributing to matpower-pip

## Notebook example

1. Use `nb-clean` to clean the notebook.

    ```shell
    pip install nb-clean
    nb-clean add-filter -M --preserve-outputs
    ```

1. Make sure to make the example compatible with `google-colab==1.0.0`. You can use below commands (optional).

    ```ipython
    # install octave
    !sudo apt-get -qq update
    !sudo apt-get -qq install octave octave-signal liboctave-dev

    # # install oct2py that compatible with colab
    # google-colab 1.0.0 requires ipykernel~=5.3.4.
    # google-colab 1.0.0 requires ipython~=7.9.0.
    # google-colab 1.0.0 requires tornado~=6.0.4.
    !pip install --quiet ipykernel==5.3.4 ipython==7.9.0 tornado==6.0.4 oct2py

    # install packages
    !pip install matpower matpowercaseframes --quiet
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
