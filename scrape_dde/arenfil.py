import os
def rename_files(pwdir,prefix,x):
    file_list = os.listdir(pwdir)
    print(file_list)
    
    for fileName in file_list:
        if fileName[:x] != prefix:
            os.rename(fileName, prefix+fileName)
            
