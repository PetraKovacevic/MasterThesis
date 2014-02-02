import kivy
kivy.require('1.6.0')

#Imports
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import ReferenceListProperty
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.uix.scatter import Scatter

# I had problems with this widget because when I would add the black semi see through background the widget would behave weird and pop up at radnom positions
# I haven't figured out how to fix that, so I seperated the background and the message into two widgets.
# This is the message widget

class MessageClock(Scatter):
	angle = NumericProperty(00)
	message_center_x = NumericProperty()
	message_center_y = NumericProperty()
	message_pos = ReferenceListProperty()
	
	def __init__(self, **kwargs):
		super(MessageClock, self).__init__(**kwargs)
		print self.width, self.height
		
	def on_yes_button(self):
		print "Calling yes_button!!!!!!!!!!!!"
		#app = App.get_running_app().root
		
		print self.width, self.height
		
		is_root = True
		
		for child in self.parent.children:
			if child.id == "idForRemoving":
				print "There is an idForRemoving"
				child.stop_clock()
				is_root = False
		
		#if there is no widget with id == "idForRemoving" then we are in stage 3 and the stop_clock should be called directly to the parent!
		if is_root:
			print "I'm calling stop_clock in main"
			self.parent.stop_clock()
		
	def on_no_button(self):
		print "Calling no_button!!!!!!!!!!!!"
		#app = App.get_running_app().root
		
		is_root = True
		
		for child in self.parent.children:
			if child.id == "idForRemoving":
				child.resume_clock()
				is_root = False
				print "found it"
				
		#if there is no widget with id == "idForRemoving" then we are in stage 3 and the stop_clock should be called directly to the parent!
		if is_root:
			self.parent.resume_clock()
				
class MessageClockApp(App):
	def build(self):
		return MessageClock()
		
if __name__ == '__main__':
    MessageClockApp().run()