# Program to convert an xml
# file to json file

# import json module and xmltodict
# module provided by python
import json
import xmltodict
import pandas as pd
# open the input xml file and read
# data in form of python dictionary
# using xmltodict module

name_file =""
path ="path"

with open(path) as xml_file:
    textExtract = xml_file.read()
    textExtract = textExtract.replace("&lt;", "<")
    textExtract = textExtract.replace("&gt;", ">")
    data_dict = xmltodict.parse(textExtract)
    xml_file.close()
    # generate the object using json.dumps()
    # corresponding to json data
    #data_dict = xmltodict.parse(dev)
    json_data = json.dumps(data_dict)


    # Write the json data to output
    # json file
    with open("data"+name_file+".json", "w") as json_file:
        json_file.write(json_data)
        json_file.close()