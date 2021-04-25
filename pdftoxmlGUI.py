import os
import subprocess, time
import psutil
import pyautogui
import re
import pyperclip


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


# Need full path to be sure
path = "C:\\Users\\Asus\\Desktop\\CaPI immobilier\\CaPIimmobilier\\données\\01-03-2021\\Complet avec revenu"
# Pour extraire les xfas
# path = "C:\\Users\\Asus\\Desktop\\CaPIimmobilier\\données\\06-04-2021"

def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()


def automatic_key(path_to_save, path_temp):
    pyautogui.press('f10')
    pyautogui.press('right')
    pyautogui.press('down', presses=17)
    pyautogui.press('enter')
    pyautogui.press('down')
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('tab', presses=6)
    pyautogui.press('enter')
    if path_to_save != path_temp:
        path_to_save = path_temp
        pyperclip.copy(path_to_save)
        pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    pyautogui.press('tab', presses=9)
    pyautogui.press('enter')
    return path_to_save


def waiting_open_pdf():
    while pyautogui.locateOnScreen("./convertirbutton1.PNG", confidence=0.8) is None:
        print(pyautogui.locateOnScreen("./convertirbutton1.PNG", confidence=0.8))
        box = pyautogui.locateOnScreen("./okbutton.PNG", confidence=0.8)
        if box != None:
            x, y = pyautogui.locateCenterOnScreen('./okbutton.PNG')
            pyautogui.click(x, y)
            pyautogui.moveTo(5, 5)


# def verfication_task():
# def verfication_task():
# À ajouter une vérification


pdfFiles = extract_files(path, ".pdf")
# ajouter la condition si le file est déjà là en xml
path_to_save = ""
print('There are ' + str(len(pdfFiles)) + ' files to transfert')
numberFile = 0
for pdfFile in pdfFiles:
    print("You are processing the "+ str(numberFile) +"/"+str(len(pdfFiles)))
    file_xml = pdfFile.replace(".pdf", "_données.xml")
    if not os.path.exists(file_xml):
        try:
            path_temp = re.search("(.*)\\\\", pdfFile, re.IGNORECASE).group(1)
            proc = subprocess.Popen(pdfFile, shell=True)
            waiting_open_pdf()
            path_to_save = automatic_key(path_to_save, path_temp)
            time.sleep(1)
            kill(proc.pid)
            time.sleep(1)
        except subprocess.TimeoutExpired:
            kill(proc.pid)
        finally:
            if os.path.exists(file_xml):
                print(file_xml + " was successfully exported")
            else:
                print(file_xml + "had a problem and was not exported in xml")
    else:
        print("The following file already exists " + file_xml)
    numberFile = numberFile + 1
