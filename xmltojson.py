# Program to convert an xml
# file to json file
import json
import xmltodict
import os
import re
import pandas as pd
import base64
import sys


PATH_FOLDER_EXTRACT = ".\\csv_data"

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def extract_version_nasform(xml):
    nasform_regex = "(?sa)<nasform_version_\d\d\s?>(.|[^<\>]*)<\/nasform_version_\d\d\s?>"
    versions = re.findall(nasform_regex, xml)
    return versions[0]

def extract_files(path, extension):
    # the path should be absoluth
    try:
        xml_Files = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(path):
            for file in f:
                if file.endswith(extension):
                    full_path = os.path.join(r, file)
                    xml_Files.append(full_path)

        return xml_Files
    except:
        print("Somethings went wrong while extracting file")


def xml_files_to_json(xml_files_path, directory):
    stringJsonFile = []
    versions_xml =[]
    number_file = 0
    for file in xml_files_path:
        direct_pictures = os.path.dirname(file)
        path_to_add = direct_pictures.split("xml_data")[1]
        direct, folder = os.path.split(path_to_add)
        folder_to_save_picture = PATH_FOLDER_EXTRACT + direct + "\\pictures\\" + folder
        create_folder(folder_to_save_picture)

        print(f'path file starting extract{number_file}_{file}')
        version_xml = []
        with open(file, encoding="utf8") as xml_file:

            textExtract = xml_file.read()
            try:
                # extract png
                textTemp = textExtract
                textTemp = textTemp.replace("&lt;", "<")
                textTemp = textTemp.replace("&gt;", ">")
                textTemp = extract_picture_to_png(textTemp, directory, file, folder_to_save_picture)
                data_dict = xmltodict.parse(textTemp)
                version_xml = extract_version_nasform(textTemp)

            except Exception as error:
                print(error)
                try:
                    textTemp = textExtract
                    balise_name = ["form_caption_xml", "radiogroup_xml", "comment_respond_xml", "item3"]
                    for name in balise_name:
                        regexExtract = "<" + name + "\s?>((.|\\n)*?)<\/" + name + "\s?>"
                        textTemp = re.sub(regexExtract, lambda x: x.group(0).replace("&lt;", "<"), textTemp)
                        textTemp = re.sub(regexExtract, lambda x: x.group(0).replace("&gt;", ">"), textTemp)
                    textTemp = extract_picture_to_png(textTemp, directory, file, folder_to_save_picture)
                    data_dict = xmltodict.parse(textTemp)
                    version_xml = extract_version_nasform(textTemp)
                except Exception as error:
                    print(error)
                    print("there is an error while extracting")
            finally:
                if version_xml not in versions_xml:
                    versions_xml.append(version_xml)
                xml_file.close()
                json_data = json.dumps(data_dict)
                stringJsonFile.append(json_data)
        print(f'path file finishing extract`{file}')
        number_file =number_file +1

    return stringJsonFile, versions_xml


def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


def json_to_csv(json_files, directory_temp, file_versions_temp):
    name_file_to_add = directory_temp.split("xml_data")[1]
    nas_file_hundred = directory_temp.split("NAS\\")[1]

    for file_version in file_versions_temp:
        if file_version:
            nasform_regex = "(?sa)nasform_version_\d\d\": \""+file_version

            json_version_temp = []
            for position in range(len(json_files)):
                if re.search(nasform_regex,json_files[position]):
                    print(f"Number file extract {position}")
                    json_object = json.loads(json_files[position])
                    try:
                        json_normalize = flatten_json(json_object['xfa:data'])
                    except:
                        json_normalize = flatten_json(json_object)
                    json_version_temp.append(json_normalize)
            json_normalize = pd.json_normalize(json_version_temp)
            path = PATH_FOLDER_EXTRACT+name_file_to_add+"\\"+nas_file_hundred+"_"+file_version+".csv"
            json_normalize.to_csv(path)


def extract_picture_to_png(xml, directory_path, path_xml_file, folder_to_save):
    # regex_to_extract = "<(.*)xfa:contentType=\"image\/((.|\n)*)\"\s?>(([\w\d\+\/\n\=]*)?)<\/(.*)\s?>"
    regex_to_extract = "(?sa)<([\w]*)\s?xfa:contentType=\\\"image\/([\w\*]*)\\\"\s?href=\\\"\\\"\s?>(.|[^<\>]*)<\/\\1\s?>"
    possibility_pictures = re.findall(regex_to_extract, xml)
   # Trouvé un cas sur les 133 qui ne respectent pas la condition
    regex_to_extract_2 = "(?sa)<([\w]*)\s?xmlns:xfa=\\\"http:\/\/www\.xfa\.org\/schema\/xfa-data\/1\.0\/\\\"\sxfa:contentType=\\\"image\/([\w\*]*)\\\"\shref=\\\"\\\"\s?>(.|[^<\>]*)<\/\\1\s?>"
    possibility_pictures_2 = re.findall(regex_to_extract_2, xml)
    if possibility_pictures_2:
        possibility_pictures = possibility_pictures + possibility_pictures_2
    # if not possibility_pictures:
    #     regex_to_extract = "<(.)* xfa:contentType=\"image\/JPG\" href=\"\"\n>(.|\n)*?<\/(.)*\n>"
    #     possibility_pictures = re.findall(regex_to_extract, xml)

    number_picture = 0
    for possibility_picture in possibility_pictures:
        picture_name = create_image_image_name( path_xml_file,  possibility_picture[0], folder_to_save)
        regex = "<(.*) xfa:contentType=\"image\/(.*)\/>"
        picture = possibility_picture[2]
        if not re.search(regex, picture):
            with open(picture_name, "wb") as fh:
                fh.write(base64.b64decode(picture))
            if os.path.exists(picture_name):
                xml_temp = xml.replace(picture, picture_name)
                xml = xml_temp
            number_picture = number_picture + 1
    return xml


def create_image_image_name( xml_path_file, end_balise, folder_to_save):
    filename = os.path.basename(xml_path_file)
    name_xml_file = filename.replace('.xml', '')
    name_xml_file = name_xml_file + "_" + end_balise
    name_xml_file = name_xml_file + '.jpg'
    name_xml_file = folder_to_save + "\\" + name_xml_file
    return name_xml_file


def extract_parent_parent_directorys(xml_paths):
    parent_parent_directory_array =[]
    for xml_path in xml_paths:
        parent_directory, directory_name = os.path.split(xml_path)
        parent_parent_directory, parent_directory_name = os.path.split(parent_directory)
        parent_parent_parent_directory, parent_parent_directory_folder = os.path.split(parent_parent_directory)
        if not parent_parent_directory_folder in parent_parent_directory_array:
            parent_parent_directory_array.append(parent_parent_directory_folder)
    return parent_parent_directory_array

try:
    directory = sys.argv[1]
    xml_files_path = extract_files(directory, ".xml")
    folders = extract_parent_parent_directorys( xml_files_path)


    for folder in  folders:
        xml_files_path_to_analyse = [path for path in xml_files_path if folder in path]

        print(len(xml_files_path_to_analyse))
        directory_extract = None
        if folder in directory:
            directory_extract = directory
        else:
            directory_extract = directory + "\\" + folder
        jsonFiles, file_versions = xml_files_to_json(xml_files_path_to_analyse, directory_extract)
        json_to_csv(jsonFiles, directory_extract, file_versions)
except Exception as error:
    print(error)
    print('You must add an path in the command line')




#def move_done_file():



