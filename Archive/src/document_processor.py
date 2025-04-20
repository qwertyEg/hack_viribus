import PyPDF2
import docx
import markdown
import re
from typing import Tuple, List, Dict
import magic
import requests
from io import BytesIO

class DocumentProcessor:
    def __init__(self):
        self.mime = magic.Magic(mime=True)

    def process_document(self, file_content: bytes, file_name: str) -> Tuple[str, List[str]]:
        """
        Обрабатывает документ и извлекает текст и формулы
        """
        mime_type = self.mime.from_buffer(file_content)
        
        if mime_type == 'application/pdf':
            return self._process_pdf(file_content)
        elif mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            return self._process_docx(file_content)
        elif mime_type == 'text/markdown' or file_name.endswith('.md'):
            return self._process_markdown(file_content)
        elif mime_type == 'text/plain' or file_name.endswith('.txt'):
            return self._process_txt(file_content)
        else:
            raise ValueError(f"Неподдерживаемый формат файла: {mime_type}")

    def _process_pdf(self, content: bytes) -> Tuple[str, List[str]]:
        """
        Обрабатывает PDF файл
        """
        pdf_file = BytesIO(content)
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        formulas = []
        
        for page in reader.pages:
            page_text = page.extract_text()
            # Ищем формулы в формате LaTeX
            latex_formulas = re.findall(r'\$\$(.*?)\$\$', page_text, re.DOTALL)
            formulas.extend(latex_formulas)
            # Удаляем формулы из текста
            text += re.sub(r'\$\$.*?\$\$', '', page_text, flags=re.DOTALL)
        
        return text.strip(), formulas

    def _process_docx(self, content: bytes) -> Tuple[str, List[str]]:
        """
        Обрабатывает DOCX файл
        """
        doc = docx.Document(BytesIO(content))
        text = ""
        formulas = []
        
        for paragraph in doc.paragraphs:
            para_text = paragraph.text
            # Ищем формулы в формате LaTeX
            latex_formulas = re.findall(r'\$\$(.*?)\$\$', para_text, re.DOTALL)
            formulas.extend(latex_formulas)
            # Удаляем формулы из текста
            text += re.sub(r'\$\$.*?\$\$', '', para_text, flags=re.DOTALL) + "\n"
        
        return text.strip(), formulas

    def _process_markdown(self, content: bytes) -> Tuple[str, List[str]]:
        """
        Обрабатывает Markdown файл
        """
        text = content.decode('utf-8')
        # Ищем формулы в формате LaTeX
        formulas = re.findall(r'\$\$(.*?)\$\$', text, re.DOTALL)
        # Удаляем формулы из текста
        text = re.sub(r'\$\$.*?\$\$', '', text, flags=re.DOTALL)
        return text.strip(), formulas

    def _process_txt(self, content: bytes) -> Tuple[str, List[str]]:
        """
        Обрабатывает текстовый файл
        """
        text = content.decode('utf-8')
        # Ищем формулы в формате LaTeX
        formulas = re.findall(r'\$\$(.*?)\$\$', text, re.DOTALL)
        # Удаляем формулы из текста
        text = re.sub(r'\$\$.*?\$\$', '', text, flags=re.DOTALL)
        return text.strip(), formulas 