# # %% [markdown]
# # # 一.数据源集成实现

# # %% [markdown]
# # 1.1 财报格式解析

# # %%
# import pdfplumber
# import pandas as pd

# class PDFParseError(Exception):
#     """Custom exception for PDF parsing errors."""
#     pass

# class PDFParser:
#     def __init__(self):
#         self.table_settings = {
#             "vertical_strategy": "text", 
#             "horizontal_strategy": "text",
#             "keep_blank_chars": True,
#             "snap_tolerance": 4
#         }

#     def extract_tables(self, file_path, page_range=None):
#         """
#         支持多页表格的连续解析
#         参数：
#             page_range: 指定页码范围，例如 (0,3) 表示前3页
#         返回：
#             List[DataFrame] 表格列表
#         """
#         tables = []
#         try:
#             with pdfplumber.open(file_path) as pdf:
#                 total_pages = len(pdf.pages)
#                 start, end = 0, total_pages-1
#                 if page_range:
#                     start = max(0, page_range[0])
#                     end = min(total_pages-1, page_range[1])
                
#                 for i in range(start, end+1):
#                     page = pdf.pages[i]
#                     # 优化表格识别参数
#                     table = page.extract_table(self.table_settings)
#                     if table:
#                         # 处理跨页表格头重复问题
#                         if i > start and self._is_header_duplicate(tables[-1], table):
#                             table = table[1:]
#                         df = pd.DataFrame(table[1:], columns=table[0])
#                         tables.append(df)
#         except Exception as e:
#             print(f"PDF解析失败:{str(e)}")
#             raise PDFParseError("PDF解析异常") from e
#         return tables

#     def _is_header_duplicate(self, prev_df, current_table):
#         """检测表格头是否重复"""
#         return list(prev_df.columns) == current_table[0]

# # %%
# import pandas as pd
# from openpyxl import load_workbook

# class ExcelParseError(Exception):
#     """Custom exception for Excel parsing errors."""
#     pass

# class ExcelParser:
#     def parse_sheets(self, file_path, sheet_names=None):
#         """
#         参数：
#             sheet_names: 指定需要解析的工作表名称列表
#         返回：
#             Dict[str: DataFrame] 工作表字典
#         """
#         try:
#             # 预加载元数据
#             wb = load_workbook(file_path, read_only=True)
#             valid_sheets = sheet_names if sheet_names else wb.sheetnames
            
#             # 读取数据
#             dfs = {}
#             for sheet in valid_sheets:
#                 df = pd.read_excel(
#                     file_path,
#                     sheet_name=sheet,
#                     engine="openpyxl",
#                     na_values=['NA', 'N/A'],
#                     dtype={'股票代码': str}  # 处理数字代码前导零问题
#                 )
#                 dfs[sheet] = self._clean_data(df)
#             return dfs
#         except Exception as e:
#             print(f"Excel解析失败：{str(e)}")
#             raise ExcelParseError("Excel解析异常") from e

#     def _clean_data(self, df):
#         """数据清洗"""
#         # 去除全空行列
#         df = df.dropna(how='all').T.dropna(how='all').T
#         # 处理合并单元格
#         df = df.ffill(axis=0)
#         return df

# # %%


# from bs4 import BeautifulSoup
# import pandas as pd
# import re

# class HTMLParseError(Exception):
#     """Custom exception for HTML parsing errors."""
#     pass

# class HTMLParser:
#     def extract_data(self, file_path, table_css=None):
#         """
#         参数：
#             table_css: CSS选择器（默认解析所有table标签）
#         返回：
#             List[DataFrame] 表格列表
#         """
#         try:
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 soup = BeautifulSoup(f, 'html.parser')
            
#             tables = soup.select(table_css) if table_css else soup.find_all('table')
#             dfs = []
#             for table in tables:
#                 # 转换嵌套表格结构
#                 df = self._convert_html_table(table)
#                 if not df.empty:
#                     dfs.append(df)
#             return dfs
#         except Exception as e:
#             print(f"HTML解析失败：{str(e)}")
#             raise HTMLParseError("HTML解析异常") from e

