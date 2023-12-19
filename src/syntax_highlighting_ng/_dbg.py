## INTERNAL MODULE (DEBUG)
def set_trace():
    import sys

    sys.path.insert(0, "/Users/antonio/shared/pydevd-2.10.0")
    import pydevd

    pydevd.settrace("localhost", port=12345, stdoutToServer=True, stderrToServer=True)
