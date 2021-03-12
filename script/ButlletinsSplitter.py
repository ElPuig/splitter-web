#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ButlletinsSplitter1.3.py
Fitxer d'entrada:     Fitxer PDF amb els butlletins de notes d'un grup sencer
                      amb el nom «informe.pdf», preparat o no per la impressió
                      a doble cara.
Fitxers de sortida:   Un fitxer ZIP amb el butlletí de cada estudiant en un
                      arxiu PDF individual i reanomenat amb el seu nom.
"""

import glob
import os
import sys
import PyPDF2
from zipfile import ZipFile

SOURCE_FILE_SAGA = sys.argv[1]
RESULT_ZIP_FILE = 'studenten.zip'
TMP_DIR = '../uploads/tmp'


"""def generate_individual_files(s)
Descripció: Divideix el PDF amb tots els butlletins de notes
            en PDF amb els butlletins individuals per estudiant.
Entrada:    Cap.
Sortida:    Cap.
"""
def generate_individual_files():
    butlletins = open(SOURCE_FILE_SAGA, 'rb')
    try:
        butlletins_reader = PyPDF2.PdfFileReader(butlletins)
    except:
        print("<br/>El fitxer seleccionat no és de butlletins de notes o no té el format esperat.")
        sys.exit()

    total_pages = butlletins_reader.getNumPages()
    page_num = 0
    current_student = None

    # Iterates through whole PDF source file
    while page_num < total_pages:
        if current_student is None:
            page_text = butlletins_reader.getPage(page_num)
            page_text_string = page_text.extractText()
            current_student = get_student_name(page_text_string)

        student = current_student
        output_file = (os.path.join(TMP_DIR, student + '.pdf'))
        output_writer = PyPDF2.PdfFileWriter()

        # Iterates through new individually created PDF file
        while (current_student == student and
               current_student is not None and
               page_num <= total_pages-1):
            output_writer.addPage(page_text)

            page_num += 1

            if page_num < total_pages:
                page_text = butlletins_reader.getPage(page_num)
                page_text_string = page_text.extractText()
                current_student = get_student_name(page_text_string)

                # Blank page
                if current_student is None:
                    page_num += 1

            with open(output_file, 'wb') as output_stream:
                output_writer.write(output_stream)

    butlletins.close()


"""def get_student_name(s)
Descripció: Troba el nom de l'alumne al text d'una pàgina del butlletí de
            notes passat com a string.
Entrada:    String.
Sortida:    String amb el nom de l'alumne si la pàgina no està buida;
            None en cas contrari.
"""
def get_student_name(s):

    try:
        # Get student's name
        """ start: 'Grup' (al text sempre davant del nom de l'alumne
                           i el seu DNI)
            end:   'CFP' (al text sempre darrere del nom de l'alumne
                          i el seu DNI)
        """
        start_index = s.index('Grup') + len('Grup')
        end_index = s.index('CFP')
        # Ignore ID's last char
        student_with_id = s[start_index:end_index][:-1]

        # Remove ID from substring (every number and/or
        #                           letter followed by a number)
        student = ''.join(l for i, l in enumerate(student_with_id)
                          if not l.isdigit() and not
                          (l.isupper() and student_with_id[i+1].isdigit()))

        return student
    except:  # Blank page
        return None


"""def zip_files
Descripció: Comprimeix tots els butlletins PDF individuals en un únic
            fitxer ZIP.
Entrada:    Cap.
Sortida:    Cap.
"""
def zip_files():
    pdf_files_list = [os.path.join(os.getcwd(), TMP_DIR, f) for f
                      in os.listdir(os.path.join(os.getcwd(),TMP_DIR))
                      if f.split('.')[1]=='pdf']

    if len(pdf_files_list) == 1:
        print("<br/>El fitxer seleccionat no és de butlletins de notes o no té el format esperat.")
        sys.exit()
    else:
        result_zip_file = os.path.join(os.getcwd(),TMP_DIR, RESULT_ZIP_FILE)
        with ZipFile(result_zip_file, 'w') as zip:
            for file in pdf_files_list:
                file_without_folder_path = file.split('/')[-1]
                zip.write(file, file_without_folder_path)


"""def remove_tmp_files
Descripció: Suprimeix tots els butlletins PDF individuals.
Entrada:    Cap.
Sortida:    Cap.
"""
def remove_tmp_files():
    pdf_files_list = [os.path.join(os.getcwd(),TMP_DIR, f) for f
                      in os.listdir(os.path.join(os.getcwd(),TMP_DIR))
                      if f.split('.')[1]=='pdf']

    for file in pdf_files_list:
        os.remove(file)


if __name__ == '__main__':
    generate_individual_files()
    zip_files()
    remove_tmp_files()