#     def _convert_html_table(self, table):
#         """处理复杂表格结构"""
#         rows = []
#         for tr in table.find_all('tr'):
#             cells = []
#             for td in tr.find_all(['th', 'td']):
#                 # 处理跨行列
#                 rowspan = int(td.get('rowspan', 1))
#                 colspan = int(td.get('colspan', 1))
#                 cells.append({
#                     'text': re.sub(r'\s+', ' ', td.text).strip(),
#                     'rowspan': rowspan,
#                     'colspan': colspan
#                 })
#             rows.append(cells)
        
#         # 构建二维表格结构
#         matrix = self._build_matrix(rows)
#         return pd.DataFrame(matrix[1:], columns=matrix[0])

#     def _build_matrix(self, rows):
#         """处理行列合并"""
#         # 实现动态矩阵构建逻辑（此处省略具体实现）
#         # 返回二维数组

# # %%
# class FinancialReportParser:
#     def __init__(self):
#         # 初始化解析器
#         pass

#     def parse(self, file_path):
#         file_type = self._detect_file_type(file_path)
#         # 根据文件类型调用不同的解析方法
#         if file_type == 'pdf':
#             return self.pdf_parser.extract_tables(file_path)
#         elif file_type == 'excel':
#             return self.excel_parser.parse_sheets(file_path)
#         elif file_type == 'html':
#             return self.html_parser.extract_data(file_path)

#     def _detect_file_type(self, file_path):
#         # 通过文件扩展名或其他方式来判断文件类型
#         if file_path.endswith('.pdf'):
#             return 'pdf'
#         elif file_path.endswith('.xls') or file_path.endswith('.xlsx'):
#             return 'excel'
#         elif file_path.endswith('.html'):
#             return 'html'
#         else:
#             return 'unknown'


# # %% [markdown]
# # 1.1.2 数据标准化处理

# # %%
# import datetime

# class FinancialDataNormalizer:
#     def __init__(self, field_mapping=None, unit_conversion=None, time_format="%Y-%m-%d %H:%M:%S"):
#         """
#         初始化数据标准化处理器

#         :param field_mapping: 字段映射字典，例如 {"原始字段名": "标准字段名"}
#         :param unit_conversion: 单位转换字典，例如 {"美元": 1, "欧元": 1.1}，
#                                 用于将不同币种或数值单位转换到统一的标准单位
#         :param time_format: 原始时间字符串的格式，用于时间格式化
#         """
#         self.field_mapping = field_mapping or {}
#         self.unit_conversion = unit_conversion or {}
#         self.time_format = time_format

#     def normalize(self, raw_data):
#         """
#         对原始数据进行标准化处理：
#         1. 字段映射标准化
#         2. 数值单位统一
#         3. 时间序列对齐
#         4. 数据质量检查

#         :param raw_data: 原始数据字典
#         :return: 标准化后的数据字典
#         """
#         # 1. 字段映射标准化
#         mapped_data = self._map_to_standard_fields(raw_data)
        
#         # 2. 数值单位统一
#         unified_data = self._unify_units(mapped_data)
        
#         # 3. 时间序列对齐
#         aligned_data = self._align_time_series(unified_data)
        
#         # 4. 数据质量检查
#         validated_data = self._validate_data(aligned_data)
        
#         return validated_data

#     def _map_to_standard_fields(self, raw_data):
#         """
#         将原始数据字段映射到标准字段。

#         :param raw_data: 原始数据字典
#         :return: 字段名称已映射为标准名称的新数据字典
#         """
#         mapped_data = {}
#         for key, value in raw_data.items():
#             std_key = self.field_mapping.get(key, key)
#             mapped_data[std_key] = value
#         return mapped_data

#     def _unify_units(self, data):
#         """
#         统一数值单位，比如将不同币种或计量单位转换为标准单位。
#         假设相关数值数据以元组形式出现：(amount, unit)

#         :param data: 数据字典
#         :return: 数值统一后的数据字典
#         """
#         for key, value in data.items():
#             if isinstance(value, tuple) and len(value) == 2:
#                 amount, unit = value
#                 conversion_factor = self.unit_conversion.get(unit, 1)
#                 data[key] = amount * conversion_factor
#         return data

#     def _align_time_series(self, data):
#         """
#         对时间数据进行格式化处理，确保时间序列的一致性。
#         假设时间字段的标准名称为 "timestamp"

#         :param data: 数据字典
#         :return: 时间格式统一后的数据字典
#         """
#         if "timestamp" in data:
#             try:
#                 data["timestamp"] = datetime.datetime.strptime(data["timestamp"], self.time_format)
#             except Exception as e:
#                 print(f"时间转换错误: {e}")
#                 data["timestamp"] = None
#         return data

