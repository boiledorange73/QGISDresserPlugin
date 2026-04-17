from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtGui import QPixmap
import os.path

class QGISDresserProps:
    PREFIX = "QGISDresser"
    _instance = None

    DEFAULTS = {
        "image_path": "",
        "image_scale": "fit_width",
        "image_repeat": "no-repeat",
        "anchor_h": "center",
        "anchor_v": "middle",
        # styles
        "text_color": "",
        "menubar_background": "",
        "treeview_background": "rgba(200, 200, 200, 0.6)",
        "main_background": "",
        "button_background": "rgba(255, 255, 255, 0)",
        "button_image": "transparent",
        "button_position": "center",
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_once()
        return cls._instance

    def __init__(self):
        pass

    def _init_once(self):
        self.settings = QSettings()
        self._apply_defaults()
        self._load()
        self._mk_pixmap()

    def _mk_pixmap(self):
        if os.path.isfile(self._image_path):
            self._pixmap = QPixmap(self._image_path)
        else:
            self._pixmap = QPixmap()

    def _apply_defaults(self):
        self._image_path = self.DEFAULTS["image_path"]
        self._image_scale = self.DEFAULTS["image_scale"]
        self._image_repeat = self.DEFAULTS["image_repeat"]
        self._anchor_h = self.DEFAULTS["anchor_h"]
        self._anchor_v = self.DEFAULTS["anchor_v"]
        self._text_color = self.DEFAULTS["text_color"]
        self._menubar_background = self.DEFAULTS["menubar_background"]
        self._treeview_background = self.DEFAULTS["treeview_background"]
        self._main_background = self.DEFAULTS["main_background"]
        self._button_background = self.DEFAULTS["button_background"]
        self._button_image = self.DEFAULTS["button_image"]
        self._button_position = self.DEFAULTS["button_position"]

    def _key(self, name):
        return f"{self.PREFIX}/{name}"

    def _load(self):
        self._image_path = str(self.settings.value(self._key("image_path"), self._image_path))
        self._image_scale = str(self.settings.value(self._key("image_scale"), self._image_scale))
        self._image_repeat = str(self.settings.value(self._key("image_repeat"), self._image_repeat))
        self._anchor_h = str(self.settings.value(self._key("anchor_h"), self._anchor_h))
        self._anchor_v = str(self.settings.value(self._key("anchor_v"), self._anchor_v))
        self._text_color = str(self.settings.value(self._key("text_color"), self._text_color))
        self._menubar_background = str(self.settings.value(self._key("menubar_background"), self._menubar_background))
        self._treeview_background = str(self.settings.value(self._key("treeview_background"), self._treeview_background))
        self._main_background = str(self.settings.value(self._key("main_background"), self._main_background))
        self._button_background = str(self.settings.value(self._key("button_background"), self._button_background))
        self._button_image = str(self.settings.value(self._key("button_image"), self._button_image))
        self._button_position = str(self.settings.value(self._key("button_position"), self._button_position))

    def _save(self, name, value):
        self.settings.setValue(self._key(name), value)

    def reload(self):
        self._load()
        self._mk_pixmap()

    def reset(self):
        self.image_path = self.DEFAULTS["image_path"]
        self.image_scale = self.DEFAULTS["image_scale"]
        self.image_repeat = self.DEFAULTS["image_repeat"]
        self.anchor_h = self.DEFAULTS["anchor_h"]
        self.anchor_v = self.DEFAULTS["anchor_v"]
        self.text_color = self.DEFAULTS["text_color"]
        self.menubar_background = self.DEFAULTS["menubar_background"]
        self.treeview_background = self.DEFAULTS["treeview_background"]
        self.main_background = self.DEFAULTS["main_background"]
        self.button_background = self.DEFAULTS["button_background"]
        self.button_image = self.DEFAULTS["button_image"]
        self.button_position = self.DEFAULTS["button_position"]
        self._mk_pixmap()
    # image_path
    @property
    def image_path(self):
        return self._image_path
    @image_path.setter
    def image_path(self, value):
        self._image_path = str(value)
        self._mk_pixmap()
        self._save("image_path", self._image_path)
    # image_scale
    @property
    def image_scale(self):
        return self._image_scale
    @image_scale.setter
    def image_scale(self, value):
        self._image_scale = str(value)
        self._save("image_scale", self._image_scale)
    # image_repeat
    @property
    def image_repeat(self):
        return self._image_repeat
    @image_repeat.setter
    def image_repeat(self, value):
        self._image_repeat = str(value)
        self._save("image_repeat", self._image_repeat)
    # anchor_h (horizontal)
    @property
    def anchor_h(self):
        return self._anchor_h
    @anchor_h.setter
    def anchor_h(self, value):
        self._anchor_h = str(value)
        self._save("anchor_h", self._anchor_h)
    # anchor_v (vertical)
    @property
    def anchor_v(self):
        return self._anchor_v
    @anchor_v.setter
    def anchor_v(self, value):
        self._anchor_v = str(value)
        self._save("anchor_v", self._anchor_v)
    # text_color (text color)
    @property
    def text_color(self):
        return self._text_color
    @text_color.setter
    def text_color(self, value):
        self._text_color = str(value)
        self._save("text_color", self._text_color)
    # menubar_background
    @property
    def menubar_background(self):
        return self._menubar_background
    @menubar_background.setter
    def menubar_background(self, value):
        self._menubar_background = str(value)
        self._save("menubar_background", self._menubar_background)
    # treeview_background
    @property
    def treeview_background(self):
        return self._treeview_background
    @treeview_background.setter
    def treeview_background(self, value):
        self._treeview_background = str(value)
        self._save("treeview_background", self._treeview_background)
    # main_background
    @property
    def main_background(self):
        return self._main_background
    @main_background.setter
    def main_background(self, value):
        self._main_background = str(value)
        self._save("main_background", self._main_background)
    # button_background
    @property
    def button_background(self):
        return self._button_background
    @button_background.setter
    def button_background(self, value):
        self._button_background = str(value)
        self._save("button_background", self._button_background)
    # button_image
    @property
    def button_image(self):
        return self._button_image
    @button_image.setter
    def button_image(self, value):
        self._button_image = str(value)
        self._save("button_image", self._button_image)
    # button_position
    @property
    def button_position(self):
        return self._button_position
    @button_position.setter
    def button_position(self, value):
        self._button_position = str(value)
        self._save("button_position", self._button_position)
    # pixmap ... not saved
    @property
    def pixmap(self):
        return self._pixmap
