import pandas as pd
from pyecharts.charts import Sankey
from pyecharts import options as opts
import re

df1 = pd.read_excel("TR_result.xlsx")

mylist1 = list(df1.values.flatten())

pattern = re.compile(r"'(.*?)'")
content_set = set()
for item in mylist1:
    content_set.update(pattern.findall(item))

content_list = list(content_set)

len(content_list)

content = pd.DataFrame(content_list, columns=['words'])

content[df1.columns] = None

for j, column in enumerate(df1.columns):
    column_data = df1[column]
    for i, value in enumerate(column_data):
        pattern = re.compile(r"'(.*?)'")
        element_list = pattern.findall(value)
        element = ''.join(element_list)
        pattern2 = re.compile(r', (.*?)\)')
        element_list2 = pattern2.findall(value)
        element2 = float(element_list2[0])
        if element in content['words'].tolist():
            content.loc[element, df1.columns[j]] = element2

df2 = content.drop(content.index[0:len(content_list)])
df2 = df2.drop(columns=['words'])

from scipy.spatial import distance

df2_filled = df2.fillna(0)

similarity_matrix = pd.DataFrame(columns=df2_filled.columns, index=df2_filled.columns)
for col1 in df2_filled.columns:
    for col2 in df2_filled.columns:
        if col1 != col2:
            vec1 = df2_filled[col1].tolist()
            vec2 = df2_filled[col2].tolist()
            similarity = 1 - distance.cosine(vec1, vec2)
            similarity_matrix.at[col1, col2] = similarity

similarities_1_2 = similarity_matrix.loc[['A0'], ['B0', 'B1']].reset_index(drop=True)
similarities_2_3 = similarity_matrix.loc[['B0', 'B1'], ['C0', 'C1', 'C2']].reset_index(drop=True)
similarities_3_4 = similarity_matrix.loc[['C0', 'C1', 'C2'], ['D0', 'D1', 'D2']].reset_index(drop=True)
similarities_4_5 = similarity_matrix.loc[['D0', 'D1', 'D2'], ['E0', 'E1', 'E2']].reset_index(drop=True)

import numpy as np
def find_similar_elements(matrix):
    matrix = matrix.to_numpy()
    rows, cols = np.where(matrix > 0)
    values = matrix[rows, cols]
    similar_matrix = np.column_stack((rows, cols, values))
    return similar_matrix

similar_elements_1_2 = find_similar_elements(similarities_1_2)

similar_elements_1_2_pd = pd.DataFrame(similar_elements_1_2, columns=['Source', 'Target', 'Value'])
similar_elements_1_2_pd['Source'] = similar_elements_1_2_pd['Source'].apply(lambda x: 'A' + str(int(x)))
similar_elements_1_2_pd['Target'] = similar_elements_1_2_pd['Target'].apply(lambda x: 'B' + str(int(x)))

similar_elements_2_3 = find_similar_elements(similarities_2_3)

similar_elements_2_3_pd = pd.DataFrame(similar_elements_2_3, columns=['Source', 'Target', 'Value'])
similar_elements_2_3_pd['Source'] = similar_elements_2_3_pd['Source'].apply(lambda x: 'B' + str(int(x)))
similar_elements_2_3_pd['Target'] = similar_elements_2_3_pd['Target'].apply(lambda x: 'C' + str(int(x)))

similar_elements_3_4 = find_similar_elements(similarities_3_4)

similar_elements_3_4_pd = pd.DataFrame(similar_elements_3_4, columns=['Source', 'Target', 'Value'])
similar_elements_3_4_pd['Source'] = similar_elements_3_4_pd['Source'].apply(lambda x: 'C' + str(int(x)))
similar_elements_3_4_pd['Target'] = similar_elements_3_4_pd['Target'].apply(lambda x: 'D' + str(int(x)))

similar_elements_4_5 = find_similar_elements(similarities_4_5)

similar_elements_4_5_pd = pd.DataFrame(similar_elements_4_5, columns=['Source', 'Target', 'Value'])
similar_elements_4_5_pd['Source'] = similar_elements_4_5_pd['Source'].apply(lambda x: 'D' + str(int(x)))
similar_elements_4_5_pd['Target'] = similar_elements_4_5_pd['Target'].apply(lambda x: 'E' + str(int(x)))

similar_elements_1_2_3_pd = pd.concat([similar_elements_1_2_pd, similar_elements_2_3_pd, similar_elements_3_4_pd, similar_elements_4_5_pd])

name = pd.read_excel('agricultural_topics_with_english.xlsx')
topic_dict = dict(zip(name['主题'], name['English Topic Name']))

def add_newlines_after_three_words(text):
    words = text.split()
    new_text = '\n'.join([' '.join(words[i:i+3]) for i in range(0, len(words), 3)])
    return new_text

for key, value in topic_dict.items():
    topic_dict[key] = add_newlines_after_three_words(value)
similar_elements_1_2_3_pd['Source'] = similar_elements_1_2_3_pd['Source'].map(lambda x: f"{x}\n{topic_dict.get(x)}")
similar_elements_1_2_3_pd['Target'] = similar_elements_1_2_3_pd['Target'].map(lambda x: f"{x}\n{topic_dict.get(x)}")

nodes = pd.Series(similar_elements_1_2_3_pd['Source'].tolist() + similar_elements_1_2_3_pd['Target'].tolist()).unique()

node_index = {node: index for index, node in enumerate(nodes)}

similar_elements_1_2_3_pd['source'] = similar_elements_1_2_3_pd['Source'].apply(lambda x: node_index[x])
similar_elements_1_2_3_pd['target'] = similar_elements_1_2_3_pd['Target'].apply(lambda x: node_index[x])

links = similar_elements_1_2_3_pd[['source', 'target', 'Value']]

data = similar_elements_1_2_3_pd.values.tolist()

nodes = []
links = []

for item in data:
    source = item[0]
    target = item[1]
    value = item[2]

    if source not in nodes:
        nodes.append(source)
    if target not in nodes:
        nodes.append(target)

    links.append({"source": source, "target": target, "value": value})

sankey = (
    Sankey(init_opts=opts.InitOpts( bg_color="#FFFFFF",width="2000px", height="800px"))
    .add(
        series_name="",
        nodes=[{"name": node} for node in nodes],
        links=links,
        linestyle_opt=opts.LineStyleOpts(opacity=0.5, curve=0.3, color="source"),
        label_opts=opts.LabelOpts(
            font_size=18,
            font_weight="bold", 
            color="black", 
        )
    )
    .set_global_opts(title_opts=opts.TitleOpts(title=""),
                     )
     
)

sankey.render('sankey_chart.html')