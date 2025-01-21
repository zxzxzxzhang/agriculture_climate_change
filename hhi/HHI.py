import pandas as pd

df = pd.read_excel('../new_agriculture_data.xlsx')
df.astype(str)
yearly_patent_count = df.groupby('申请年')['公开(公告)号'].count()
yearly_patent_count = pd.DataFrame(yearly_patent_count).rename(columns={'公开(公告)号': '专利数量'})

ipc_yearly_patent_count = df[df['IPC主分类号(小类)'] != '-'].groupby(['申请年', 'IPC主分类号(小类)'])['公开(公告)号'].count().unstack(fill_value=0)
ipc_yearly_patent_count.rename(columns={'IPC主分类号(小类)': '申请年'}, inplace=True)

ipc_yearly_patent_count = ipc_yearly_patent_count.reset_index()
yearly_patent_count = yearly_patent_count.reset_index()

full_ipc_yearly_patent_count = ipc_yearly_patent_count.merge(yearly_patent_count, on='申请年', how='left')

def hhiyear(ipc, count):
    if count == 0:
        return 0
    hhi = 0
    for share in ipc:
        hhi += (share / count) ** 2
    return hhi

hhi_results = []
for index, row in full_ipc_yearly_patent_count.iterrows():
    ipc = row.iloc[1:-1]  
    count = row['专利数量']
    hhi = hhiyear(ipc, count)
    hhi_results.append(hhi)

full_ipc_yearly_patent_count['HHI'] = hhi_results
full_ipc_yearly_patent_count['申请年'] = full_ipc_yearly_patent_count['申请年'].astype(int)
full_ipc_yearly_patent_count.rename(columns={'申请年': 'Year'}, inplace=True)

full_ipc_yearly_patent_count.to_excel('HHI.xlsx', index=False)

