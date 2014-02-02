import kivy
kivy.require('1.6.0')

#Imports
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.uix.button import Button

class RotateButton(Button):
	user = NumericProperty()
	angle = NumericProperty()