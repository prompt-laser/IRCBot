from random import randint

def plugin_about():
	return "Returns a random number between 1 and 20."

def plugin_trigger():
	return "d20"

def plugin_help():
	return "Arguments: none	Example: @d20"
	
def plugin_main(input):
	bounds = [1, 20]
		
	try:
		return str(randint(int(bounds[0]),int(bounds[1])))
	except:
		return "The die rolled off the table."
