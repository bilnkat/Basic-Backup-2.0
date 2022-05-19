from dirsync import sync
from sys_profile import SystemProfile

my_sys_profile = SystemProfile()

my_sys_profile.isProgramRunning()

sourcedirs = my_sys_profile.get_source_dirs()
destdirs = my_sys_profile.get_dest_dirs()
action = 'sync'

zipped_dirs = list(zip(sourcedirs, destdirs))
for each_dir in zipped_dirs:
    sync(each_dir[0], each_dir[1], action, twoway=False, ctime=False, verbose=True, purge=False, create=True, force=False)
