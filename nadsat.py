#! /usr/bin/env python
#Author: Matthew O'Neill
try:
	import urllib2, sys, os, re
except:
	import sys
	print("Need python 2.x.x, your version is: " +sys.version.split(' ')[0])
	sys.exit(1)

def getDict():
	"""
	Uses the urllib22 library to open http://soomka.com/nadsat.html, which is
	an online page with Nadsat definitions, remove most of the
	unwanted bits and store the definitions in a python dictionary,
	which is returned
	"""
	try:
		request = urllib2.Request("http://soomka.com/nadsat.html")
		handle = urllib2.urlopen(request)
		content = handle.read()
	except Exception:
		print ("Cannot retrieve data. Internet working?")
		exit(0)

	#start and end of the area with the data I want
	content = content.split("<B>Origins</B>")
	content = content[1].split("<!--#include file=\"gohome.html\"-->")

	#remove all html tags (not their contents)
	content = re.sub("<[^>]*>", "", str(content[0]))
	words = {}
	for line in str(content).splitlines():
		if not line.startswith('\t') and not line.startswith(' '):
			splitted = line.split('\t')
			if len(splitted) > 2:
				word = splitted[0].lower()
				#the meaning is either in 1 or 2, based on how many tabs used in html
				meaning = splitted[1] if splitted[1] != '' else splitted[2]
				#add to the dict:
				words[word] = meaning
			
	return words

def lookup(words, inputWord):
	return words[inputWord] if inputWord in words else "not found"

def showIntro(count):
	intro = """
This script provides a dictionary to look up the English meaning of the 
various Nadsat words that appear in Anthony Burgess' novel 
\"A Clockwork Orange\". The definitions used are taken from the webpage: 
http://soomka.com/nadsat.html"""
	print (intro + "\nThere are "+str(count) +" words in the dictionary today.\n")

def main():
	#command line arguments
	if len(sys.argv) > 1:
		words = getDict()
		inputWord = ''
		for i in range(1, len(sys.argv)):
			inputWord += sys.argv[i]
			inputWord += ' '
		inputWord = inputWord.rstrip()
		if inputWord == "printdict":
			for word in words:
				print (word +" : "+ words[word])
		else:
			print (lookup(words, inputWord))
		sys.exit()
	#no arguments
	else:
		print ("Loading data...")
		words = getDict()

		if os.name == "posix":#cross compatibility, yo
			os.system("clear")
		else:
			os.system("cls")

		showIntro(len(words))

	while 1:
		
		inputWord = raw_input("Enter a word (or type \'exit\' to quit): ").lower()
		
		if inputWord == "printdict":
			for word in words:
				print (word +" : "+ words[word])

		elif inputWord == "printdicttofile":#for my benefit, to be try
			removed:
				fp = open(str(raw_input("Enter file name (including full path if necessary, doesn't need to exist): ")), "w")
			except IOError:
				print ("Can't open that file.")
				sys.exit(1)
			for word in words:
				fp.write(word +" : "+ words[word] +'\n')
			fp.close()
			print ("Done")

		elif inputWord.rstrip() == '' :
			pass

		elif inputWord != 'exit' and inputWord != 'quit':
			print("Meaning: " + lookup(words, inputWord))

		else:
			sys.exit(0)

if __name__ == '__main__':
	main()