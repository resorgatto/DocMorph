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
import os
import datetime
import subprocess
import shutil
from pathlib import Path
from gi.repository import Adw, Gtk, Gio, GLib

@Gtk.Template(resource_path='/io/github/resorgatto/docmorph/window.ui')
class DocmorphWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'DocmorphWindow'

    toast_overlay = Gtk.Template.Child()
    selectconvert = Gtk.Template.Child()

    selected_file = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        open_action = Gio.SimpleAction(name='open_file')
        open_action.connect('activate', self.on_open_file_activated)
        self.add_action(open_action)

        convert_action = Gio.SimpleAction(name='convert')
        convert_action.connect('activate', self.on_convert_activated)
        self.add_action(convert_action)

    def on_open_file_activated(self, action, _):
        """Callback para abrir o diálogo de seleção de arquivo."""
        dialog = Gtk.FileDialog.new()
        dialog.set_title("Selecione um arquivo para converter")
        dialog.open(self, None, self.on_open_file_response)

    def on_open_file_response(self, dialog, result):
        """Processa a resposta do diálogo de seleção de arquivo."""
        try:
            file = dialog.open_finish(result)
            if file:
                self.selected_file = file
                print(f"Arquivo selecionado: {file.get_path()}")
        except GLib.Error as e:
            print(f"Seleção de arquivo cancelada ou falhou: {e.message}")
        except Exception as e:
            print(f"Erro inesperado ao abrir o arquivo: {e}")
            self.show_error_dialog("Erro ao Abrir Arquivo", f"Não foi possível abrir o arquivo selecionado.\n\nDetalhes: {e}")

    def on_convert_activated(self, action, param):
        """Callback para iniciar o processo de conversão."""
        if not self.selected_file:
            self.show_toast("Por favor, selecione um arquivo primeiro.")
            return

        dialog = Gtk.FileDialog.new()
        dialog.set_title("Salvar arquivo convertido")

        file_type = self.selectconvert.get_selected_item().get_string().lower()

        input_basename = Path(self.selected_file.get_basename()).stem
        dialog.set_initial_name(f"{input_basename}_convertido.{file_type}")

        dialog.save(self, None, self._on_save_dialog_response, file_type)

    def _on_save_dialog_response(self, dialog, result, file_type):
        """
        Chamado após o usuário escolher onde salvar.
        Inicia a conversão do arquivo.
        """
        try:
            output_file_gio = dialog.save_finish(result)
            if not output_file_gio:
                print("Operação de salvar cancelada pelo usuário.")
                return

            output_path = output_file_gio.get_path()
            input_path = self.selected_file.get_path()

            print(f"Iniciando conversão de '{input_path}' para '{output_path}'")

            if input_path.lower().endswith('.pdf'):
                self.convert_from_pdf(input_path, output_path)
            elif output_path.lower().endswith('.pdf'):
                self.convert_to_pdf(input_path, output_path)
            else:
                self.convert_standard(input_path, output_path)

            success_message = f"O seu documento foi convertido com sucesso!\n\nSalvo em: {output_path}"
            print(success_message)
            self.show_success_dialog("Conversão Concluída", success_message)

        except FileNotFoundError as e:
            error_message = f"Comando não encontrado: '{e.filename}'.\n\nVerifique se o Pandoc e/ou as ferramentas de PDF (poppler-utils) estão instalados e acessíveis no seu sistema."
            print(error_message)
            self.show_error_dialog("Dependência Faltando", error_message)

        except subprocess.CalledProcessError as e:
            error_details = e.stderr.encode('utf-8', errors='ignore') or e.stdout.decode('utf-8', errors='ignore') or "Nenhuma saída de erro detalhada."
            error_message = f"Ocorreu um erro durante a conversão.\n\nDetalhes do erro:\n{error_details}"
            print(error_message)
            self.show_error_dialog("Erro na Conversão", error_message)

        except GLib.Error as e:
            print(f"Operação de salvar cancelada ou falhou: {e.message}")

        except Exception as e:
            error_message = f"Ocorreu um erro inesperado: {e}"
            print(error_message)
            self.show_error_dialog("Erro Inesperado", error_message)

    def convert_from_pdf(self, input_path, output_path):
        """Converte um arquivo PDF para outro formato usando pdftotext + pandoc."""
        print("Detectado arquivo PDF de entrada. Usando 'pdftotext' como passo intermediário.")

        temp_dir = Path(GLib.get_tmp_dir())
        intermediate_txt_path = temp_dir / f"{Path(input_path).stem}_{datetime.datetime.now().timestamp()}.txt"

        try:
            subprocess.run(
                ["pdftotext", input_path, str(intermediate_txt_path)],
                check=True, capture_output=True, text=True, encoding='utf-8'
            )
            subprocess.run(
                ["pandoc", str(intermediate_txt_path), "-o", output_path],
                check=True, capture_output=True, text=True, encoding='utf-8'
            )
        finally:
            if intermediate_txt_path.exists():
                os.remove(intermediate_txt_path)

    def convert_to_pdf(self, input_path, output_path):
        """Converte um arquivo para PDF usando Pandoc, procurando dinamicamente pelo motor de PDF."""
        print("Detectado arquivo PDF de saída. Usando Pandoc com motor de PDF.")

        pdf_engine_path = shutil.which("pdflatex")

        if not pdf_engine_path:
            error_message = (
                "Motor de PDF (pdflatex) não foi encontrado.\n\n"
                "Verifique se a extensão 'org.freedesktop.Sdk.Extension.texlive' "
                "está corretamente definida no seu manifesto Flatpak."
            )
            self.show_error_dialog("Erro de Configuração", error_message)
            raise FileNotFoundError(error_message)

        print(f"Usando motor de PDF encontrado em: {pdf_engine_path}")
        subprocess.run(
            [
                "pandoc",
                input_path,
                "-o",
                output_path,
                f"--pdf-engine={pdf_engine_path}"
            ],
            check=True, capture_output=True
        )

    def convert_standard(self, input_path, output_path):
        """Realiza uma conversão padrão usando Pandoc."""
        subprocess.run(
            ["pandoc", input_path, "-o", output_path],
            check=True, capture_output=True
        )

    def show_toast(self, text):
        """Mostra uma notificação rápida (toast)."""
        if self.toast_overlay:
             self.toast_overlay.add_toast(Adw.Toast.new(text))
        else:
             print(f"TOAST: {text}")

    def show_success_dialog(self, title, message):
        """Mostra uma janela de diálogo de sucesso."""
        dialog = Adw.MessageDialog.new(self, title, message)
        dialog.add_response("ok", "OK")
        dialog.set_default_response("ok")
        dialog.connect("response", lambda d, r: d.close())
        dialog.present()

    def show_error_dialog(self, title, message):
        """Mostra uma janela de diálogo de erro."""
        dialog = Adw.MessageDialog.new(self, title, message)
        dialog.add_response("ok", "OK")
        dialog.set_default_response("ok")
        dialog.connect("response", lambda d, r: d.close())
        dialog.present()

