from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from functools import partial
class FirstKivy(App):
    
    def disable(self, instance, *args):
        instance.disabled = True

    
    def update(self, instance, *args):
        instance.background_color = (255,0,0,53)
        instance.text = "Disabled"
        

    def build(self):
        mybtn = Button(text="Click me to disable", pos=(300,350), size_hint = (.25, .18))
        

        mybtn.bind(on_press=partial(self.disable, mybtn))

        mybtn.bind(on_press=partial(self.update, mybtn))

        return mybtn

FirstKivy().run()