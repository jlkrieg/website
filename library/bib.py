#!/usr/bin/env python 
# -*- coding: utf-8 -*-

#This script translates .xls files into bibTex using xlrd.
#Loops over rows and writes out author, coauther, title, year, publisher, language, ISBN and location
#Some optimizationfor author and language applied to adjust for plone4 bibTex setup
import xlrd, codecs, sys

if len(sys.argv) > 1: filename = sys.argv[1]
else: filename="/users/eeh/vschneider/library/BibiliothekTL-HL" #.xls

fields = {}
editorV = ('(Ed.)', '(Eds.)', '(Hrsg.)','(Hrsg)','et al.', 'et. al','(et al, Editor)')
editorVneu = ('(Ed.)', '(Eds.)','(Hrsg.)', '(Hrsg.)','et al.', 'et al.','et al. (Ed.)')
lang = {'d' :'German','e' :'English','f' :'French'}

book = xlrd.open_workbook(filename + ".xls")
sh = book.sheet_by_index(0)

outname = filename.rpartition("/")[-1]
outfile=unicode(outname + '.bib')
f = codecs.open(outfile, 'w')

filledrows=0
for row in range(1, sh.nrows):
	for field in range (0,sh.ncols):
		fieldname = sh.cell_value(0,field)
		a = sh.cell_value(row, field)
		fields[fieldname] = a.encode("utf_8") if isinstance(a, (str, unicode)) else str(int(a))
	
	if (fields["Autor"] or fields["Titel"]): # leere Eintraege weglassen	
		f.write('@book{' + str(row) + ',\n'); filledrows += 1	
# Coautoren splitten, 'and' einfuegen und zusammenfuegen mit Autor. 
# 'Editor' in Autor und Coautor abschneiden und zu Nachnamen hinzufuegen. 
# et al. in Autoren verarzten
		liste =  fields["Autor"]
		for co in fields["Coautoren"].split('; '):
			if co: liste += ' and ' + co		
		for j,key in enumerate(editorV): 
			y = 0
			for i in range (liste.count(key)):
				y = liste.find(key, y)
				x = liste.rfind(', ',0,y)
				liste = liste[0:x] + " " + editorVneu[j] + ", " + liste[x+2:y-1] + liste[y + len(key):]				
		f.write('  author = {' +liste + '},\n')
# Autoren Ende
# other fields: title, year, publisher, ISBN
		f.write('  title = {' + fields["Titel"] + '},\n')
		f.write('  year = {' + str(fields["Erschjahr"]) + '},\n')
		f.write('  publisher = {' + fields["Verlag"] + '},\n')
		f.write('  ISBN = {' + str(fields["ISBN_Nr"]) + '},\n')
		f.write('  number = {' + str(fields["Inventar_Nr"]) + '},\n')
# Sprachzerlegung 
		f.write('  Note = {Language: ') 
		a = fields["Sprache"].split('/')
		for j,co in enumerate(a):
			if j:	f.write('/') 
			try: f.write(lang[co])
			except KeyError: print('Other language in line '+str(row)+'. Check and maybe add another language!: ' + fields["Sprache"])	
		f.write(', \n')
# Sprachzerlegung Ende
# final fields: Standort, Sortierungsmerkmal
		f.write('Located: ' + fields["Standort"] +' '+ fields["Sortierungsmerkmal"] + '}\n')
		f.write('}\n\n')
f.close()
print('Library to bib files complete. \nNumber of processed entries: '+ str(filledrows))	    
