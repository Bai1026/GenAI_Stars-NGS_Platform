import fitz  # PyMuPDF
from elasticsearch import Elasticsearch
import logging

# 设置日志记录
logging.basicConfig(level=logging.DEBUG)

# 初始化Elasticsearch
# es = Elasticsearch([{'host': '172.17.0.2', 'port': 9200, 'scheme': 'http'}])
es = Elasticsearch(
    [{'host': '172.17.0.2', 'port': 9200, 'scheme': 'http'}],
    timeout=30,  # 设置超时时间为30秒
    max_retries=10,  # 设置最大重试次数
    retry_on_timeout=True  # 启用超时重试
)


# 确保Elasticsearch服务在运行
try:
    if not es.ping():
        raise ValueError("Connection failed")
except Exception as e:
    logging.error("Elasticsearch ping failed: %s", e)

# 创建索引
try:
    es.options(ignore_status=[400]).indices.create(index='knowledge_base')
except Exception as e:
    logging.error("Failed to create index: %s", e)

# 将PDF文件转换为文本
def pdf_to_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

pdf_paths = ['./pdf/paper.pdf']

for i, pdf_path in enumerate(pdf_paths):
    try:
        text = pdf_to_text(pdf_path)
        doc = {'content': text}
        es.index(index='knowledge_base', id=i, body=doc)
    except Exception as e:
        logging.error("Failed to index document: %s", e)

print("PDF files have been indexed.")