#     def _validate_data(self, data):
#         """
#         进行数据质量检查，例如关键字段是否存在、数值是否合理等。
#         此处以检查 "amount" 字段为例，判断其是否为正值。

#         :param data: 数据字典
#         :return: 增加数据有效性标记后的数据字典
#         """
#         is_valid = True
#         if "amount" in data:
#             if data["amount"] is None or data["amount"] <= 0:
#                 is_valid = False
        
#         # 你可以在此处添加更多的校验逻辑
#         data["is_valid"] = is_valid
#         return data


# # %% [markdown]
# # # 1.1.3提关键词

# # %%
# import jieba
# import jieba.analyse
# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# import string

# # 下载 nltk 需要的资源（如果未安装，请先运行一次）
# # nltk.download('punkt')
# # nltk.download('stopwords')

# class ExchangeRateRiskKeywordsExtractor:
#     def __init__(self, topK=10, stop_words_file=None):
#         """
#         初始化关键词提取器，支持中英文
        
#         :param topK: 提取的关键词数量
#         :param stop_words_file: 可选的中文停用词文件路径
#         """
#         self.topK = topK
#         # 设置中文停用词
#         if stop_words_file:
#             jieba.analyse.set_stop_words(stop_words_file)
#         # 获取英文停用词表
#         self.english_stopwords = set(stopwords.words('english'))
    
#     def extract_keywords(self, risk_text):
#         """
#         从混合的中英文汇率风险文本中提取关键词
#         """
#         # 1. 提取中文关键词
#         cn_keywords = jieba.analyse.extract_tags(risk_text, topK=self.topK, withWeight=False)

#         # 2. 提取英文关键词
#         en_keywords = self.extract_english_keywords(risk_text)

#         # 3. 合并中英文关键词
#         combined_keywords = list(set(cn_keywords + en_keywords))

#         return combined_keywords

#     def extract_english_keywords(self, text):
#         """
#         提取英文关键词（去除停用词、标点，并转换为小写）
#         """
#         words = word_tokenize(text)  # 分词
#         filtered_words = [
#             word.lower() for word in words
#             if word.isalnum() and word.lower() not in self.english_stopwords
#         ]
#         return filtered_words

# # %% [markdown]
# # # 2.RAG系统

# # %% [markdown]
# # 2.1.1新闻文档分块

# # %

# import spacy
# from spacy.tokens import Doc
# from typing import List, Dict
# import numpy as np
# from sentence_transformers import SentenceTransformer

# class NewsChunker:
#     def __init__(self):
#         # 加载多语言模型
#         self.nlp = spacy.load('xx_ent_wiki_sm')  # 多语言模型
#         self.min_chunk_size = 100  # 最小分块字符数
#         self.max_chunk_size = 500  # 最大分块字符数
#         self.paragraph_sep = ["\n\n", "。", "！", "？", ".", "!", "?"]  # 中英文段落分隔符
#         self.exchange_rate_markers = ["汇率", "exchange rate", "USD/CNY", "EUR/USD", "JPY/CNY", "美元/人民币"]  # 汇率关键词
#         self.embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
#     def chunk_news(self, news_text):
#         """主分块方法"""
#         doc = self.nlp(news_text)
#         semantic_paragraphs = self._get_semantic_paragraphs(doc)
        
#         chunks = []
#         current_chunk = []
#         current_size = 0
        
#         for para in semantic_paragraphs:
#             para_len = len(para)
            
#             # 处理超长段落的分割
#             if para_len > self.max_chunk_size:
#                 sub_paragraphs = self._split_long_paragraph(para)
#                 for sub_para in sub_paragraphs:
#                     chunks.extend(self._process_paragraph(sub_para))
#                 continue
                
#             # 动态合并逻辑
#             if self._should_start_new_chunk(current_size, para_len):
#                 if current_chunk:
#                     chunks.append(self._create_chunk(current_chunk))
#                 current_chunk = [para]
#                 current_size = para_len
#             else:
#                 current_chunk.append(para)
#                 current_size += para_len
                
#         # 处理最后一个块
#         if current_chunk:
#             chunks.append(self._create_chunk(current_chunk))
            
#         return chunks

