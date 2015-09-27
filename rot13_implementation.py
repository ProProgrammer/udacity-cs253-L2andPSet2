ASCII_a = ord('a') # equals 97
ASCII_A = ord('A') # equals 65
ROTNum = 13 # requiredShift

def rot13(user_input):
	outputList = []
	if user_input:
		for i in user_input:
			if isLowerCaseChar(i):
				outputList.append(rotLowerCase(i, ROTNum))
			elif isUpperCaseChar(i):
				outputList.append(rotUpperCase(i, ROTNum))
			else:
				outputList.append(i)

	return ''.join(outputList)

def rotLowerCase(inputChar, requiredShift):
	outputASCII = (((ord(inputChar) - ASCII_a) + requiredShift) % 26) + ASCII_a
	return chr(outputASCII)

def rotUpperCase(inputChar, requiredShift):
	outputASCII = (((ord(inputChar) - ASCII_A) + requiredShift) % 26) + ASCII_A
	return chr(outputASCII)

def isUpperCaseChar(c):
	if ord(c) >= ord('A') and ord(c) <= ord('Z'):
		return True
	else:
		return False

def isLowerCaseChar(c):
	if ord(c) >= ord('a') and ord(c) <= ord('z'):
		return True
	else:
		return False

print rot13('deep SukhwaniZZZ')


"""
# Experimenting before finalizing function
for x in range(ord('a'), ord('z') + 1):
	print x, chr(x), (ord('z') + 13) % ord('z')

requiredRot = 13
for x in range(ord('a'), ord('z') + 1):	
	inputAscii = x
	outputAscii = x + requiredRot
	if (outputAscii > ord('z'))
	print x, chr(x), 'output:', chr(outputAscii)

for x in range(97, 123):
	outputValue = (((x - 97) + 13) % 26) + 65
	print x, chr(x), ':', outputValue, chr(outputValue)
inputAscii
outputAscii == inputAscii + 13
"""