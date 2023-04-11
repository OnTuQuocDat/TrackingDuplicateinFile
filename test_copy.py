import shutil

def test_copy():
    src_debug = 'debug.csv'
    dst_debug = 'setupcopy.csv'
    shutil.copyfile(src_debug,dst_debug)

test_copy()