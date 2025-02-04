############################################################################################################
# Author: LHYe200
# Date: 2025-02-04
# Version: 1.1
# Usage: python AddFile.py
# 注意: 请将本文件放在uvproj文件同一目录下运行
# Note: Please run this file in the same directory as the uvproj file
# 描述: 添加文件，自动修改uvproj文件，添加文件到指定组
# Description: Add files, automatically modify the uvproj file, and add files to the specified group
# 警告: 请注意备份uvproj文件及相关项目文件，以免出现意外，使用风险自负
# Warning: Please backup the uvproj file and related project files to avoid accidents, USE AT YOUR OWN RISK
############################################################################################################

import os
import re
import xml.dom.minidom

# 使用前请根据情况修改
source_file_path = "./"
header_file_path = "./Header"
source_group_name = "Source"
header_group_name = "Header"
auto_include_in_source = '#include "Header/AI8H.H"'
change_to_create_hex_file = True


def AddFileToAGroup(file_name, path_name, group_name,DOMTree):
    collection = DOMTree.documentElement
    groups = collection.getElementsByTagName("Group")
    group = None
    for group_t in groups:
        # ad = group_t.getElementsByTagName("GroupName")
        if group_t.getElementsByTagName("GroupName")[0].childNodes[0].data == group_name:
            group = group_t
            break
    else:
        group_t = DOMTree.createElement("Group")
        group_t.appendChild(DOMTree.createElement("GroupName"))
        group_t.getElementsByTagName("GroupName")[0].appendChild(DOMTree.createTextNode(group_name))
        group_t.appendChild(DOMTree.createElement("Files"))
        collection.getElementsByTagName("Groups")[0].appendChild(group_t)
        group = group_t
    
    ruled_path = ".\\"+os.path.normpath(os.path.join(path_name, file_name))
    for file_path_C in group.getElementsByTagName("FilePath"):
        if file_path_C.childNodes[0].data == ruled_path:
            input("The file has already existed!")
            exit(-1)
    files = group.getElementsByTagName("Files")[0]
    file = DOMTree.createElement("File")
    file.appendChild(DOMTree.createElement("FileName"))
    file.getElementsByTagName("FileName")[0].appendChild(DOMTree.createTextNode(file_name))
    file.appendChild(DOMTree.createElement("FileType"))
    if file_name.endswith(".c"):
        file.getElementsByTagName("FileType")[0].appendChild(DOMTree.createTextNode("1"))
    elif file_name.endswith(".h"):
        file.getElementsByTagName("FileType")[0].appendChild(DOMTree.createTextNode("5"))
    file.appendChild(DOMTree.createElement("FilePath"))
    file.getElementsByTagName("FilePath")[0].appendChild(DOMTree.createTextNode(ruled_path))
    files.appendChild(file)
    print("Add file to group success!")

def createHeaderFile(header_file_name):
    if not os.path.exists(header_file_path):
        os.makedirs(header_file_path)
    if not os.path.exists(os.path.join(header_file_path , header_file_name)):
        with open(os.path.join(header_file_path , header_file_name), "w") as f:
            f.write("#ifndef __" + header_file_name[:-2].upper() + "_H__\n")
            f.write("#define __" + header_file_name[:-2].upper() + "_H__\n\n\n")
            f.write("#endif\n")
    print("Create header file success!")

def createSourceFile(file_name,has_header):
    if not os.path.exists(source_file_path):
        os.makedirs(source_file_path)
    if not os.path.exists(os.path.join(source_file_path , file_name)):
        with open(os.path.join(source_file_path , file_name), "w") as f:
            f.write(auto_include_in_source + "\n")
            if has_header:
                f.write("#include \"./"+str(os.path.normpath(os.path.relpath(os.path.join(header_file_path, file_name)[:-2] + ".h",os.path.join(source_file_path, file_name)).replace("..",".",1))).replace("\\","/")+ "\"\n")
    print("Create source file success!")



if __name__ == "__main__":
    file_name = input("Please input the file name: ").strip()
    header_file_name = ""
    if file_name.lower().endswith(".c"):
        if_create_header = input("Do you want to create a header file for this file?([y]/n): ").strip()
        if not if_create_header.lower() == "n":
            header_file_name = file_name[:-1] + "h"

    elif file_name.lower().endswith(".h"):
        header_file_name = file_name
        file_name = ""

    else:
        input("The file type is not support!")
        exit(-1)

    uvproj_files = []
    
    for file in os.listdir(os.path.abspath(os.path.dirname(__file__))):
        file = file.lower()
        if file.endswith(".uvproj") or file.endswith(".uvprojx"):
            uvproj_files.append(file)
    if len(uvproj_files) == 0:
        input("No UV project file found!")
        # input("Press any key to exit...")
        exit(-1)
    elif len(uvproj_files) > 1:
        input("More than one UV project file found!")
        exit(-1)
    uvproj_file = uvproj_files[0]
    xml_str = ""
    with open(uvproj_file, "r", encoding="utf-8") as f:
        xml_str = f.readlines()
        xml_str = [x for x in xml_str if x.strip()]
        xml_str = "".join(xml_str)
        xml_str = xml_str.replace("\n", "")
        xml_str = xml_str.replace("\t", "")
        
    DOMTree = xml.dom.minidom.parseString(xml_str)

    collection = DOMTree.documentElement

    if change_to_create_hex_file:
        collection.getElementsByTagName("CreateHexFile")[0].childNodes[0].data = "1"

    if file_name != "":
        createSourceFile(file_name,header_file_name != "")
        AddFileToAGroup(file_name, source_file_path, source_group_name,DOMTree)

    if header_file_name != "":
        createHeaderFile(header_file_name)
        AddFileToAGroup(header_file_name, header_file_path, header_group_name,DOMTree)
    
    xml_str = DOMTree.toprettyxml().replace("\t","  ")
    xml_str = re.sub(r'<(\w+)([^>]*)/>', r'<\1\2></\1>', xml_str)
    with open(uvproj_file, "w", encoding="utf-8") as f:
        # DOMTree.writexml(f, addindent="  ", newl="\n", )
        f.write(xml_str)
        print("Modify uvproj file success!")
    input("Add file success! Press any key to exit...")
