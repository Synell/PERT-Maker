#----------------------------------------------------------------------

    # Libraries
import os
import pyautogui
#----------------------------------------------------------------------

    # Class
class get:
    def __new__(cls):
        return None

    class screen:
        def __new__(cls):
            return None

        def size():
            return pyautogui.size()

    class files:
        def __new__(cls):
            return None

        def extensions(dir_ = None, extensions = [], subDir = True, onlyFiles = False):
            if dir_ is None:
                return None

            totalFiles = []
            for x in range(len(extensions)):
                extensions[x] = extensions[x].replace('.', '')

            if subDir:
                for (now, subfolders, files) in os.walk(dir_):
                    for x in files:
                        if x.split('.')[-1] in extensions:
                            if onlyFiles:
                                totalFiles.append(x)
                            else:
                                totalFiles.append(f'{now}\\{x}')
            else:
                if onlyFiles:
                    totalFiles = [file for file in os.listdir(dir_) if os.path.isfile(os.path.join(dir_, file)) if file.split('.')[-1] in extensions ]
                else:
                    totalFiles = [ f'{dir_}{file}' for file in os.listdir(dir_) if os.path.isfile(os.path.join(dir_, file)) if file.split('.')[-1] in extensions ]

            return totalFiles
#----------------------------------------------------------------------
