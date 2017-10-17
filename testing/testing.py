import glob
import socket
import os
import sys

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
	
def load_plugins():
	print("Finding plugins...")
	mods = glob.glob("module_*.py")
	modList = []

	print("Loading plugins...")
	i = 0
	for mod in mods:
		mods[i] = mods[i].replace("module_", "")
		mods[i] = mods[i].replace(".py", "")
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
		self.trigger = plugin_get_trigger(name)
		self.about = plugin_get_about(name)
		self.help = plugin_get_help(name)

##############################################################		
# Begin plugin loading
##############################################################
modList = load_plugins()

###############################################################
# Begin test workload
###############################################################
errors = []
i = 0
for mod in modList:
	try:
		print(call_plugin(modList[i].name, ""))
	except Exception as e:
		errors.append("no arguments - " + str(e))

	try:
		print(call_plugin(modList[i].name, "5"))
	except Exception as e:
		errors.append("with arguments - " + str(e))

	try:
		print(plugin_get_trigger(modList[i].name))
	except Exception as e:
		errors.append("get trigger - " + str(e))		

	try:
		print(plugin_get_about(modList[i].name))
	except Exception as e:
		errors.append("get about - " + str(e))

	try:
		print(plugin_get_help(modList[i].name))
	except Exception as e:
		errors.append("get help - " + str(e))

print(errors)