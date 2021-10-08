

import subprocess
import psutil
import pyautogui
import pyperclip
import sys
from ReasonForm import ReasonForm
from FilterFileExtract import *

pyautogui.FAILSAFE=False


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
    im=None
    try:
        im = pyautogui.locateOnScreen(".\\ComparePicture\\form_options.PNG", confidence=0.8)
        time.sleep(0.3)
    except IOError:
        print("locate ON screen didn't work")
        pass
    if im:
        contains_extract_form_option = True
        pyautogui.hotkey('shift', 's')
        pyautogui.hotkey('shift', 'x')
        time.sleep(1)
        pyautogui.press('tab', presses=6)
        pyautogui.press('enter')
        pyperclip.copy(path_to_save)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
        pyautogui.press('tab', presses=9)
        pyautogui.press('enter')
    return contains_extract_form_option

def waiting_open_pdf():
    while pyautogui.locateOnScreen(".\\ComparePicture\\readypicture.PNG", confidence=0.8) is None:
        pass



def proccess_pdfs(pdfFiles, reason_form, path_to_save, directory_name):
    print('There are ' + str(len(pdfFiles)) + ' files to transfert')
    logging.info(f'There are {len(pdfFiles)} files to transfert')
    numberFile = 0
    for pdfFile in pdfFiles:
        subdirectory_and_file_to_join = pdfFile.split("\\" + directory_name + "\\")[1]
        path_to_add = os.path.split(subdirectory_and_file_to_join)[0]
        path_to_save_pdf = path_to_save + "\\" + path_to_add
        create_folder(path_to_save_pdf)
        print("You are processing the " + str(numberFile) + "/" + str(len(pdfFiles)))
        file_xml = pdfFile.replace(".pdf", "_data.xml")
        file_xml = os.path.basename(file_xml)
        file_xml = path_to_save_pdf + "\\" + file_xml
        if not os.path.exists(file_xml):
            proc = subprocess.Popen(pdfFile, shell=True, stdout=subprocess.PIPE)
            try:
                waiting_open_pdf()
                extract_form_bool = automatic_key(os.path.abspath(path_to_save_pdf))
                if not extract_form_bool:
                    reason_form.append(pdfFile, "Can't export in xml, because the file does not have")
                if extract_form_bool:
                    reason_form.append(pdfFile, "PDF export in xml")
                time.sleep(3)
                kill(proc.pid)
                time.sleep(1)
            except subprocess.TimeoutExpired:
                kill(proc)
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




# Need full path to be sure
def main():
    # Instanciate form reason to extract a pdf
    import logging
    # Argument to take the path
    logging.basicConfig(filename='pdf_to_xml_gui.log', level=logging.DEBUG)
    path = sys.argv[1]
    print(path)
    logging.info(f'Voici le path que le script a été appliqué {path}')

    year = sys.argv[2]

    reason_form = ReasonForm(year)
    print(path)
    logging.info(f'Lannée de votre NAS {year}')

    path_to_save_folder = ".\\xml_data\\" + str(year) + "\\"
    logging.debug('start to extract file')

    # À ajouter une vérification
    pdfFiles = []
    directory_name = None
    path_to_save = None
    if not ".pdf" in path:
        parent_directory, directory_name = os.path.split(path)
        pdfFiles = extract_files(path, ".pdf")

        if directory_name == "NAS":

            path_to_save = path_to_save_folder + directory_name

            pdfFiles = extract_number_sublevel(pdfFiles, path, 3)

        else:
            path_to_save = path_to_save_folder +"NAS\\"+ directory_name
            pdfFiles = extract_number_sublevel(pdfFiles, path, 2)
        pdfFiles = get_last_or_second_last_modify_file(pdfFiles, reason_form)
    else:
        # Le cas d'un fichier d'un pdf seul
        pdfFiles.append(path)
        path_to_save = ".\\xml_data\\" + str(year)+ "\\NAS"
        directory_name ="NAS"

    logging.debug('start extract pdf')
    proccess_pdfs(pdfFiles, reason_form, path_to_save, directory_name)

    # Compare folder
    if not ".pdf" in path:
        reason_form.compare_folder(path, path_to_save_folder)
        reason_form.extract_empty_folder()
    # add_3e_file_supplémentaire
    reason_form.extract_to_pdf()

if __name__ == "__main__":
    main()






