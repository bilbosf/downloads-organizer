import os, sys
from getpass import getuser


USER_NAME = getuser()
path_downloads = "C:\\Users\\%s\\Downloads" %USER_NAME

if len(sys.argv) == 1:
    path_organized = "C:\\Users\\%s\\Documents\\Organized downloads" %USER_NAME
elif len(sys.argv) == 2:
    path_organized = sys.argv[1]
else:
    print("Use no options to set the organized downloads folder to C:\\Users\\%s\\Documents\\Organized downloads" %USER_NAME)
    print("Use one option to specify the path to the organized downloads directory")
    sys.exit()



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
            os.rename(os.path.join(path_downloads, f), os.path.join(path_current_extension, f))