#     def _get_semantic_paragraphs(self, doc):
#         """语义段落识别"""
#         paragraphs = []
#         current_para = []
        
#         for sent in doc.sents:
#             # 检测段落分隔符
#             if self._is_paragraph_boundary(sent):
#                 if current_para:
#                     paragraphs.append("".join(current_para))
#                     current_para = []
#                 continue
                
#             current_para.append(sent.text)
            
#             # 基于依存关系的段落分割
#             if self._has_discourse_marker(sent):
#                 paragraphs.append("".join(current_para))
#                 current_para = []
        
#         # 处理最后一个段落
#         if current_para:
#             paragraphs.append("".join(current_para))
            
#         return paragraphs

#     def _is_paragraph_boundary(self, sent):
#         """检测显式段落分隔符"""
#         return any(sep in sent.text for sep in self.paragraph_sep)

#     def _has_discourse_marker(self, sent):
#         """检测语篇标记词（转折、因果等连接词）"""
#         markers = ["然而", "因此", "同时", "另一方面", "尽管如此", "however", "therefore", "meanwhile", "on the other hand"]
#         for token in sent:
#             if token.text in markers and token.dep_ == "mark":
#                 return True
#         return False

#     def _should_start_new_chunk(self, current_size, new_para_size):
#         """动态分块决策逻辑"""
#         # 强制分块条件
#         if current_size + new_para_size > self.max_chunk_size:
#             return True
#         # 语义完整性保护：不合并包含不同实体的段落
#         if current_size > self.min_chunk_size and new_para_size > self.min_chunk_size:
#             return True
#         return False

#     def _split_long_paragraph(self, paragraph):
#         """处理超长段落的分割"""
#         doc = self.nlp(paragraph)
#         split_points = []
        
#         # 寻找自然分割点
#         for sent in doc.sents:
#             if len(sent) > 50:  # 长句子优先作为分割点
#                 split_points.append(sent.end)
        
#         # 动态生成子段落
#         sub_paragraphs = []
#         start = 0
#         for end in split_points:
#             sub_para = doc[start:end].text
#             if len(sub_para) > self.min_chunk_size:
#                 sub_paragraphs.append(sub_para)
#                 start = end
#         # 处理剩余部分
#         if start < len(doc):
#             sub_paragraphs.append(doc[start:].text)
            
#         return sub_paragraphs

#     def _create_chunk(self, paragraphs):
#         """创建最终分块"""
#         chunk_text = "\n".join(paragraphs)
#         return {
#             "text": chunk_text,
#             "length": len(chunk_text),
#             "paragraph_count": len(paragraphs),
#             "entities": self._extract_entities(chunk_text)
#         }

#     def _extract_entities(self, text):
#         """提取金融实体信息"""
#         doc = self.nlp(text)
#         entities = []
        
#         for ent in doc.ents:
#             # 提取机构、货币、日期等实体
#             if ent.label_ in ["ORG", "MONEY", "DATE", "GPE"]:
#                 entities.append({
#                     "text": ent.text,
#                     "label": ent.label_,
#                     "start": ent.start_char,
#                     "end": ent.end_char
#                 })
#             # 提取汇率相关实体（如USD/CNY）
#             if ent.label_ == "MONEY" and "/" in ent.text:
#                 entities.append({
#                     "text": ent.text,
#                     "label": "EXCHANGE_RATE",
#                     "start": ent.start_char,
#                     "end": ent.end_char
#                 })
        
#         return entities
#     def vectorize_text(self, chunks: List[Dict]) -> np.ndarray:
#         """将文本分块向量化"""
#         texts = [chunk["text"] for chunk in chunks]
#         return self.embedding_model.encode(texts)

# # %% [markdown]
# # 2.1.2数据分块

# # %%


# import pandas as pd
# import numpy as np
# from sentence_transformers import SentenceTransformer
# from typing import List, Dict, Union

# class DataChunker:
#     def __init__(self, 
#                  window_size: int = 7,
#                  vectorization_method: str = "statistical",
#                  text_template: str = "日期范围：{start_date}至{end_date}，{column}平均值为{mean:.2f}，标准差为{std:.2f}"):
#         """
#         结构化数据分块与向量化处理器
        
