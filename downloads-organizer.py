import os, sys, time
from getpass import getuser
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

USER_NAME = getuser()
path_downloads = "C:\\Users\\%s\\Downloads" %USER_NAME
leave_recent_files_alone = True #Set to true to ignore files downloaded today
add_startup = True #Set to true to add program to startup folder, so that it will organize the files every time the computer is booted
setup_watchdog = False #Set to true to setup watchdog to automatically organize files as soon as they're downloaded (use only with leave_recent_files_alone = False)

if len(sys.argv) == 1:
    path_organized = "C:\\Users\\%s\\Documents\\Organized downloads" %USER_NAME
elif len(sys.argv) == 2:
    path_organized = sys.argv[1]
else:
    print("Use no options to set the organized downloads folder to C:\\Users\\%s\\Documents\\Organized downloads" %USER_NAME)
    print("Use one option to specify the path to the organized downloads directory")
    sys.exit()

def on_created(event):
    f = os.path.basename(event.src_path)
    extension = f[f.rfind("."):]
    path_current_extension = os.path.join(path_organized, extension[1:])
    if os.path.exists(path_current_extension):
        os.rename(os.path.join(path_downloads, f), os.path.join(path_current_extension, f))
    else:
        os.rename(os.path.join(path_downloads, f), os.path.join(path_organized, "Avulsos", f))

def add_to_startup(file_path=""):
    if file_path == "":
        file_path = os.path.realpath(__file__)
    bat_path = r'C:\\Users\\%s\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\downloads-organizer.bat' %USER_NAME
    with open(bat_path, "w+") as bat_file:
        bat_file.write(r'start "" "%s"' %file_path)
    print("Added to startup")

def remove_from_startup(file_path=""):
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
    bat_path = r'C:\\Users\\%s\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\downloads-organizer.bat' %USER_NAME
    if(os.path.exists(bat_path)):
        os.remove(bat_path)
    print("Removed from startup")

if setup_watchdog:
    patterns = "*"
    ignore_patterns = ""
    ignore_directories = True
    case_sensitive = False
    event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    event_handler.on_created = on_created

    observer = Observer()
    observer.schedule(event_handler, path_downloads, recursive=False)

    observer.start()

if add_startup:
    add_to_startup()
else:
    remove_from_startup()

print("Organizing downloads")
print("leave_recent_files_alone:", leave_recent_files_alone)
print("add_startup:", add_startup)
print("setup_watchdog:" setup_watchdog)

files = [f for f in os.listdir(path_downloads) if os.path.isfile(os.path.join(path_downloads, f))]

files_dict = {}
count = {}

for f in files:
    extension = f[f.rfind("."):]
    try:
        count[extension] += 1
        files_dict[extension].append(f)
    except KeyError:
        count[extension] = 1
        files_dict[extension] = [f]

try:
    os.mkdir(path_organized)
except FileExistsError:
    pass

try:
    os.mkdir(os.path.join(path_organized, "Avulsos"))
except FileExistsError:
    pass

for extension in files_dict.keys():
    if count[extension] == 1:
        os.rename(os.path.join(path_downloads, files_dict[extension][0]), os.path.join(path_organized, "Avulsos", files_dict[extension][0]))

    else:
        path_current_extension = os.path.join(path_organized, extension[1:])

        try:
            os.mkdir(path_current_extension)
        except FileExistsError:
            pass

        for f in files_dict[extension]:
            if (not leave_recent_files_alone) or time.time() - os.path.getctime(os.path.join(path_downloads, f)) > 24*3600:
                os.rename(os.path.join(path_downloads, f), os.path.join(path_current_extension, f))

if setup_watchdog:
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
else:
    os.system("pause")