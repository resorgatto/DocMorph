# 📄 DocMorph

**DocMorph** é um conversor de documentos simples e elegante para o ambiente de trabalho GNOME. Construído com **Python** e **GTK4/Libadwaita**, ele aproveita o poder do **Pandoc** para fornecer uma conversão fluida entre vários formatos de documentos.

> O objetivo do DocMorph é oferecer uma interface limpa e amigável para um backend poderoso, tornando a conversão de documentos acessível a todos — sem precisar usar a linha de comando.

---

## ✨ Funcionalidades

- **Amplo Suporte a Formatos**  
  Converta entre vários formatos como:  
  `Markdown`, `HTML`, `DOCX`, `ODT`, `EPUB` e mais.

- **Conversão Completa de PDF**  
  - Converta arquivos PDF existentes para outros formatos editáveis.  
  - Crie documentos PDF de alta qualidade a partir de qualquer tipo de arquivo suportado.

- **Interface Moderna**  
  UI limpa e adaptável que se integra perfeitamente com o GNOME moderno.

- **Foco em Flatpak**  
  Projetado para ser distribuído via Flatpak para facilitar a instalação e segurança.

- **Fluxo de Trabalho Simples**  
  Basta selecionar um arquivo, escolher o formato de saída e salvar.

---

## ⚙️ Dependências

DocMorph depende das seguintes ferramentas externas:

- **[Pandoc](https://pandoc.org/)**  
  O motor principal de conversão de documentos.

- **[Poppler](https://poppler.freedesktop.org/)**  
  Utiliza o `pdftotext` para ler conteúdos de arquivos PDF.

- **[TeX Live](https://www.tug.org/texlive/)**  
  Requerido pelo Pandoc para gerar PDFs via `--pdf-engine`.

> Estas dependências são geridas automaticamente ao construir a aplicação como um Flatpak.

---

## 📦 Construção e Execução com Flatpak

### 1. Pré-requisitos

Certifique-se de que os seguintes pacotes estão instalados:

sudo apt install flatpak flatpak-builder
flatpak install org.gnome.Sdk//47


---

### 2. Construir a Aplicação

git clone https://github.com/resorgatto/DocMorph.git
cd DocMorph
flatpak-builder --force-clean build-dir io.github.resorgatto.docmorph.json


---

### 3. Instalar e Executar
# Instalar
flatpak-builder --user --install --force-clean build-dir io.github.resorgatto.docmorph.json

# Executar
flatpak run io.github.resorgatto.docmorph


---

## 🛠️ Desenvolvimento

A forma recomendada de desenvolver o DocMorph é utilizando o **GNOME Builder**, que detecta automaticamente o manifesto Flatpak e configura o ambiente de desenvolvimento completo.

> Basta abrir o diretório do projeto no GNOME Builder e começar a desenvolver!

---

## 📄 Licença

Este programa é software livre: você pode redistribuí-lo e/ou modificá-lo sob os termos da **Licença Pública Geral GNU (GPL)**, conforme publicada pela **Free Software Foundation**, seja a versão 3 ou qualquer versão posterior.

---
