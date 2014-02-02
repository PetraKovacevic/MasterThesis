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

class MessageCancelClockWidget(Widget):
	angle = NumericProperty(90)
	message_center_x = NumericProperty()
	message_center_y = NumericProperty()
	message_pos = ReferenceListProperty()
	
	def __init__(self, **kwargs):
		super(MessageCancelClockWidget, self).__init__(**kwargs)
		print self.width, self.height
		
	def on_yes_button(self):
		print "Calling yes_button!!!!!!!!!!!!"
		#app = App.get_running_app().root
		
		print self.width, self.height
		
		for child in self.parent.children:
			if child.id == "idForRemoving":
				child.stop_clock()
		
	def on_no_button(self):
		print "Calling yes_button!!!!!!!!!!!!"
		#app = App.get_running_app().root
		
		for child in self.parent.children:
			if child.id == "idForRemoving":
				child.resume_clock()
				
class MessageCancelClockWidgetApp(App):
	def build(self):
		return MessageCancelClockWidget()
		
if __name__ == '__main__':
    MessageCancelClockWidgetApp().run()