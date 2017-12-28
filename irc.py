import glob
import socket
import importlib

def reload_plugin(name):
	mod = __import__("module_%s" % name)
	importlib.reload(mod)

def load_plugin(name):
	mod = __import__("module_%s" % name)
	return mod

def call_plugin(name, *args, **kwargs):
	plugin = load_plugin(name)
	return plugin.plugin_main(*args, **kwargs)
	
def plugin_get_trigger(name):
	plugin = load_plugin(name)
	return plugin.plugin_trigger()
	
def plugin_get_help(name):
	plugin = load_plugin(name)
	return plugin.plugin_help()
	
def plugin_get_about(name):
	plugin = load_plugin(name)
	return plugin.plugin_about()
	
def load_plugins(*args, **kwargs):
	print("Finding plugins...")
	mods = glob.glob("c:\\python\\module_*.py")
	modList = []

	print("Loading plugins...")
	i = 0
	for mod in mods:
		mods[i] = mods[i].replace("c:\\python\\module_", "")
		mods[i] = mods[i].replace(".py", "")
		if(kwargs.get('reload')):
			modList.append(Plugin(mods[i], reload=True))
		else:
			modList.append(Plugin(mods[i]))
		print("Loaded module " + modList[i].name + "...")
		i = i + 1
	print("Loaded " + str(i) + " plugins")
	return modList

class Plugin(object):
	name = ""
	trigger = ""
	about = ""
	help = ""
	
	def __init__(self, name):
		self.name = name
		if(kwargs.get('reload')):
			reload_plugin(name)
		self.trigger = plugin_get_trigger(name)
		self.about = plugin_get_about(name)
		self.help = plugin_get_help(name)

##############################################################		
# Begin plugin loading
##############################################################
modList = load_plugins()

###############################################################
# Begin IRC connection
###############################################################

HOSTNAME = 'chat.freenode.net'
PORT = 6667
BUFFER_SIZE = 1024
COMMAND_CHAR = command_character_string 		# "@"
CHANNEL = channel_string				# "#freenode"
USER = user_string					# "guest"
NICK = nick_string					# "guest"
REAL_NAME = real_name_string				# "this is my real name"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOSTNAME, PORT))

s.send(bytes("NICK " + NICK + "\r\n", "ASCII"))

print(s.recv(BUFFER_SIZE))

s.send(bytes("USER " + USER + " 0 * :" + REAL_NAME + "\r\n", "ASCII"))

print(s.recv(BUFFER_SIZE))

s.send(bytes("JOIN " + CHANNEL + "\r\n", "ASCII"))

#############################################################
# Begin main loop
#############################################################

while(True):
	message = s.recv(BUFFER_SIZE)
	message = str(message)
	if(message):
		print(message)
		if(message.split(":")[0].find("PING") != -1):
			s.send(bytes("PONG " + message.split()[1], "ASCII"))
		elif(message.find("PRIVMSG") != -1):
			segments = message.split(":")
			if(segments[2][0] == COMMAND_CHAR):
				command = segments[2].split()[0]
				if(command.find("\\r\\n'") != -1):
					command = command.replace("\\r\\n'", "")
				arguments = segments[2].replace(command, "")
				command = command.replace(COMMAND_CHAR, "")
				arguments = arguments.replace("\\r\\n'", "")
				arguments = arguments.strip()
				if arguments is None:
					arguments = ""
				
				if(command.lower().find("help") != -1):
					s.send(bytes("PRIVMSG " + CHANNEL + " :Here's a list of my loaded plugins\r\n", "ASCII"))
					for mod in modList:
						s.send(bytes("PRIVMSG " + CHANNEL + " :" + mod.name + " - " + mod.about + "\r\n", "ASCII"))
				elif(command.lower().find("reload") != -1):
					modList = load_plugins(reload=True)
				else:
					for mod in modList:
						if(mod.trigger == command.lower()):
							if(arguments == "help"):
								s.send(bytes("PRIVMSG " + CHANNEL + " :" + mod.help + "\r\n", "ASCII"))
							elif(arguments == "about"):
								s.send(bytes("PRIVMSG " + CHANNEL + " :" + mod.about + "\r\n", "ASCII"))
							else:
								print("Trying to execute command: " + command + " with arguments: " + arguments)
								try:
									s.send(bytes("PRIVMSG " + CHANNEL + " :" + call_plugin(mod.name, arguments) + "\r\n", "ASCII"))
								except Exception as e:
									s.send(bytes("PRIVMSG " + CHANNEL + " :Well, this is embarassing...\r\n", "ASCII"))
