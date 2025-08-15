from random import uniform
import arxiv
import requests
import os
from tqdm import tqdm
from time import sleep

# 1. 搜索量子计算相关论文
search = arxiv.Search(
    query="cat:quant-ph AND cs.DS",
    max_results=None,  # 获取所有结果
    sort_by=arxiv.SortCriterion.SubmittedDate
)
client = arxiv.Client()
results = list(client.results(search))
print(f"找到 {len(results)} 篇论文")
# 2. 创建保存目录
save_dir = "quantum_papers"
os.makedirs(save_dir, exist_ok=True)

# 3. 带进度条的下载函数
# def download_with_progress(url, filename, pbar):
#     response = requests.get(url, stream=True)
#     for chunk in response.iter_content(chunk_size=1024):
#         if chunk:
#             with open(os.path.join(save_dir, filename), 'ab') as f:
#                 f.write(chunk)
#             pbar.update(len(chunk))

# 4. 批量下载论文
# total_bytes = 0
# paper_sizes = []
# for paper in results:
#     # print(dir(paper))
#     try:
#         head = requests.head(paper.pdf_url)
#         size = int(head.headers.get('content-length', 0))
#     except Exception:
#         size = 0
#     paper_sizes.append(size)
#     total_bytes += size

with tqdm(total=len(results), desc='Download Progress') as pbar:
    for idx, paper in enumerate(results):
        try:
            # filename = f"{paper.get_short_id()}.pdf"
            paper._pdf_url = paper.pdf_url.replace("arxiv.org", "xxx.itp.ac.cn")
            # download_with_progress(paper.pdf_url, filename, pbar)
            paper.download_pdf(dirpath="./papers")
            pbar.update(1)
            sleep(uniform(1, 3))  # 避免请求过频
        except Exception as e:
            print(f"下载失败 {paper.title}: {str(e)}")
