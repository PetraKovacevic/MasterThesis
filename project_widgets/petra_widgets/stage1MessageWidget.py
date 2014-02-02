import kivy
kivy.require('1.6.0')

#Imports
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import NumericProperty
from selectionTransferWidget import SelectionTransferWidget

class Stage1MessageWidget(Widget):
		
	def ok_button(self):
				
		app = App.get_running_app().root
		#app.add_widget(SelectionTransferWidget(pos = (0, 0), id = '1'))
		app.call_selection1()
		print "Im in Stage1MessageWidget and I've pressed ok!"