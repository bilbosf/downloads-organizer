import os

path_downloads = "C:\\Users\\Gabriel Fernandes\\Downloads"

arquivos = [f for f in os.listdir(path_downloads) if os.path.isfile(os.path.join(path_downloads, f))]

files = {}
count = {}

for f in arquivos:
    extension = f[f.find("."):]
    try:
        count[extension] += 1
        files[extension].append(f)
    except:
        count[extension] = 1
        files[extension] = [f]


path_organized = "C:\\Users\\Gabriel Fernandes\\Documents\\Organized downloads"

try:
    os.mkdir(path_organized)
except:
    pass

try:
    os.mkdir("C:\\Users\\Gabriel Fernandes\\Documents\\Organized downloads\\Avulsos")
except:
    pass

for extension in files.keys():
    if count[extension] == 1:
        os.rename(os.path.join(path_downloads, files[extension][0]), os.path.join(path_organized, "Avulsos", files[extension][0]))
    else:
        pasta = os.path.join(path_organized, extension[1:])
        try:
            os.mkdir(pasta)
        except:
            pass

        for f in files[extension]:
            os.rename(os.path.join(path_downloads, f), os.path.join(pasta, f))

