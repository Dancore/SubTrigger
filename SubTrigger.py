import sublime, sublime_plugin

class MytestCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# self.view.insert(edit, 0, "Hello, World! ")
		self.view.run_command("show_panel", {"panel": "console"}) # "toggle": 0})
		# print self.view.file_name(), "is now the active view"

class SublimeOnSave(sublime_plugin.EventListener):
	def on_pre_save(self, view):    	
		print "on_pre_save"
		# view.run_command('mytest')
		view.run_command("run_multiple_commands", {"commands": [{"command": "show_panel", "args": {"panel": "console"}, "context": "window"}]})
		# print "filename is: "+str(view.file_name())  

	def on_post_save(self, view):    	
		print "on_post_save"
		# print "filename is: "+str(view.file_name())

	def on_activated(self, view):
		print "view activated"
		# view.run_command("run_multiple_commands")
		# view.run_command("mytest")

# Takes an array of commands (same as those you'd provide to a key binding) with
# an optional context (defaults to view commands) & runs each command in order.
# Valid contexts are 'text', 'window', and 'app' for running a TextCommand,
# WindowCommands, or ApplicationCommand respectively.
# 
# The run_multiple_commands.py has been developed by Nilium - see 
# http://www.sublimetext.com/forum/viewtopic.php?f=5&t=8677 for a discussion.
 
class RunMultipleCommandsCommand(sublime_plugin.TextCommand):
	def exec_command(self, command):
		if not 'command' in command:
			raise Exception('No command name provided.')

		args = None
		if 'args' in command:
			args = command['args']

		# default context is the view since it's easiest to get the other contexts
		# from the view
		context = self.view
		if 'context' in command:
			context_name = command['context']
			if context_name == 'window':
				context = context.window()
			elif context_name == 'app':
				context = sublime
			elif context_name == 'text':
				pass
			else:
				raise Exception('Invalid command context "'+context_name+'".')

		# skip args if not needed
		if args is None:
			context.run_command(command['command'])
			# uncomment the next line, if you want to add a delay to the execution
			# sublime.set_timeout( lambda: context.run_command(command['command']), 2000 )
		else:
			context.run_command(command['command'], args)
			# uncomment the next line, if you want to add a delay to the execution
			# sublime.set_timeout( lambda: context.run_command(command['command'], args), 2000 )

	def run(self, edit, commands = None):
		print "running multiple commands"
		if commands is None:
			return # not an error
		for command in commands:
			self.exec_command(command)
