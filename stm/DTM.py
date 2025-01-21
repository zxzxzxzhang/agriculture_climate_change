
import re

import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

df = pd.read_excel(r'../new_agriculture_data.xlsx')
df = df.dropna(subset=['摘要(译)(English)'])
df = df[df['摘要(译)(English)'] != '-']

import spacy

nlp = spacy.load('en_core_web_sm')

def clean_step1(text):
    # 去除标点符号和特殊字符
    text = re.sub(r'[^\w\s]', '', text)
    # 去除所有符号和数字
    pattern = re.compile(r'[^a-zA-Z\s]')
    text = pattern.sub(' ', text)
    # 分词
    tokens = nltk.word_tokenize(text)
    # 转换为小写
    tokens = [token.lower() for token in tokens]
    # 移除停用词
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    # 词形还原
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    doc = nlp(' '.join(tokens))  # 将清理后的词汇列表重新组合成字符串并进行处理
    cleaned_text = ' '.join([token.lemma_.lower().strip() for token in doc if not token.is_stop])
    return cleaned_text

df['摘要(译)(English)'] = df['摘要(译)(English)'].astype(str).apply(clean_step1)

def clean_step2(text):
    # 去除标点符号和特殊字符
    text = re.sub(r'[^\w\s]', '', text)
    # 去除所有符号和数字
    pattern = re.compile(r'[^a-zA-Z\s]')
    text = pattern.sub(' ', text)
    # 分词
    tokens = nltk.word_tokenize(text)
    # 转换为小写
    tokens = [token.lower() for token in tokens]
    # 移除停用词
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    # 词形还原
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    doc = nlp(text)
    tokens = [token.lemma_.lower().strip() for token in doc if not token.is_stop]
    return tokens

df['摘要(译)(English)'] = df['摘要(译)(English)'].astype(str).apply(clean_step2)

from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
# 假设 df['摘要_英文'] 包含了经过 clean_text 处理后的结果
corpus = df['摘要(译)(English)'].apply(lambda tokens: ' '.join(tokens))

vectorizer = CountVectorizer()
DTM = vectorizer.fit_transform(corpus)

# 可选：将结果转换为DataFrame
DTM_df = pd.DataFrame(DTM.toarray(), columns=vectorizer.get_feature_names_out())

DTM_df.to_csv(r'DTM_new.csv')
