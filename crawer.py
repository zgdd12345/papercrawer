# arXiv 文献爬虫示例
import requests

import arxiv
from bs4 import BeautifulSoup

def fetch_arxiv_papers(query, max_results=5):
	"""
	爬取 arXiv 上与 query 相关的论文，返回标题、作者和摘要。
	"""
	url = f"https://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}"
	
	# 设置请求头以避免SSL问题
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
	}
	
	try:
		response = requests.get(url, headers=headers, timeout=30)
		if response.status_code != 200:
			print("请求失败", response.status_code)
			return []
		soup = BeautifulSoup(response.content, 'xml')
	except requests.exceptions.RequestException as e:
		print("网络请求错误:", e)
		return []
	except Exception as e:
		print("解析错误:", e)
		return []
	
	entries = soup.find_all('entry')
	papers = []
	for entry in entries:
		title = entry.title.text.strip().replace('\n', ' ')
		authors = [author.find('name').text for author in entry.find_all('author')]
		summary = entry.summary.text.strip().replace('\n', ' ')
		link = entry.id.text
		papers.append({
			'title': title,
			'authors': authors,
			'summary': summary,
			'link': link
		})
	return papers


  # 安装：pip install arxiv
import os

def download_arxiv_papers(query="cat:cs.CV", max_results=None):
    # 按关键词批量下载（计算机视觉领域示例）
    # 创建papers目录（如果不存在）
    os.makedirs("./papers", exist_ok=True)
    
    search = arxiv.Search(
        query=query,  # 学科分类码
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    
    client = arxiv.Client()

    for result in client.results(search):
        try:
            result.download_pdf(dirpath="./papers")  # 保存到本地文件夹
            print(f"✅ 已下载: {result.title}")
        except Exception as e:
            print(f"❌ 下载失败: {result.title} - 错误: {e}")
            continue



if __name__ == "__main__":
	# query = input("请输入检索关键词: ")
	# papers = fetch_arxiv_papers(query)
	# for i, paper in enumerate(papers, 1):
	# 	print(f"\n论文 {i}:")
	# 	print("标题:", paper['title'])
	# 	print("作者:", ', '.join(paper['authors']))
	# 	print("摘要:", paper['summary'])
	# 	print("链接:", paper['link'])
    download_arxiv_papers(query="cat:quant-ph AND cs.DS", max_results=10)
