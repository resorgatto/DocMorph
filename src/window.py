# window.py
#
# Copyright 2025 Suby
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk, Gio


@Gtk.Template(resource_path='/io/github/resorgatto/docmorph/window.ui')
class DocmorphWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'DocmorphWindow'

    label = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        open_action = Gio.SimpleAction(name='open_file')
        open_action.connect('activate', self.open_file)
        self.add_action(open_action)



    def open_file(self, action, _):
        self._native = Gtk.FileChooserNative(
        title="Open File",
        transient_for=self,
        action=Gtk.FileChooserAction.OPEN
        )
        self._native.connect('response', self.on_open_response)
        self._native.show()

    def on_open_response(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            self.open_file(dialog.get_file())

        self._native = None