#         :param window_size: 时间窗口大小（适用于时间序列）
#         :param vectorization_method: 向量化方法 ["statistical", "text_embedding"]
#         :param text_template: 文本描述模板（用于text_embedding模式）
#         """
#         self.window_size = window_size
#         self.vectorization_method = vectorization_method
#         self.text_template = text_template
        
#         # 加载多语言文本嵌入模型（用于text_embedding模式）
#         if vectorization_method == "text_embedding":
#             self.embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

#     def chunk_data(self, 
#                  df: pd.DataFrame,
#                  timestamp_col: str = "date") -> List[Dict]:
#         """
#         数据分块方法
        
#         :param df: 输入数据框
#         :param timestamp_col: 时间戳列名
#         :return: 分块列表，每个分块包含数据和元数据
#         """
#         chunks = []
        
#         # 确保时间戳列为datetime类型
#         df[timestamp_col] = pd.to_datetime(df[timestamp_col])
        
#         # 按时间窗口分块
#         start_date = df[timestamp_col].min()
#         end_date = start_date + pd.Timedelta(days=self.window_size)
        
#         while start_date < df[timestamp_col].max():
#             chunk_df = df[(df[timestamp_col] >= start_date) & (df[timestamp_col] < end_date)]
            
#             # 计算元数据
#             metadata = {
#                 "start_date": start_date,
#                 "end_date": end_date,
#                 "columns": chunk_df.columns.tolist(),
#                 "row_count": len(chunk_df)
#             }
            
#             chunks.append({
#                 "data": chunk_df,
#                 "metadata": metadata
#             })
            
#             # 更新时间窗口
#             start_date = end_date
#             end_date = start_date + pd.Timedelta(days=self.window_size)
        
#         return chunks

#     def vectorize(self, 
#                  chunks: List[Dict],
#                  target_columns: List[str] = ["USD/CNY"]) -> np.ndarray:
#         """
#         数据向量化方法
        
#         :param chunks: 分块列表
#         :param target_columns: 需要处理的数值列
#         :return: 向量数组 (n_chunks, n_features)
#         """
#         vectors = []
        
#         for chunk in chunks:
#             df = chunk["data"]
#             metadata = chunk["metadata"]
            
#             if self.vectorization_method == "statistical":
#                 # 统计特征向量化
#                 vec = []
#                 for col in target_columns:
#                     vec.extend([
#                         df[col].mean(),    # 均值
#                         df[col].std(),     # 标准差
#                         df[col].max(),     # 最大值
#                         df[col].min(),     # 最小值
#                         df[col].diff().mean()  # 趋势
#                     ])
#                 vectors.append(vec)
                
#             elif self.vectorization_method == "text_embedding":
#                 # 生成文本描述后向量化
#                 descriptions = []
#                 for col in target_columns:
#                     desc = self.text_template.format(
#                         start_date=metadata["start_date"],
#                         end_date=metadata["end_date"],
#                         column=col,
#                         mean=df[col].mean(),
#                         std=df[col].std()
#                     )
#                     descriptions.append(desc)
                
#                 # 拼接所有列的描述
#                 full_text = "。".join(descriptions)
#                 vec = self.embedding_model.encode([full_text])[0].tolist()
#                 vectors.append(vec)
                
#         return np.array(vectors)

#     def get_chunk_descriptions(self,
#                               chunks: List[Dict],
#                               target_columns: List[str] = ["USD/CNY"]) -> List[str]:
#         """
#         生成分块文本描述（用于与文本分块统一检索）
        
#         :return: 文本描述列表
#         """
#         descriptions = []
#         for chunk in chunks:
#             df = chunk["data"]
#             metadata = chunk["metadata"]
            
#             descs = []
#             for col in target_columns:
#                 desc = self.text_template.format(
#                     start_date=metadata["start_date"],
#                     end_date=metadata["end_date"],
#                     column=col,
#                     mean=df[col].mean(),
#                     std=df[col].std()
#                 )
#                 descs.append(desc)
            
#             descriptions.append("。".join(descs))
        
#         return descriptions

#     def hybrid_retrieve(self,
#                        text_vectors: np.ndarray,
#                        data_vectors: np.ndarray,
#                        query: str,
#                        top_k: int = 3,
#                        alpha: float = 0.5) -> List[int]:
#         """
#         混合检索方法（文本与数据）
        
