import arxiv
import requests
import os
from tqdm import tqdm
from time import sleep

# 1. 搜索量子计算相关论文
search = arxiv.Search(
    query="quantum computing",
    max_results=None,  # 获取所有结果
    sort_by=arxiv.SortCriterion.SubmittedDate
)
results = list(search.results())

# 2. 创建保存目录
save_dir = "quantum_papers"
os.makedirs(save_dir, exist_ok=True)

# 3. 带进度条的下载函数
def download_with_progress(url, filename):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(os.path.join(save_dir, filename), 'wb') as f:
        with tqdm(total=total_size, unit='B', unit_scale=True, desc=filename[:20]) as pbar:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))

# 4. 批量下载论文
for idx, paper in enumerate(tqdm(results, desc="Total Progress")):
    try:
        download_with_progress(paper.pdf_url, f"{paper.get_short_id()}.pdf")
        sleep(1)  # 避免请求过频
    except Exception as e:
        print(f"下载失败 {paper.title}: {str(e)}")
        # test
