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

class NameTagWidget(Widget):
    #name_label = StringProperty()
	user = StringProperty()
	color = ListProperty()
	angle = NumericProperty(0)

	def __init__(self, **kwargs):
		# make sure we aren't overriding any important functionality
		super(NameTagWidget, self).__init__(**kwargs)

class NameTagWidgetApp(App):
	def build(self):
		return NameTagWidget(user = "1", color = [1, 0, 0, 0.6])
		
if __name__ == '__main__':
    NameTagWidgetApp().run()