#         :param text_vectors: 文本分块向量
#         :param data_vectors: 数据分块向量
#         :param query: 查询文本
#         :param top_k: 返回结果数量
#         :param alpha: 文本权重 (0-1)
#         :return: 相关分块索引列表
#         """
#         # 查询向量化
#         query_vec = self.embedding_model.encode([query])[0]
        
#         # 计算相似度
#         text_sim = np.dot(text_vectors, query_vec)
#         data_sim = np.dot(data_vectors, query_vec)
        
#         # 混合相似度
#         combined_sim = alpha * text_sim + (1 - alpha) * data_sim
        
#         # 获取Top-K索引
#         sorted_indices = np.argsort(combined_sim)[::-1]
#         return sorted_indices[:top_k]

# # %% [markdown]
# # 2.1.3 构建混合索引

# # %%

# import faiss
# import numpy as np

# class HybridIndexer:
#     def __init__(self):
#         self.index = None
#         self.chunks = []  # 存储所有分块的元数据

#     def build_index(self, text_chunks: List[Dict], data_chunks: List[Dict]):
#         # 合并文本和数据分块
#         all_chunks = text_chunks + data_chunks
#         self.chunks = all_chunks
        
#         # 提取所有嵌入向量
#         embeddings = []
#         for chunk in all_chunks:
#             embeddings.append(chunk["embedding"])
#         embeddings = np.array(embeddings).astype('float32')
        
#         # 创建FAISS索引
#         dimension = embeddings.shape[1]
#         self.index = faiss.IndexFlatL2(dimension)
#         self.index.add(embeddings)

#     def search(self, query: str, top_k: int = 5) -> List[Dict]:
#         # 查询向量化
#         query_embedding = self.embedding_model.encode([query])[0]
        
#         # FAISS检索
#         distances, indices = self.index.search(
#             np.array([query_embedding]).astype('float32'), 
#             top_k
#         )
        
#         # 返回结果分块
#         return [self.chunks[i] for i in indices[0]]

# %% [markdown]
# RAG

# %%
import numpy as np
import pandas as pd
from typing import List, Dict, Any
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document

class CrossModalRAGSystem:
    def __init__(self, openai_api_key: str):
        """
        处理文本和数值的RAG系统
        """
        # OpenAI嵌入和语言模型
        self.text_embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(temperature=0.1)
        
        # 数值数据存储
        self.numeric_data = None
        
        # 文本向量数据库
        self.text_vectorstore = None

    def _numeric_feature_engineering(self, df: pd.DataFrame) -> np.ndarray:
        """
        数值特征工程
        将数值特征映射到低维语义空间
        """
        # 选择关键特征，根据实际数据修改
        features = df[['exchange_rate', 'inflation_rate', 'economic_indicator']].values  #根据实际数据修改
        
        # 标准化
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)
        
        return scaled_features
# 数值数据和文本数据不好融合，因此把数值数据变为文本数据
    def _create_semantic_description(self, row: pd.Series) -> str:
        """
        为数值数据创建语义描述
        """
        return (
            f"金融数据报告：\n"
            f"汇率为 {row['exchange_rate']} 时，"
            f"通胀率为 {row['inflation_rate']}%，"
            f"经济指标为 {row['economic_indicator']}。"
            f"这表明当前经济环境较为 {'稳定' if row['economic_indicator'] > 100 else '波动'}。"
        )

    def load_data(self, 
                  text_documents: List[Document], 
                  numeric_dataframe: pd.DataFrame):
        """
        加载文本和数值数据
        """
        # 存储原始数值数据
        self.numeric_data = numeric_dataframe
        
        # 数值特征工程
        numeric_features = self._numeric_feature_engineering(numeric_dataframe)
        
        # 为数值数据创建语义描述
        numeric_docs = []
        for (_, row), feature_vec in zip(numeric_dataframe.iterrows(), numeric_features):
            semantic_desc = self._create_semantic_description(row)
            doc = Document(
                page_content=semantic_desc,
                metadata={
                    'exchange_rate': row['exchange_rate'],
                    'numeric_features': feature_vec.tolist()
                }
            )
            numeric_docs.append(doc)
        
        # 合并文本和数值文档
        all_documents = text_documents + numeric_docs
        
        # 创建向量数据库
        self.text_vectorstore = Chroma.from_documents(
            documents=all_documents, 
            embedding=self.text_embeddings
        )

    def advanced_retrieval(self, query: str, top_k: int = 3):
        """
        高级跨模态检索
        """
        # 文本嵌入
        query_embedding = self.text_embeddings.embed_query(query)
        
        # 相似度检索
        results = self.text_vectorstore.similarity_search_with_score(query, k=top_k*2)
        
        # 结果后处理
        enriched_results = []
        for doc, score in results:
            # 检查是否包含原始数值特征
            if 'numeric_features' in doc.metadata:
                numeric_features = doc.metadata['numeric_features']
                
                # 在原始数据中查找匹配
                matching_rows = self.numeric_data[
                    (self.numeric_data['exchange_rate'] == doc.metadata.get('exchange_rate', 0))
                ]
                
                enriched_results.append({
                    'text_content': doc.page_content,
                    'semantic_score': score,
                    'numeric_data': matching_rows.to_dict('records')[0] if not matching_rows.empty else None
                })
            else:
                enriched_results.append({
                    'text_content': doc.page_content,
                    'semantic_score': score,
                    'numeric_data': None
                })
        
        # 排序并返回
        return sorted(enriched_results, key=lambda x: x['semantic_score'])[:top_k]
