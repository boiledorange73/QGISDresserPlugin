"""Plugin main class"""

# Copyright (C) 2025 Shinsuke Nakamori
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import os

import yaml
from PIL import Image
from qgis.PyQt.QtWidgets import QDialog, QMessageBox
from qgis.PyQt import uic
# log
from qgis.core import QgsMessageLog, Qgis

from qgis.PyQt.QtCore import QObject, QEvent, Qt, QRect
from qgis.PyQt.QtGui import QPainter, QColor, QPixmap
from qgis.PyQt.QtWidgets import QWidget

import math # ceil

from .qgd_props import QGISDresserProps

class BackgroundWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAutoFillBackground(False)

    def paintEvent(self, event):
        props = QGISDresserProps()
        # painter
        p = QPainter(self)
        # 1) 背景色
        # p.fillRect(self.rect(), self.bg_color)
        # 2) 画像
        if props.pixmap.isNull():
            return
        vw, vh = self.width(), self.height()
        iw, ih = props.pixmap.width(), props.pixmap.height()
        rw, rh = vw/iw, vh/ih # rate ... scale candidate
        # scale
        if props.main_scale == "fit_larger":
            sw = sh = rw if rw > rh else rh
        elif props.main_scale == "fit_smaller":
            sw = sh = rw if rw < rh else rh
        elif props.main_scale == "stretch":
            sw, sh = rw, rh
        elif props.main_scale == "shrink_larger":
            sc = rw if rw > rh else rh
            sw = sh = 1 if sc > 1 else sc
        elif props.main_scale == "shrink_smaller":
            sc = rw if rw < rh else rh
            sw = sh = 1 if sc > 1 else sc
        else: # none
            sw, sh = 1., 1.
        # drawing area (single)
        dw, dh = int(sw*iw), int(sh*ih)
        if not (dw >= 1 and dh >= 1):
            return
        # 横位置 (シングル画像左上隅)
        if "center" in props.main_position_x:
            # (x+dw/2) = vw/2
            x = int((vw-dw)/2)
        elif "right" in props.main_position_x:
            x =  vw - dw
        else: # "left"
            x = 0
        # 縦位置 (シングル画像左上隅)
        if "middle" in props.main_position_y:
            y = int((vh-dh)/2)
        elif "bottom" in props.main_position_y:
            y =  vh - dh
        else: # "top"
            y = 0
        # repeat
        main_repeat = props.main_repeat
        if main_repeat == "repeat" or main_repeat == "repeat-x" or main_repeat == "repeat-xy":
            x0 = x % dw
            if x0 > 0:
                x0 -= dw
            x1 = vw
        else:
            x0 = x
            x1 = x0 + 1
        if main_repeat == "repeat" or main_repeat == "repeat-y" or main_repeat == "repeat-xy":
            y0 = y % dw
            if y0 > 0:
                y0 -= dh
            y1 = vh
        else:
            y0 = y
            y1 = y0 + 1
        # draws
        tx = 0
        for x in range(x0, x1, dw):
            tx = tx + 1
            ty = 0
            for y in range(y0, y1, dh):
                ty = ty + 1
                p.drawPixmap(QRect(x, y, dw, dh), props.pixmap)

class MainWindowResizeFilter(QObject):
    def __init__(self, bg_widget):
        super().__init__()
        self.bg_widget = bg_widget

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Resize:
            self.bg_widget.setGeometry(obj.rect())
            self.bg_widget.lower()
            self.bg_widget.update()
        return False
