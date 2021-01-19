#!/bin/bash
#by Fede Jerez @ INS Puig Castellar STKO
# USO: ./SagaSplit.sh fichero_notas.pdf

if [[ -f "$1" ]]
then


	#Convertimos a txt para sacar nombres y numero de paginas

	pdftotext $1 informe.txt
	grep -A2 "Alumne" informe.txt | grep -v -- "^--$"|grep -v "Alumne"|sed '0~2d'|uniq|sed "s/ /_/g">alumnes.txt

	#Alumnos totales
	alumtotal=$(cat alumnes.txt|wc -l)
	#paginas_pdf
	pagtotal=$(pdftk $1 dump_data_utf8|grep 'NumberOfPages'|cut -d ' ' -f 2)
	#pagines per alumne
	((saltpag = $pagtotal / $alumtotal))

	echo "Nombre d'alumnes... $alumtotal"
	echo "Pagines totals..... $pagtotal"
	echo "Salt de pagina..... $saltpag"
	echo "Generant informes, please wait..."

	inici=1
	final=$saltpag

	while IFS= read -r line
	do
		pdftk $1 cat $inici-$final output $line.pdf
		((inici += saltpag))
		((final=inici+saltpag-1))
	done < "alumnes.txt"

	rm informe.txt alumnes.txt
else
	echo "Falta nom del fitxer de notes"
fi