# import openai

# class GPT4Generator:
#     def __init__(self, api_key: str):
#         openai.api_key = api_key

#     def generate(self, prompt: str, max_tokens: int = 500) -> str:
#         """调用 GPT-4 生成答案"""
#         response = openai.ChatCompletion.create(
#             model="gpt-4o",
#             messages=[
#                 {"role": "system", "content": "你是一个金融分析师，根据提供的上下文生成专业、准确的回答。"},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=max_tokens,
#             temperature=0.3  # 控制生成结果的随机性
#         )
#         return response.choices[0].message["content"]

# class ConversationManager:
#     def __init__(self, max_tokens: int = 8000, recent_window: int = 5):
#         """
#         :param max_tokens: 最大上下文长度（tokens）
#         :param recent_window: 最近对话窗口大小
#         """
#         self.max_tokens = max_tokens
#         self.recent_window = recent_window
#         self.conversation_history = []  # 存储对话历史

#     def add_message(self, role: str, content: str):
#         """添加对话消息"""
#         self.conversation_history.append({"role": role, "content": content})

#     def truncate_context(self) -> List[Dict]:
#         """截断上下文，确保不超过最大长度"""
#         # 优先保留最近的对话
#         recent_messages = self.conversation_history[-self.recent_window:]
        
#         # 计算当前 tokens 数量
#         current_tokens = sum(len(msg["content"].split()) for msg in recent_messages)
        
#         # 如果未超过最大长度，直接返回
#         if current_tokens <= self.max_tokens:
#             return recent_messages
        
#         # 如果超过最大长度，逐步移除最早的消息
#         truncated_messages = recent_messages.copy()
#         while current_tokens > self.max_tokens and len(truncated_messages) > 1:
#             removed_message = truncated_messages.pop(0)  # 移除最早的消息
#             current_tokens -= len(removed_message["content"].split())
        
#         return truncated_messages

#     def get_context(self) -> str:
#         """获取截断后的上下文"""
#         truncated_messages = self.truncate_context()
#         return "\n".join([f"{msg['role']}: {msg['content']}" for msg in truncated_messages])


# class FinancialRAG:
#     def __init__(self, indexer: HybridIndexer, gpt4_generator: GPT4Generator):
#         self.indexer = indexer
#         self.gpt4_generator = gpt4_generator
#         self.conversation_manager = ConversationManager()

#     def generate_answer(self, query: str) -> str:
#         # 添加用户问题到对话历史
#         self.conversation_manager.add_message("user", query)
        
#         # 检索相关分块
#         relevant_chunks = self.indexer.search(query)
#         context = self._format_context(relevant_chunks)
        
#         # 获取截断后的对话历史
#         conversation_context = self.conversation_manager.get_context()
        
#         # 构建 GPT-4 的输入提示
#         prompt = f"""
#         对话历史：
#         {conversation_context}
        
#         上下文：
#         {context}
        
#         问题：{query}
#         请根据上下文和对话历史生成回答。
#         """
        
#         # 调用 GPT-4 生成答案
#         answer = self.gpt4_generator.generate(prompt)
        
#         # 添加生成的答案到对话历史
#         self.conversation_manager.add_message("assistant", answer)
#         return answer

