"""
UI screens and layouts
"""

from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class HomeScreen(Screen):
    """Home screen of the application"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        
        # Title
        title = Label(
            text="BIMMERAH Diagnostics",
            size_hint_y=0.2,
            bold=True,
            font_size="28sp"
        )
        layout.add_widget(title)
        
        # Button grid
        button_grid = GridLayout(cols=2, spacing=10, size_hint_y=0.6)
        
        btn_connect = Button(text="Connect Vehicle")
        btn_codes = Button(text="Read Codes")
        btn_clear = Button(text="Clear Codes")
        btn_settings = Button(text="Settings")
        
        button_grid.add_widget(btn_connect)
        button_grid.add_widget(btn_codes)
        button_grid.add_widget(btn_clear)
        button_grid.add_widget(btn_settings)
        
        layout.add_widget(button_grid)
        
        # Status bar
        status = Label(
            text="Status: Not Connected",
            size_hint_y=0.2,
            color=(1, 0.5, 0, 1)
        )
        layout.add_widget(status)
        
        self.add_widget(layout)
