import kivy
kivy.require('1.6.0')

#Imports
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from kivy.properties import NumericProperty

class MessageWidget(Widget):
	user = StringProperty()
	angle = NumericProperty()
	text = StringProperty()

	def __init__(self, **kwargs):
		# make sure we aren't overriding any important functionality
		super(MessageWidget, self).__init__(**kwargs)
	
	def stop_clock(self):
		self.parent.stop_clock()