#     def _format_context(self, chunks: List[Dict]) -> str:
#         """格式化检索到的分块为 GPT-4 的输入上下文"""
#         context = []
#         for chunk in chunks:
#             if chunk["type"] == "text":
#                 context.append(f"[新闻] {chunk['content']}")
#             elif chunk["type"] == "data":
#                 context.append(f"[数据] {chunk['metadata']['description']}")
#         return "\n".join(context)

# %%

import os
from typing import List, Dict, Any
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class ForexRiskMultiAgentSystem:
    def __init__(self, openai_api_key: str):
        """
        初始化多智能体系统，包括不同专业角色的智能体
        """
        os.environ["OPENAI_API_KEY"] = openai_api_key
        
        # 初始化不同角色的语言模型
        self.economic_analyst = ChatOpenAI(temperature=0.1, model="gpt-4")
        self.risk_manager = ChatOpenAI(temperature=0.2, model="gpt-4")
        self.policy_expert = ChatOpenAI(temperature=0.3, model="gpt-4")
        
        # 定义各角色的专业提示模板1
        # 1.金融分析提示词
        self.economic_analyst_prompt = PromptTemplate(
            input_variables=["query", "context"],
            template="""作为经济分析师，分析以下外汇风险场景：
查询内容：{query}
上下文信息：{context}

请从宏观经济角度提供详细分析，重点关注：
1. 经济指标变化
2. 潜在经济风险
3. 汇率波动可能性
"""
        )
        # 2.风险管理提示词
        self.risk_manager_prompt = PromptTemplate(
            input_variables=["query", "context"],
            template="""作为风险管理专家，评估以下外汇风险场景：
查询内容：{query}
上下文信息：{context}

请提供具体风险评估，包括：
1. 风险等级
2. 风险缓解策略
3. 可能的金融工具对冲建议
"""
        )
        # 3.政策法规专家提示词
        self.policy_expert_prompt = PromptTemplate(
            input_variables=["query", "context"],
            template="""作为政策法规专家，解读以下外汇风险场景：
查询内容：{query}
上下文信息：{context}

请分析：
1. 相关法规和政策
2. 合规性建议
3. 潜在政策风险
"""
        )
        
        # 创建专业分析链
        self.economic_analysis_chain = LLMChain(
            llm=self.economic_analyst, 
            prompt=self.economic_analyst_prompt
        )
        
        self.risk_analysis_chain = LLMChain(
            llm=self.risk_manager, 
            prompt=self.risk_manager_prompt
        )
        
        self.policy_analysis_chain = LLMChain(
            llm=self.policy_expert, 
            prompt=self.policy_expert_prompt
        )

    def comprehensive_risk_assessment(
        self, 
        query: str, 
        rag_context: List[Dict[str, Any]]
    ) -> Dict[str, str]:
        """
        综合多智能体分析
        
        Args:
            query (str): 用户查询
            rag_context (List[Dict]): RAG系统检索的上下文
        
        Returns:
            Dict[str, str]: 多维度风险评估报告
        """
        # 直接使用文本内容作为上下文
        context_str = "\n\n".join([
            item['text_content'] for item in rag_context
        ])
        
        # 并行执行多智能体分析
        economic_analysis = self.economic_analysis_chain.run({
            "query": query, 
            "context": context_str
        })
        
        risk_analysis = self.risk_analysis_chain.run({
            "query": query, 
            "context": context_str
        })
        
        policy_analysis = self.policy_analysis_chain.run({
            "query": query, 
            "context": context_str
        })
        
        return {
            "economic_analysis": economic_analysis,
            "risk_analysis": risk_analysis,
            "policy_analysis": policy_analysis
        }

    def integrate_with_rag_system(
        self, 
        rag_system: CrossModalRAGSystem, 
        query: str
    ):
        """
        与原RAG系统集成
        
        Args:
            rag_system (CrossModalRAGSystem): 跨模态RAG系统实例
            query (str): 用户查询
        
        Returns:
            Dict: 综合风险评估结果
        """
        # 使用RAG系统进行检索
        rag_context = rag_system.advanced_retrieval(query)
        
        # 多智能体风险评估
        risk_assessment = self.comprehensive_risk_assessment(
            query, rag_context
        )
        
        return {
            "rag_context": rag_context,
            "risk_assessment": risk_assessment
        }

