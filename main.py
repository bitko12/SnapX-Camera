from datetime import datetime
import os

from kivy.app import App
from kivy.uix.camera import Camera
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.graphics import Color, Ellipse, Line, Rectangle, RoundedRectangle
from kivy.core.window import Window

Window.size = (360, 640)


class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        with layout.canvas.before:
            Color(0.03, 0.04, 0.08, 1)
            Rectangle(pos=(0, 0), size=Window.size)

        glow = Label(text='◉', font_size='100sp', color=(0.36, 0.72, 1, 0.85), pos_hint={'center_x': 0.5, 'center_y': 0.62})
        layout.add_widget(glow)

        title = Label(text='SnapX', font_size='34sp', bold=True, color=(1, 1, 1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.48})
        layout.add_widget(title)

        subtitle = Label(text='Capture the moment', font_size='16sp', color=(0.7, 0.75, 0.92, 1), pos_hint={'center_x': 0.5, 'center_y': 0.38})
        layout.add_widget(subtitle)

        self.logo = Label(text='📸', font_size='72sp', pos_hint={'center_x': 0.5, 'center_y': 0.58})
        self.logo.opacity = 0.0
        layout.add_widget(self.logo)

        start_btn = Button(
            text='Open Camera',
            size_hint=(None, None),
            size=(180, 52),
            pos_hint={'center_x': 0.5, 'center_y': 0.22},
            background_color=(0.19, 0.62, 1, 1),
        )
        start_btn.bind(on_press=self.go_to_camera)
        layout.add_widget(start_btn)

        self.add_widget(layout)

        self.animate_logo()

    def animate_logo(self):
        self.logo.opacity = 0
        anim = Animation(opacity=1, duration=0.8) + Animation(opacity=0.9, duration=0.5)
        anim.start(self.logo)

    def go_to_camera(self, instance):
        if self.manager is not None:
            self.manager.current = 'camera'


class ToolButton(Button):
    def __init__(self, icon, **kwargs):
        super().__init__(**kwargs)
        self.text = icon
        self.font_size = '18sp'
        self.size_hint = (None, None)
        self.size = (44, 44)
        self.background_color = (0, 0, 0, 0)
        self.bind(pos=self._draw, size=self._draw)
        self._draw()

    def _draw(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.18, 0.20, 0.28, 0.72)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[18, 18, 18, 18])
            Color(0.38, 0.72, 1, 0.22)
            RoundedRectangle(pos=(self.x, self.y + self.height * 0.45), size=(self.width, self.height * 0.55), radius=[18, 18, 18, 18])
            Color(1, 1, 1, 0.18)
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 18), width=1.1)


class CameraScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = BoxLayout(orientation='vertical')

        with root.canvas.before:
            Color(0.07, 0.08, 0.11, 1)
            Rectangle(pos=(0, 0), size=Window.size)

        header = BoxLayout(size_hint_y=0.1, padding=[20, 10], spacing=10)
        with header.canvas.before:
            Color(0.10, 0.11, 0.16, 1)
            Rectangle(pos=(0, 0), size=header.size)
        title = Label(
            text='SnapX Camera',
            font_size='22sp',
            bold=True,
            color=(0, 0.9, 1, 1),
            halign='left',
            text_size=self.size,
            valign='middle'
        )
        header.add_widget(title)
        root.add_widget(header)

        preview = RelativeLayout(size_hint_y=0.75, padding=10)
        self.camera = Camera(resolution=(640, 480), play=True)
        preview.add_widget(self.camera)
        root.add_widget(preview)

        controls = BoxLayout(size_hint_y=0.15, padding=[20, 15], spacing=20)
        with controls.canvas.before:
            Color(0.10, 0.11, 0.16, 1)
            Rectangle(pos=(0, 0), size=controls.size)

        gallery_btn = Button(
            text='Gallery',
            size_hint_x=0.25,
            background_normal='',
            background_color=(0.16, 0.18, 0.24, 1),
            color=(1, 1, 1, 1),
            bold=True
        )
        controls.add_widget(gallery_btn)

        self.capture_btn = Button(
            text='CAPTURE',
            size_hint_x=0.5,
            background_normal='',
            background_color=(0, 0.4, 1, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size='18sp'
        )
        self.capture_btn.bind(on_press=self.capture)
        controls.add_widget(self.capture_btn)

        filter_btn = Button(
            text='Filter',
            size_hint_x=0.25,
            background_normal='',
            background_color=(0.16, 0.18, 0.24, 1),
            color=(1, 1, 1, 1),
            bold=True
        )
        controls.add_widget(filter_btn)

        root.add_widget(controls)
        self.add_widget(root)

    def capture(self, instance=None):
        if instance is not None:
            anim = Animation(size=(72, 72), duration=0.08) + Animation(size=(82, 82), duration=0.08)
            anim.start(instance)

        folder = os.path.join(os.getcwd(), 'snapx_photos')
        os.makedirs(folder, exist_ok=True)
        file_name = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        path = os.path.join(folder, file_name)

        try:
            self.camera.export_to_png(path)
            print(f'SnapX: Photo saved at {path}')
        except Exception as e:
            print(f'SnapX: Camera capture failed: {e}')
            return

        if self.manager is not None and 'preview' in self.manager.screen_names:
            preview_screen = self.manager.get_screen('preview')
            preview_screen.show_image(path)
            self.manager.current = 'preview'


class PreviewScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        with self.layout.canvas.before:
            Color(0.08, 0.08, 0.12, 1)
            Rectangle(pos=(0, 0), size=Window.size)

        self.preview_panel = FloatLayout(size_hint=(0.82, 0.68), pos_hint={'center_x': 0.5, 'center_y': 0.62})
        with self.preview_panel.canvas.before:
            Color(0.14, 0.17, 0.24, 1)
            RoundedRectangle(pos=(0, 0), size=self.preview_panel.size, radius=[26, 26, 26, 26])

        self.image = Image(allow_stretch=True, keep_ratio=True, opacity=1)
        self.image.size_hint = (0.9, 0.8)
        self.image.pos_hint = {'center_x': 0.5, 'center_y': 0.55}
        self.preview_panel.add_widget(self.image)

        self.path_label = Label(
            text='Saved photo',
            color=(1, 1, 1, 0.8),
            font_size='13sp',
            halign='center',
            valign='middle',
            size_hint=(0.9, None),
            height=30,
            pos_hint={'center_x': 0.5, 'center_y': 0.18}
        )
        self.preview_panel.add_widget(self.path_label)
        self.layout.add_widget(self.preview_panel)

        back_btn = Button(
            text='← Back to Camera',
            size_hint=(None, None),
            size=(180, 46),
            pos_hint={'center_x': 0.5, 'y': 0.08},
            background_color=(0.2, 0.6, 1, 1)
        )
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def show_image(self, path):
        self.image.source = path
        self.image.reload()
        self.path_label.text = os.path.basename(path)

    def go_back(self, instance):
        if self.manager is not None:
            self.manager.current = 'camera'


class SnapXApp(App):
    def build(self):
        self.title = 'SnapX Camera'
        sm = ScreenManager()
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(CameraScreen(name='camera'))
        sm.add_widget(PreviewScreen(name='preview'))
        return sm


if __name__ == '__main__':
    SnapXApp().run()
