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

class MessageViewingTurnWidget(Widget):
	user = StringProperty()
		
	def ok_button(self):
		#app = App.get_running_app().root
		#app = self.parent
		#app.ok_pressed()
		
		for child in self.parent.children:
			if child.id == "idForRemoving":
				child.ok_pressed()