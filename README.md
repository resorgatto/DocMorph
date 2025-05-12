# Conversor de Arquivos

Este projeto é uma ferramenta de conversão de arquivos desenvolvida em Python usando GTK e Pandoc. Ele permite converter arquivos nos formatos PDF, DOCX e HTML de forma eficiente.

## Funcionalidades

- **Conversão de PDF:** Converta arquivos PDF para outros formatos suportados.
- **Conversão de DOCX:** Converta documentos Word (DOCX) para PDF ou HTML.
- **Conversão de HTML:** Converta páginas HTML em PDFs ou DOCX.
- **Interface Gráfica:** Interface intuitiva desenvolvida com GTK para facilitar o uso.

## Requisitos

Antes de executar o projeto, certifique-se de ter os seguintes requisitos instalados:

- Python 3.8+
- GTK 4
- Pandoc (para realizar as conversões de arquivo)

## Instalação

1. **Instale o Pandoc**:  
   Para instalar o Pandoc, siga as instruções específicas para o seu sistema operacional disponíveis [aqui](https://pandoc.org/installing.html).

2. **Instale o PyGObject** para GTK:

   ```bash
   pip install PyGObject
   ```

## Uso

1. Clone o repositório:

   ```bash
   git clone https://github.com/usuario/conversor-de-arquivos.git
   cd conversor-de-arquivos
   ```

2. Execute o aplicativo:

   ```bash
   python main.py
   ```

3. Utilize a interface para selecionar e converter seus arquivos. 🎉

### Exemplo de Uso com Pandoc

Para converter um arquivo DOCX para PDF usando Pandoc diretamente pela linha de comando, você pode executar:

```bash
pandoc input.docx -o output.pdf
```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a [GNU General Public License v3.0](LICENSE).

## Contato

Para mais informações, você pode entrar em contato pelo email: renatosorgatto@gmail.com
