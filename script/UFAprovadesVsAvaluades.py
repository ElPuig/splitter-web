#!/usr/bin/python3
# -*- coding: UTF-8 -*-


import os
import sys
import PyPDF2
import re

SOURCE_FILE_SAGA = sys.argv[1]
TMP_DIR = '../uploads/tmp'

patro = re.compile('UF\d\d-\d{3,}')

def openfile(file):
    butlletins = open(file,"rb")
    return butlletins

def main(_filePdf):
    num_pages = _filePdf.getNumPages()
    current_page = 0
    avaluades = 0
    ap = 0
    while current_page < num_pages:
        page_text = _filePdf.getPage(current_page).extractText()

        llistaUFs = patro.findall(page_text)
        #esborrem la FCT (UF01-317) pq amb amb l'expressió regular es cola al llistat
        while 'UF01-317' in llistaUFs:
            llistaUFs.remove('UF01-317')
        #print(llistaUFs)

        #UF's aprovades
        for uf in llistaUFs:
            nota = int(uf[7:])
            if nota >=5:
                ap += 1

        #Qtat de UF's avaluades per cada pàgina
        l = len(llistaUFs)
        avaluades += l
        current_page += 1

    print(f"Avaluades: {avaluades}, aprovades: {ap} : {((ap/avaluades)*100):.2f}%")

if __name__ == "__main__":
    if len(sys.argv)==2:
        try:
            f = open(SOURCE_FILE_SAGA, 'rb')
            comanda = "/usr/bin/gs -o "+TMP_DIR+"/repair.pdf -sDEVICE=pdfwrite "+SOURCE_FILE_SAGA
    
            os.system(comanda)

            f = open(TMP_DIR+"/repair.pdf", 'rb')

            pdf = PyPDF2.PdfFileReader(f)
            main(pdf)
        except FileNotFoundError as e:
            print(f"No existeix el fitxer {argv[1]}")
    else:
        print("Falta el pdf")
