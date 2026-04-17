"""Plugin dialog class"""

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

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog, QFileDialog, QColorDialog
from qgis.PyQt.QtCore import QCoreApplication, pyqtSignal

from .qgd_props import QGISDresserProps

class QGISDresserDialog(QDialog):
    applyRequested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.dialog = uic.loadUi(
            os.path.join(os.path.dirname(__file__), "plugin_dialog.ui"), self
        )
        if self.dialog is None:
            raise RuntimeError("Failed loading UI file.")
        self._presets = self._get_presets()
        self._init_widgets()
        self._connect_signals()
        self._init_values()

    def _init_widgets(self):
        self.cmbPresets.clear()
        self.cmbPresets.addItem("","")
        if self._presets is not None:
            for key in self._presets.keys():
                self.cmbPresets.addItem(key, key)
        self.cmbImageScale.clear()
        self.cmbImageScale.addItem(self.tr("None"), "none")
        self.cmbImageScale.addItem(self.tr("Fit (Smaller)"), "fit_smaller")
        self.cmbImageScale.addItem(self.tr("Fit (Larger)"), "fit_larger")
        self.cmbImageScale.addItem(self.tr("Shrink (Smaller)"), "shrink_smaller")
        self.cmbImageScale.addItem(self.tr("Shrink (Larger)"), "shrink_larger")
        self.cmbImageScale.addItem(self.tr("Stretch"), "stretch")
        self.cmbImageRepeat.clear()
        self.cmbImageRepeat.addItem(self.tr("None"), "no-repeat")
        self.cmbImageRepeat.addItem(self.tr("X"), "repeat-x")
        self.cmbImageRepeat.addItem(self.tr("Y"), "repeat-y")
        self.cmbImageRepeat.addItem(self.tr("X/Y"), "repeat")
        self.cmbAnchorH.clear()
        self.cmbAnchorH.addItem(self.tr("Left"), "left")
        self.cmbAnchorH.addItem(self.tr("Center"), "center")
        self.cmbAnchorH.addItem(self.tr("Right"), "right")
        self.cmbAnchorV.clear()
        self.cmbAnchorV.addItem(self.tr("Top"), "top")
        self.cmbAnchorV.addItem(self.tr("Middle"), "middle")
        self.cmbAnchorV.addItem(self.tr("Bottom"), "bottom")

    def _connect_signals(self):
        self.cmbPresets.currentIndexChanged.connect(self.on_preset)
        self.btnPresets.clicked.connect(self.on_preset)
        self.btnImagePath.clicked.connect(self.on_browse_image)
        self.btnTextColor.clicked.connect(
            lambda: self.select_color_for(self.txtTextColor)
        )
        self.btnMenubarBackground.clicked.connect(
            lambda: self.select_color_for(self.txtMenubarBackground)
        )
        self.btnTreeviewBackground.clicked.connect(
            lambda: self.select_color_for(self.txtTreeviewBackground)
        )
        self.btnMainBackground.clicked.connect(
            lambda: self.select_color_for(self.txtMainBackground)
        )
        self.btnButtonBackground.clicked.connect(
            lambda: self.select_color_for(self.txtButtonBackground)
        )
        self.btnOk.clicked.connect(self.on_ok)
        self.btnCancel.clicked.connect(self.dialog.reject)
        self.btnApply.clicked.connect(self.on_apply)
        self.cmbImageScale.currentTextChanged.connect(self.on_style_changed)
        self.cmbImageRepeat.currentTextChanged.connect(self.on_style_changed)
        self.cmbAnchorH.currentTextChanged.connect(self.on_style_changed)
        self.cmbAnchorV.currentTextChanged.connect(self.on_style_changed)

    def _init_values(self):
        prop = QGISDresserProps()
        self.txtImagePath.setText(prop.image_path)
        self._set_combo_data(self.cmbImageScale, prop.image_scale)
        self._set_combo_data(self.cmbImageRepeat, prop.image_repeat)
        self._set_combo_data(self.cmbAnchorH, prop.anchor_h)
        self._set_combo_data(self.cmbAnchorV, prop.anchor_v)
        self.txtTextColor.setText(prop.text_color)
        self.txtMainBackground.setText(prop.main_background)
        self.txtMenubarBackground.setText(prop.menubar_background)
        self.txtTreeviewBackground.setText(prop.treeview_background)
        self.txtButtonBackground.setText(prop.button_background)

    def _update_values(self, data):
        self.txtImagePath.setText(data["image_path"])
        self._set_combo_data(self.cmbImageScale, data["image_scale"])
        self._set_combo_data(self.cmbImageRepeat, data["image_repeat"])
        self._set_combo_data(self.cmbAnchorH, data["anchor_h"])
        self._set_combo_data(self.cmbAnchorV, data["anchor_v"])
        self.txtTextColor.setText(data["text_color"])
        self.txtMainBackground.setText(data["main_background"])
        self.txtMenubarBackground.setText(data["menubar_background"])
        self.txtTreeviewBackground.setText(data["treeview_background"])
        self.txtButtonBackground.setText(data["button_background"])

    def showEvent(self, event):
        super().showEvent(event)
        self.cmbPresets.setCurrentIndex(-1)


    def _set_combo_data(self, combo, value):
        index = combo.findData(value)
        if index != -1:
            combo.setCurrentIndex(index)

    def _get_combo_data(self, combo):
        data = combo.currentData()
        return data if data is not None else ""

    def tr(self, message):
        return QCoreApplication.translate("QGISDresserDialog", message)

    def on_preset(self):
        key = self._get_combo_data(self.cmbPresets)
        if not key in self._presets:
            return
        preset = self._presets[key]
        if preset is None:
            return
        self._update_values(preset)

    def on_browse_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self.dialog,
            self.tr("Choose an image"),
            "",
            self.tr("Images (*.png *.jpg *.jpeg *.bmp *.webp)")
        )
        if path:
            self.txtImagePath.setText(path)

    def select_color_for(self, line_edit):
        color = QColorDialog.getColor(parent=self.dialog)
        if color.isValid():
            line_edit.setText(color.name())  # 例: #ff0000

    def on_style_changed(self, _value):
        # コンボ変更時の処理
        # print("スタイル設定が変更されました")
        pass

    def on_apply(self):
        prop = QGISDresserProps()
        prop.image_path = self.txtImagePath.text()
        prop.image_scale = self._get_combo_data(self.cmbImageScale)
        prop.image_repeat = self._get_combo_data(self.cmbImageRepeat)
        prop.anchor_h = self._get_combo_data(self.cmbAnchorH)
        prop.anchor_v = self._get_combo_data(self.cmbAnchorV)
        prop.text_color = self.txtTextColor.text()
        prop.menubar_background = self.txtMenubarBackground.text()
        prop.treeview_background = self.txtTreeviewBackground.text()
        prop.main_background = self.txtMainBackground.text()
        prop.button_background = self.txtButtonBackground.text()
        self.applyRequested.emit()

    def on_ok(self):
        self.on_apply()
        self.dialog.accept()

    def collect_settings(self):
        return {
            "image_path": self.txtImagePath.text(),
            "image_scale": self.cmbImageScale.currentData(),
            "image_repeat": self.cmbImageRepeat.currentData(),
            "anchor_h": self.cmbAnchorH.currentData(),
            "anchor_v": self.cmbAnchorV.currentData(),
            "text_color": self.txtTextColor.text(),
            "menubar_background": self.txtMenubarBackground.text(),
            "treeview_background": self.txtTreeviewBackground.text(),
            "main_background": self.txtMainBackground.text(),
            "button_background": self.txtButtonBackground.text(),
        }
    #
    def _get_presets(self) -> dict:
        import json
        json_path = os.path.join(os.path.dirname(__file__), "preset", "list.json")
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        if data is None:
            return None
        # filenaem to full path
        for key in data.keys():
            style = data[key]
            if style is not None:
                for subkey in ("image_path", "button_image"):
                    if subkey in style and style[subkey] is not None and style[subkey] != "":
                        path = os.path.join(os.path.dirname(__file__), "preset", "images", style[subkey])
                        if os.path.isfile(path):
                            style[subkey] = path
        return data
