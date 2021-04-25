# Program to convert an xml
# file to json file
import json
import xmltodict
import os
import re
import pandas as pd
import base64


def extract_xml_files(directory):
    try:
        xml_Files = []
        for path in os.listdir(directory):
            if ".xml" in path:
                full_path = os.path.join(directory, path)
                if os.path.isfile(full_path):
                    xml_Files.append(full_path)
        return xml_Files
    except:
        print("Somethings went wrong while extracting file")


def xml_files_to_json(xml_files_path, directory):
    stringJsonFile = []
    for file in xml_files_path:
        # print(file)
        with open(file) as xml_file:
            textExtract = xml_file.read()
            try:
                # extract png
                textTemp = textExtract
                textTemp = textTemp.replace("&lt;", "<")
                textTemp = textTemp.replace("&gt;", ">")
                textTemp = extract_picture_to_png(textTemp, directory, file)
                data_dict = xmltodict.parse(textTemp)

            except:
                try:
                    textTemp = textExtract
                    balise_name = ["form_caption_xml", "radiogroup_xml", "comment_respond_xml", "item3"]
                    for name in balise_name:
                        regexExtract = "<" + name + ">((.|\\n)*?)<\/" + name + ">"
                        textTemp = re.sub(regexExtract, lambda x: x.group(0).replace("&lt;", "<"), textTemp)
                        textTemp = re.sub(regexExtract, lambda x: x.group(0).replace("&gt;", ">"), textTemp)
                    textTemp = extract_picture_to_png(textTemp, directory, file)
                    data_dict = xmltodict.parse(textTemp)
                except:
                    print("there is an error while extracting")
            finally:
                xml_file.close()
                json_data = json.dumps(data_dict)
                stringJsonFile.append(json_data)

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
        json_object = json.loads(jsons_Files[position])
        json_normalize = flatten_json(json_object)
        jsons_Files[position] = json_normalize

    json_normalize = pd.json_normalize(jsons_Files)
    json_normalize.to_csv(".\\firstfile.csv")


def extract_picture_to_png(xml, directory_path, path_xml_file):
    regex_to_extract = "<(.*)xfa:contentType=\"image\/(.*)\">((.|\n)*?)<\/(.*)>"
    possibility_pictures = re.findall(regex_to_extract, xml)
    number_picture = 0
    for possibility_picture in possibility_pictures:
        picture_name = create_image_image_name(directory_path, path_xml_file, number_picture)
        regex = "<(.*) xfa:contentType=\"image\/(.*)\/>"
        picture = possibility_picture[2]
        if not re.search(regex, picture):

            with open(picture_name, "wb") as fh:
                fh.write(base64.b64decode(picture))
            if os.path.exists(picture_name):
                xml_temp = xml.replace(picture, picture_name)
            number_picture = number_picture + 1
            xml = xml_temp
    return xml


def create_image_image_name(directory_path, xml_path_file, number_picture):
    name_xml_file_with_extension = xml_path_file.replace(directory_path + "\\", '')
    name_xml_file = name_xml_file_with_extension.replace('.xml', '')
    name_xml_file = name_xml_file + "_picture"
    name_xml_file = name_xml_file + str(number_picture) + '.jpg'
    name_xml_file = '.\\pictures\\' + name_xml_file
    return name_xml_file


def create_folder_picture():
    if not os.path.exists('.\\pictures'):
        os.makedirs('.\\pictures')

directory = "..\\CaPI immobilier\\CaPIimmobilier\\données\\25-02-2021"
create_folder_picture()
xml_files_path = extract_xml_files(directory)
jsonFiles = xml_files_to_json(xml_files_path, directory)
json_to_csv(jsonFiles)

