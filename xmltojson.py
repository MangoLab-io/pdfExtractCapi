# Program to convert an xml
# file to json file
import json
import xmltodict
import os
import re
import pandas as pd
import base64
import sys


# def extract_xml_files(directory):
#     try:
#         xml_Files = []
#         for path in os.listdir(directory):
#             if ".xml" in path:
#                 full_path = os.path.join(directory, path)
#                 if os.path.isfile(full_path):
#                     xml_Files.append(full_path)
#         return xml_Files
#     except:
#         print("Somethings went wrong while extracting file")

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
    number_file = 0
    for file in xml_files_path:

        print(f'path file starting extract{number_file}_{file}')

        with open(file, encoding="utf8") as xml_file:
            textExtract = xml_file.read()
            try:
                # extract png
                textTemp = textExtract
                textTemp = textTemp.replace("&lt;", "<")
                textTemp = textTemp.replace("&gt;", ">")
                textTemp = extract_picture_to_png(textTemp, directory, file)
                data_dict = xmltodict.parse(textTemp)

            except Exception as error:
                print(error)
                try:
                    textTemp = textExtract
                    balise_name = ["form_caption_xml", "radiogroup_xml", "comment_respond_xml", "item3"]
                    for name in balise_name:
                        regexExtract = "<" + name + "\s?>((.|\\n)*?)<\/" + name + "\s?>"
                        textTemp = re.sub(regexExtract, lambda x: x.group(0).replace("&lt;", "<"), textTemp)
                        textTemp = re.sub(regexExtract, lambda x: x.group(0).replace("&gt;", ">"), textTemp)
                    textTemp = extract_picture_to_png(textTemp, directory, file)
                    data_dict = xmltodict.parse(textTemp)
                except Exception as error:
                    print(error)
                    print("there is an error while extracting")
            finally:
                xml_file.close()
                json_data = json.dumps(data_dict)
                stringJsonFile.append(json_data)
        print(f'path file finishing extract`{file}')
        number_file =number_file +1

    return stringJsonFile


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


def json_to_csv(jsons_Files):

    for position in range(len(jsons_Files)):
        print(f"Number file extract {position}")
        json_object = json.loads(jsons_Files[position])
        try:
            json_normalize = flatten_json(json_object['xfa:data'])
        except:
            json_normalize = flatten_json(json_object)
        jsons_Files[position] = json_normalize

    json_normalize = pd.json_normalize(jsons_Files)
    json_normalize.to_csv(".\\firstfile.csv")


def extract_picture_to_png(xml, directory_path, path_xml_file):
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
        picture_name = create_image_image_name(directory_path, path_xml_file, number_picture, possibility_picture[0])
        regex = "<(.*) xfa:contentType=\"image\/(.*)\/>"
        picture = possibility_picture[2]
        if not re.search(regex, picture):
            directory_picture = os.path.dirname(picture_name)
            create_folder_picture(directory_picture)
            with open(picture_name, "wb") as fh:
                fh.write(base64.b64decode(picture))
            if os.path.exists(picture_name):
                xml_temp = xml.replace(picture, picture_name)
            number_picture = number_picture + 1
            xml = xml_temp
    return xml


def create_image_image_name(directory_path, xml_path_file, number_picture, end_balise):
    filename = os.path.basename(xml_path_file)
    name_xml_file = filename.replace('.xml', '')
    name_xml_file = name_xml_file + "_" + end_balise
    name_xml_file = name_xml_file + '.jpg'
    name_xml_file = '.\\pictures\\' + name_xml_file
    return name_xml_file


def create_folder_picture(name='.\\pictures'):
    if not os.path.exists(name):
        os.makedirs(name)

def create_folder_done_file():
    if not os.path.exists('.\\done_file'):
        os.makedirs('.\\done_file')

try:
    directory = sys.argv[1]
    # directory = "..\\CaPI immobilier\\CaPIimmobilier\\données\\25-02-2021"
    print(directory)
    create_folder_picture()
    xml_files_path = extract_files(directory, ".xml")
    # La possibilité que si je donne un file
    if not xml_files_path and ".xml" in directory:
        xml_files_path = [directory]

    print(len(xml_files_path))
    jsonFiles = xml_files_to_json(xml_files_path, directory)
    json_to_csv(jsonFiles)
except Exception as error:
    print(error)
    print('You must add an path in the command line')


# def move_done_file():


