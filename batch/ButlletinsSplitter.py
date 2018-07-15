#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ButlletinsSplitter.py - Versió 1.3
Fitxer d'entrada:     Fitxer PDF amb els butlletins de notes d'un grup sencer
                      amb el nom «informe.pdf», preparat o no per la impressió
                      a doble cara.
Fitxers de sortida:   Un fitxer ZIP amb un fitxer PDF per cada estudiant amb el
                      seu butlletí i reanomenat amb el seu nombre d'ordre i nom.
"""

import glob
import os
import sys
import PyPDF2
from zipfile import ZipFile


SOURCE_FILE_SAGA = sys.argv[1]
RESULT_DIR = str(os.path.dirname(__file__)) + '/tmp/'
RESULT_ZIP_FILE = 'butlletins.zip'

def generate_individual_files(**correct_student_names_dict):
    """def generate_individual_files(**correct_student_names_dict)
    Descripció: Genera un PDF individual amb les notes de cada estudiant,
                reanomenat amb seu nombre d'ordre i el nom sense caràcters
                que no siguin ASCII.
    Entrada:    Diccionari buit amb els noms sense i amb caràcters no ASCII.
    Sortida:    Diccionari ple amb els noms sense i amb caràcters no ASCII.
    """
    butlletins = open(SOURCE_FILE_SAGA, 'rb')
    butlletins_reader = PyPDF2.PdfFileReader(butlletins)

    total_pages = butlletins_reader.getNumPages()
    page_num = 0
    current_student = None
    student_list_number = 1

    # Iterate through the whole PDF source file
    while page_num < total_pages:
        if current_student is None:
            page_text = butlletins_reader.getPage(page_num)
            page_text_string = page_text.extractText()
            (current_student, 
             correct_student_names_dict) = get_student_name(page_text_string,
                                                 **correct_student_names_dict)

        student = current_student

        output_file = RESULT_DIR +\
                      str(student_list_number).zfill(2) +\
                      ' - ' + student +\
                      '.pdf'
        output_writer = PyPDF2.PdfFileWriter()

        # Iterate through the new individually created PDF file
        while (current_student == student and
               current_student is not None and
               page_num <= total_pages):
            output_writer.addPage(page_text)

            page_num += 1

            if page_num < total_pages:
                page_text = butlletins_reader.getPage(page_num)
                page_text_string = page_text.extractText()
                (current_student,
                 correct_student_names_dict) = get_student_name(page_text_string,
                                                     **correct_student_names_dict)

                # Blank page case
                if current_student is None:
                    page_num += 1

            with open(output_file, 'wb') as output_stream:
                output_writer.write(output_stream)
        
        student_list_number += 1

    butlletins.close()

    return correct_student_names_dict


def get_student_name(s, **correct_student_names_dict):
    """def get_student_name(s, **correct_student_names_dict)
    Descripció: Troba el nom de l'alumne al text d'una pàgina del butlletí de
                notes passat com a string.
    Entrada:    String.
    Sortida:    String amb el nom de l'alumne si la pàgina no està buida;
            None en cas contrari.
    """
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
        
        # Remove non-ASCII chars since Apache won't take any at this point
        arranged_student_name = ''.join([i if ord(i) < 128 else '' for i in student])

        # Add to just-ASCII - non-ASCII names link dictionary
        if (arranged_student_name not in correct_student_names_dict and
          arranged_student_name is not None):
            correct_student_names_dict[
                     arranged_student_name.encode('utf-8')
                                       ] = student.encode('utf-8') 

        return arranged_student_name, correct_student_names_dict
    except:  # Blank page case
        return None, correct_student_names_dict


def rename_files_including_nonASCII_chars(**correct_student_names_dict):
    """def rename_files_including_nonASCII_chars(**correct_student_names_dict)
    Descripció: Reanomena els fitxers afegint els caràcters no ASCII.
    Entrada:    Diccionari ple amb els noms sense i amb caràcters no ASCII.
    Sortida:    Cap.
    """
    os.chdir(RESULT_DIR)

    for file in glob.glob('*.pdf'):
        file_name = os.path.basename(file)
        student_number = file_name.split(" - ")[0]
        ASCII_name = file_name.split(" - ")[1].split(".")[0]

        non_ASCII_name = correct_student_names_dict.get(ASCII_name)
        
        os.rename(os.path.abspath(file),
                  os.path.join(os.path.dirname(file),
                               (str(student_number) +
                                " - " +
                                str(non_ASCII_name) +
                                ".pdf")))


def zip_files():
    """def zip_files
    Descripció: Comprimeix tots els butlletins PDF individuals en un únic
                fitxer ZIP.
    Entrada:    Cap.
    Sortida:    Cap.
    """
    with ZipFile(RESULT_ZIP_FILE, 'w') as zip:
        for file in glob.glob('*.pdf'):
            zip.write(file)


def remove_existing_pdf_files(target_dir):
    """remove_existing_pdf_files
    Descripció: Elimina tots els arxius PDF al directori indicat.
    Entrada:    Directori al qual es volen eliminar tots els fitxers PDF.
    Sortida:    Cap.
    """
    pdf_files = [f for f in os.listdir(target_dir) if f.endswith('.pdf')]
    for file in pdf_files:
        os.remove(os.path.join(target_dir, file))


if __name__ == '__main__':
    remove_existing_pdf_files(RESULT_DIR)
    correct_student_names_dict = {}
    correct_student_names_dict = generate_individual_files(
                                          **correct_student_names_dict)
    rename_files_including_nonASCII_chars(**correct_student_names_dict)
    zip_files()
