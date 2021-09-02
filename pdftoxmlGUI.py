import logging
import os
import subprocess, time
import psutil
import pyautogui
import re
import pyperclip
import sys
from ReasonForm import ReasonForm
from FilterFileExtract import *


logging.basicConfig(filename='information_with_path_data.log', level=logging.DEBUG)

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()


def automatic_key(path_to_save):
    contains_extract_form_option = False
    pyautogui.press('f10')
    pyautogui.press('right')
    pyautogui.press('enter')
    if pyautogui.locateOnScreen(".\\ComparePicture\\form_options.PNG", confidence=0.8):
        contains_extract_form_option = True
        # pyautogui.hotkey('ctrl', 'v')
        pyautogui.hotkey('shift', 's')
        pyautogui.hotkey('shift', 'x')
        #pyautogui.hotkey('shift', 's')
        #pyautogui.press('down', presses=17)

        #pyautogui.press('down')
        #pyautogui.press('enter')
        time.sleep(1)
        pyautogui.press('tab', presses=6)
        pyautogui.press('enter')
        # if path_to_save != path_temp:
        #     path_to_save = path_temp
        pyperclip.copy(path_to_save)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
        pyautogui.press('tab', presses=9)
        pyautogui.press('enter')
    return contains_extract_form_option
# "\\SRV608\ladossi2020\NAS\NAS20-00700 à NAS20-00799"

def waiting_open_pdf():
    while pyautogui.locateOnScreen(".\\ComparePicture\\readypicture.PNG", confidence=0.8) is None:
        # print(pyautogui.locateOnScreen(".\\ComparePicture\\readybutton.PNG", confidence=0.8))
        box = pyautogui.locateOnScreen(".\\ComparePicture\\okbutton.PNG", confidence=0.8)
        # if box != None:
        #     x, y = pyautogui.locateCenterOnScreen('.\\ComparePicture\\okbutton.PNG')
        #     pyautogui.click(x, y)
        #     pyautogui.moveTo(5, 5)


# "\\SRV608\ladossi2020\NAS\NAS20-00001 à NAS20-00099"
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
        logging.info(f'Somethings went wrong while extracting files')


# Need full path to be sure
def main():
    # Instanciate form reason to extract a pdf
    reason_form = ReasonForm()
    # Argument to take the path
    path = sys.argv[1]
    print(path)
    logging.info(f'Voici le path que le script a été appliqué {path}')
    parent_directory, directory_name = os.path.split(path)

    # À ajouter une vérification

    pdfFiles = extract_files(path, ".pdf")
    pdfFiles = extract_number_sublevel(pdfFiles, path, 2)
    pdfFiles = get_last_or_second_last_modify_file(pdfFiles, reason_form)

    # ajouter la condition si le file est déjà là en xml
    path_to_save = "C:\\Users\\dpare\\Documents\\pdfExtractCapi\\xml_data\\2020\\"
    path_to_save += directory_name
    print('There are ' + str(len(pdfFiles)) + ' files to transfert')
    logging.info(f'There are {len(pdfFiles)} files to transfert')
    numberFile = 0
    for pdfFile in pdfFiles:
        subdirectory_and_file_to_join = pdfFile.split("\\"+directory_name+"\\")[1]
        path_to_add = os.path.split(subdirectory_and_file_to_join)[0]
        path_to_save_pdf = path_to_save+"\\"+path_to_add
        create_folder(path_to_save_pdf)
        print("You are processing the " + str(numberFile) + "/" + str(len(pdfFiles)))
        file_xml = pdfFile.replace(".pdf", "_data.xml")
        file_xml = os.path.basename(file_xml)
        file_xml = path_to_save_pdf + "\\" + file_xml
        if not os.path.exists(file_xml):
            try:
                # path_temp = re.search("(.*)\\\\", pdfFile, re.IGNORECASE).group(1)
                proc = subprocess.Popen(pdfFile, shell=True)
                waiting_open_pdf()

                extract_form_bool = automatic_key(path_to_save_pdf)
                if not extract_form_bool:
                    reason_form.append(pdfFile,"Can't export in xml, because the file does not have")
                if extract_form_bool:
                    reason_form.append(pdfFile, "PDF export in xml")
                time.sleep(3)
                kill(proc.pid)
                time.sleep(1)
            except subprocess.TimeoutExpired:
                kill(proc.pid)
            finally:
                if os.path.exists(file_xml):
                    print(file_xml + " was successfully exported")
                    logging.debug(f'{file_xml} was successfully exported')
                else:
                    print(file_xml + "had a problem and was not exported in xml")
                    logging.debug(f'{file_xml} had a problem and was not exported in xml')
        else:
            print("The following file already exists " + file_xml)
            reason_form.append(pdfFile, "PDF already in xml")
            logging.debug(f'The following file already exists {file_xml}')
        numberFile = numberFile + 1
    reason_form.extract_to_pdf()

if __name__ == "__main__":
    main()

path = ""
# path = "C:\\Users\\Asus\\Desktop\\CaPI immobilier\\CaPIimmobilier\\données\\01-03-2021\\Complet avec revenu"
# Pour extraire les xfas
# path = "C:\\Users\\Asus\\Desktop\\CaPIimmobilier\\données\\06-04-2021"
