"""
For the curious, some references:
http://www.pythonware.com/library/pil/handbook/image.htm
http://stackoverflow.com/questions/2181292/using-the-image-point-method-in-pil-to-manipulate-pixel-data
http://stackoverflow.com/questions/138250/read-the-rgb-value-of-a-given-pixel-in-python-programaticly
http://docs.python.org/library/binascii.html
http://www.network-science.de/ascii/

When using this product. Please remember to give credit to oni49, 
the author of this product. 

Reachable at Twitter @oni_49 and GitHub @oni49. Feedback welcome.
"""

from PIL import Image
import math, binascii

alphabet = 'abcdefghijklmnopqrstuvwxyz_'
def getNumber(c, k):
	"""Function to turn a letter into a number and shift it
	will use 27 letters such that we can encode special characters
	as a _ """
	try:
		i = alphabet.index(c)
	except Exception, e:
		i = 26
	x = math.fmod(i + k, 27)
	return int(x)

def getLetter(c, k):
	"""Take a number and turn it into a character"""
	key = 27 - int(math.fmod(k, 27))
	x = int(math.fmod(c+key, 27))
	try:
		a = alphabet[x]
	except Exception, e:
		a = '?'

	return a

def pad(s):
	"""Take in a binary string and pad it to make it 5 bits long"""
	last = len(s)
	##get rid of "0b" notation
	s = s[2: last]
	## if it's less than 5 digits
	if len(s) < 5:
		##make a string to hold the zeros
		c = ""
		for i in range(5 - len(s)):
			c = c + "0"
		s = c + s
	return s


def enShift(m, k):
	"""Function to encrypt the string passed in with a given key"""
	m = m.lower()
	c = ""
	for letter in m:
		x = getNumber(letter, k)
		c = c + pad(bin(x))
	return c

def split(s):
	"""FUnction to split a string into sections of 5 characters.
	Code from:
	http://code.activestate.com/recipes/496784-split-string-into-n-size-pieces/"""
	return [s[i:i+5] for i in range(0, len(s), 5)]
	
	

def deShift(c, k):
	"""Function to change the string back to plain text"""
	list = split(c)
	m = ""
	for num in list:
		x = int(num, 2)
		m = m + getLetter(x, k)
	return m

def hideBit(pixel, bit):
	""" function to hide a bit inside the blue value of a RGB pixel, only needs to do plus one, because
	we're working mod 2"""
	blue = pixel[2]
	if int(math.fmod(blue,2)) != int(bit):
		blue = blue + 1
	return blue

def uncoverBit(pixel):
	"""Function to find what bit we may have hidden in the blue value of the pixel"""
	blue = pixel[2]
	bit = int(math.fmod(blue, 2))
	return str(bit)

def hideMessage(imgPath, outPath, text, key):
	##make the cipher text to hide
	ctext = enShift(text, key)

	##set up the image, based on the path
	img = Image.open(imgPath)
	pic = img.load()

	##make a list of all pixels
	pixelList = list(img.getdata())

	##loop through the message and hide each bit
	for i in range(len(ctext)):
		##grab the pixel
		pixel = pixelList[i]
		##hide the bit in the pixel
		pixelList[i] = pixel[0], pixel[1], hideBit(pixel, ctext[i])
	##overwrite the new pixels onto the picture
	img.putdata(pixelList)

	try:
		img.save(outPath, "BMP")
	except IOError:
		print "Unable to write back"

def uncoverMessage(imgPath, key):
	##set up the image, based on the path
	img = Image.open(imgPath)
	pic = img.load()

	##make a list of all pixels
	pixelList = list(img.getdata())

	##file to print out to
	msgOut = open('message.txt', 'w')

	bitString = ""
	for i in range(len(pixelList)):
		bitString = bitString + uncoverBit(pixelList[i])
	message = deShift(bitString, key)
	msgOut.write(message)
	print "Message written to message.txt"

print "+---------------------------------------------+"
print ""
print "  ___|  |                    __ )  |           "
print "\\___ \\  __|  _ \\  _` |  _ \\  __ \\  | |   |  _ \\"
print "      | |    __/ (   | (   | |   | | |   |  __/"
print "_____/ \\__|\\___|\\__, |\\___/  ___/ _|\\__,_|\\___|"
print "                |___/                          "
print "+---------------------------------------------+"

def branch():

	select = raw_input("What would you like to do?: ")
	select = select.lower().strip()

	if select == "hide":
		print "+---------------------------------------------+"
		print "HIDE MESSAGE"
		print "+---------------------------------------------+"

		imagePath = raw_input("Enter the in photo to use as a medium with extension (.bmp): ")
		outPath = raw_input("Enter the output file with extension (.bmp): ")
		message = raw_input("Enter the message you want to hide: ")
		key = int(raw_input("Enter the key to encrypt the message with (integer): "))

		hideMessage(imagePath, outPath, message, key)

		img1 = Image.open(imagePath)
		img2 = Image.open(outPath)

		print imagePath, img1.format, "%dx%d" % img1.size, img1.mode
		print outPath, img2.format, "%dx%d" % img2.size, img2.mode

		branch()

	elif select == "find":
		print "+---------------------------------------------+"
		print "FIND MESSAGE"
		print "+---------------------------------------------+"

		outPath = raw_input("Enter the file name with extension (.bmp): ")
		key = int(raw_input("Enter the key to decrypt the message with (integer): "))		

		uncoverMessage(outPath, key)

		branch()
	elif select != "exit":
		print "+---------------------------------------------+"
		print "Please enter only hide, find, or exit!"
		print "+---------------------------------------------+"
		branch()

##Starts executing here
branch()
