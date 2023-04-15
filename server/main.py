"""object-processor"""

import glob
import shutil
import os
import zipfile
import subprocess

source_path='../source/*'
destination_path='../destination'

postfix=[1,2,3]
while True:
    source_object=glob.glob(source_path)
    if len(source_object)>0:
        object_path=source_object[0]
        object_name=os.path.basename(object_path).split('.')
        prefix=object_name[0]
        postfix2=object_name[1]
        shutil.copy(object_path,'.')
        # print(postfix2)
        if postfix2=='py':
            py_path_name=os.path.basename(object_path)
            print(py_path_name)
            result=subprocess.run(["python", py_path_name], capture_output=True, text=True)
            print(result.stdout)
            print(result.stderr)
            os.remove(object_path)
        elif postfix2=='txt':
            # shutil.copy(object_path,'.')
            for item in range(len(postfix)):
                main_item=item+1
                num_of_lines=main_item*10
                file_name=prefix+'_'+str(main_item)+'.'+postfix2
                with open(file_name,'w') as file:
                    file.write(f"{file_name} will have {num_of_lines} lines\n")
                with open(object_path,'r') as file:
                    lines = file.readlines()
                    with open(file_name,'a') as file:
                        for i,val in enumerate(lines):
                            if i==num_of_lines:
                                break
                            file.write(val)
            # zip file
            zip_file_name = prefix + '.zip'
            with zipfile.ZipFile(zip_file_name, 'w') as zip_file:
                for converted_file in glob.glob(prefix + '_*.{}'.format(postfix2)):
                    zip_file.write(converted_file)

            # Move the zip file to the destination directory
            shutil.move(zip_file_name, destination_path)

            # Unzip the file in the destination directory
            with zipfile.ZipFile(os.path.join(destination_path, zip_file_name), 'r') as zip_file:
                zip_file.extractall(destination_path)


            os.remove(object_path)
            os.remove(os.path.basename(object_path))
            current_folder_path = os.path.abspath(os.getcwd())
            files = os.listdir(current_folder_path)
            for file in files:
                if 'txt' in file:
                    os.remove(file)
        break

