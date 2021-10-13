# pdfExtractCapi
Ce projet permet d'extraire les NAS et les transformer en CSV. C'est seulement ceux qui ont l'option d'exporter en xml qui seront extraits. 
Il y a 2 parties à l'algorithme: PDF à XML et XML à CSV.

# Préconditions de l'algorithme:
Les dossiers doivent avoir cet arborescence:
``` 
NAS 
   |_
     "NAS_X0X à NAS-X99"
                        |_ 
                           "NAS-Adresse- Nombre"
                                                |_ 
                                                  numéro_NAS.pdf
```

# Pour partir l'algorithme

## 1. PDF À XML
Cet algorithme utilise la librairie pyautogui afin d'ouvrir le pdf et automatiser l'extraction en xml. Si vous roulez le code à partir de pycharm, il faut laisser l'écran ouvert
   et ne pas mettre en veille, car sinon le script s'arrête.
   
Pour utiliser le script, télécharger pycharm community(https://www.jetbrains.com/fr-fr/pycharm/download/#section=windows).  Il va télécharger le .venv et après rouler run_bash_file avec windows sceduler.
Avant de partir l'algorithme, il faut modifier la 4e ligne de run_bash_file selon votre besoin et elle doit la forme ci-dessous.
```
python "path_du_vers_fichier_pdftoxmlGUI" "path_des_fichiers_à_extraire" "année_à_extraire"

ex. python .\pdftoxmlGUI "\\Srv608\ladossi2019\NAS" 2019
```

Vous avez 3 possibilités de chemin pour remplacer "path_des_fichiers_à_extraire":
- Le chemin vers NAS
> ex. "\\Srv608\ladossi2019\NAS"
- Le chemin vers une centaine de NAS
>  ex. "\\Srv608\ladossi2019\NAS\NAS19-00001 à NAS19-00099"
- Vers un pdf
>  ex. "\\Srv608\ladossi2019\NAS\NAS19-00001 à NAS19-00099\NAS19-00005  4610 CH LAPORTE Saint-Côme\8091024.pdf"


Cela créera le dossier *xml_data* où se trouvera les fichiers xmls.

## 2. XML À CSV
Après avoir fini de transformer et vérifier vos xml, vous pouvez maintenant rouler la 2e partie de l'algorithme.
Vous devez changer la 4e ligne de run_bash_file et inscrire la commande ci-dessous:
```
python "path_du_vers_fichier_xmltojson" "path_des_fichiers_xml_à_transformer" 
```
Vous avez 2 moyens pour transformer les xml.

- Par année
>    ex. python .\xmltojson.py  ".\xml_data\2019\NAS"


- Par centaine d'une année
>    ex. python .\xmltojson.py  ".\xml_data\2019\NAS\NAS19-00001 à NAS19-00099"
      
Cela créera le fichier csv_data. Les csv sont créés en batch de 100 et vous pouvez trouver les photos reliés au pdf.

# Le dossier Log
Deux fichiers se retrouvent dans ce dossier vous donnent de l'information supplémentaire.
### - *pdf_that_are_not_extract.csv*
Ce fichier dit quels fichiers ne sont pas extraits.

### - *folder_empty.csv*
Ce ficher dit quel dossier est vide. Cela vous aidera à chercher les fichiers que l'algorithme ne cherche pas et les extraires un par un.  
