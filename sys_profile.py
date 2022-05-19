import sys
import os
import subprocess
import psutil
import webbrowser
from datetime import datetime

class SystemProfile:

    def __init__(self):
        self._user_path = os.path.expanduser('~')
        self._dest_path = self.getBackupPath()
        if sys.platform == 'win32':
            script_path = sys.argv[0]
            script_dir = os.path.split(script_path)[0]
            restore_file_win = f'{os.path.join(script_dir, "Restore.exe")}'
            app_cache = os.path.join(self._user_path, 'AppData\Local\Google\DriveFS')
            self._name = 'Windows'
            self._gd_app_path = r'C:\Program Files'
            self._gd_process_name = 'GoogleDriveFS.exe',
            self._selected_dirs = ('Desktop', 'Documents', 'Pictures')
            self._gd_drive_path = self.getGDFSDrivePath()
            self._open_gd = lambda: subprocess.Popen(self.winAppPathFinder(r'C:\Program Files', 'GoogleDriveFS.exe'))
            self._restore = restore_file_win
            self._app_cache = app_cache
            self._download_path = os.path.join(self._user_path, 'Downloads', 'GoogleDriveSetup.exe')
            self._download_link = 'https://dl.google.com/drive-file-stream/GoogleDriveSetup.exe'
        elif sys.platform == 'darwin':
            app_cache = os.path.join(self._user_path, 'Library/Application Support/Google/DriveFS')
            self._name = 'macOS'
            self._gd_app_path = '/Applications'
            self._gd_process_name = 'Google Drive'
            self._selected_dirs = ('Desktop', 'Documents', 'Pictures')
            self._gd_drive_path = self. getGDFSDrivePath()
            self._open_gd = lambda: subprocess.Popen(["/usr/bin/open", "/Applications/Google Drive.app"])
            self._restore = '/Applications/Basic Backup.app/Contents/Restore.zip'
            self._app_cache = app_cache
            self._download_path = os.path.join(self._user_path, 'Downloads', 'GoogleDrive.dmg')
            self._download_link = 'https://dl.google.com/drive-file-stream/GoogleDrive.dmg'
        else: print(f'Sorry! unknown OS {sys.platform}')

    def get_name(self):
        return self._name

    def get_google_drive_app_path(self):
        return self._gd_app_path

    def get_google_drive_process_name(self):
        return self._gd_process_name

    def get_user_folders(self):
        return self._selected_dirs

    def get_google_drive_local_path(self):
        return self._gd_drive_path

    def run_google_drive(self):
        return self._open_gd

    def get_restore_file_path(self):
        return self._restore

    def get_google_drive_app_cache_path(self):
        return self._app_cache

    def get_dest_dirs(self):
        dest_dirs = [os.path.join(self._dest_path, str(x)) for x in self._selected_dirs]
        return dest_dirs

    def get_source_dirs(self):
        source_dirs = [os.path.join(self._user_path, str(x)) for x in self._selected_dirs]
        return source_dirs

    def get_user_path(self):
        return self._user_path

    def get_download_path(self):
        return self._download_path

    def getDriveLetter(self):
        cmd = 'wmic logicaldisk get deviceid, volumename  | findstr "Google Drive File Stream"'
        tempstr = os.popen(cmd).read()
        driveletter = tempstr.split()
        return driveletter[0]

    def getGDFSDrivePath(self):
        if sys.platform == 'win32':
            drive_letter = ''
            try:
                drive_letter = self.getDriveLetter()
            except:
                pass
            return os.path.join(f'{drive_letter}', 'My Drive')
        elif sys.platform == 'darwin':
            return os.path.join(os.path.abspath(os.sep), 'Volumes', 'GoogleDrive', 'My Drive')

    def getBackupPath(self):
        backup_path = os.path.join(f'{self.getGDFSDrivePath()}', 'AppLovin_Backup')
        return backup_path

    def winAppPathFinder(self, app_path, app_process_name):
        gd_paths = []
        for dirpath, dirnames, filenames in os.walk(app_path):
            for filename in filenames:
                if app_process_name in filename:
                    gd_paths.append(os.path.join(dirpath, filename))
        return max(gd_paths)

    # checks if GDFS is installed
    def isProgramInstalled(self):
        filexist = False
        if self._name.lower() == 'windows':
            gdfs = []
            for dirpath, dirnames, filenames in os.walk(self._gd_app_path):
                gdfs.extend([f for f in filenames if f == self._gd_process_name])
            if gdfs:
                filexist = True
        elif self._name.lower() == 'macos':
            if f'{self._gd_process_name}.app' in os.listdir(self._gd_app_path):
                filexist = True
        if not filexist:
            webbrowser.open(self._download_link)

    # checks if GDFS is running
    def isProgramRunning(self):
        running = []
        for p in psutil.process_iter():
            try:
                if p.name():
                    running.append(p._name)
            except Exception:
                pass
        if self._gd_process_name not in running:
            self._open_gd()

    # checks if GDFS is configured
    def isSignedInToGDFS(self, app_cache_path, clear_terminal):
        clear_terminal()
        lst = []
        for dirpath, dirnames, filenames in os.walk(app_cache_path):
            lst.extend(filenames)
        if 'enabled' not in lst:
            pass
