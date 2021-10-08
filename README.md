# pdfExtractCapi
Ce projet permet d'extraire 

Préconditions de l'algorithme:
  Il extrait des arborescences de ce style:
         NAS 
          |- "NAS_X0X à NAS-X99"
                           |- "NAS-Adresse- Nombre"
                                           |-   adresse.pdf

# Pour partir l'algorithme
Deux parties
1. pdf à csv
Cet algorithme utilise la librairie pyautogui afin d'ouvrir et automatise l'extraction en xml pour les fichiers dont 
   l'option extraction est requis. Si vous roulez le code à partir de pycharm, il faut laisser l'écran ouvert
   et ne pas mettre en veille, car sinon le script s'arrête. Le code se retrouve en général dans le fichier pdftoxmlGUI
   
Pour utiliser le script, télécharger pycharm, il va se charger de télécharger le .venv et après rouler run_bash_file avec windows sceduler.
Avant de partir l'algorithme, il faut modifier la 4e ligne selon vos besoins.

Voici comment écrire la commande en générale:
"""
python "path_du_vers_fichier_pdftoxmlGUI" "path_des_fichiers_à_extraire" "année_à_extraire"
"""

Vous avez 3 possibilités de chemin de fichiers à extraire:
   1.Le chemin vers NAS ex. "\\Srv608\ladossi2019\NAS"


   2. Le chemin vers une centaine de NAS "\\Srv608\ladossi2019\NAS\NAS19-00001 à NAS19-00099"


   3. Vers un pdf "\\Srv608\ladossi2019\NAS\NAS19-00001 à NAS19-00099\NAS19-00005  4610 CH LAPORTE Saint-Côme\8091024.pdf"

2.xml à csv
Après avoir fini de transformer et vérifier vos xml, vous pouvez maintenant rouler la 2e partie de l'algorithme.
Vous devez changer la 4e ligne de run_bash_file. Voici la commande à écrire:
"""
python "path_du_vers_fichier_xmltojson" "path_des_fichiers_xml_à_transformer" 
"""
Vous avez 2 possibilités de grosseur de paquets à transformer:
   1.Tous les xml d'une année:
      ex. python .\xmltojson.py  ".\xml_data\2019\NAS"


   2. Une centaine d'xml:
        ex. python .\xmltojson.py  ".\xml_data\2019\NAS\NAS19-00001 à NAS19-00099"
      

