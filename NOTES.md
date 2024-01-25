## setup

> **NOTE** These are my personal note!!!

## Init

### setup conda env

1. base env
   ```bash
   conda create -n syntax-highlighting-ng --file tests/environment.yaml
   ```

2. remove old pakage and install using pip newer:
   ```bash
   conda uninstall --force rpds-py
   pip install rpds-py aab
   ```

### prepare the addon to Anki

Quick cycle install:

1. build
   ```bash
   aab build
   (or)
   aab build -d local current
   ```

2. Install from GUI *from file* 
   
   **build/syntax-highlighting_ng-7b6cdd2-anki21.ankiaddon**

3. replace with current code
   ```bash
   D=~/Library/"Application Support"/Anki2/addons21
   rm -rf "$D"/syntax_highlighting_ng
   ln -s $(pwd)/src/syntax_highlighting_ng \
      "$D"/syntax_highlighting_ng
   ```

Debug:

0. patch pydevd
   ```text
   --- /Users/antonio/shared/pydevd-2.10.0/_pydevd_bundle/pydevd_filtering.py	2023-12-18 15:35:50
   +++ /Users/antonio/shared/pydevd-2.10.0/_pydevd_bundle/pydevd_filtering.py.new	2023-12-18 15:35:22
   @@ -156,8 +156,8 @@

         # Make sure we always get at least the standard library location (based on the `os` and
         # `threading` modules -- it's a bit weird that it may be different on the ci, but it happens).
   -        roots.append(os.path.dirname(os.__file__))
   -        roots.append(os.path.dirname(threading.__file__))
   +        roots.append(os.path.dirname(os.__file__) if hasattr(os, "__file__") else "/Users/antonio/envs/syntax-highlighting-ng/lib/python3.12")
   +        roots.append(os.path.dirname(threading.__file__) if hasattr(threading, "__file__") else "/Users/antonio/envs/syntax-highlighting-ng/lib/python3.12")
            if IS_PYPY:
                # On PyPy 3.6 (7.3.1) it wrongly says that sysconfig.get_path('stdlib') is
                # <install>/lib-pypy when the installed version is <install>/lib_pypy.
   --- /Users/antonio/shared/pydevd-2.10.0/pydevd_file_utils.py	2023-12-18 15:35:49
   +++ /Users/antonio/shared/pydevd-2.10.0/pydevd_file_utils.py.new	2023-12-18 15:35:33
   @@ -88,7 +88,7 @@
                 break

     if library_dir is None or not os_path_exists(library_dir):
   -        library_dir = os.path.dirname(os.__file__)
   +        library_dir = os.path.dirname(os.__file__) if hasattr(os, "__file__") else "/Users/antonio/envs/syntax-highlighting-ng/lib/python3.12"

        return library_dir
   ```

1. use:
   ```python
   import sys; sys.path.insert(0, "/Users/antonio/shared/pydevd-2.10.0")
   import pydevd; pydevd.settrace('localhost', port=12345, stdoutToServer=True, stderrToServer=True)
   ```

2. launch app
   ```bash
   PYDEVD_DISABLE_FILE_VALIDATION=1 open /Applications/Anki.app
   ```


## Release
  1. git tag -m "release" 0.0.3 
  2. aab build release
  3. upload to anki
