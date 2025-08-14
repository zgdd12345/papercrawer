# papercrawer
爬arxive等开源文献

## 功能
这个脚本可以从 arXiv API 获取与指定关键词相关的学术论文信息，包括标题、作者、摘要和链接，并支持批量下载PDF文件。

## 安装依赖
```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 获取论文信息
取消注释 `crawer.py` 中的以下代码段：
```python
if __name__ == "__main__":
    query = input("请输入检索关键词: ")
    papers = fetch_arxiv_papers(query)
    for i, paper in enumerate(papers, 1):
        print(f"\n论文 {i}:")
        print("标题:", paper['title'])
        print("作者:", ', '.join(paper['authors']))
        print("摘要:", paper['summary'])
        print("链接:", paper['link'])
```

### 2. 批量下载论文PDF
脚本默认会批量下载论文PDF文件到 `./papers` 目录：
```python
if __name__ == "__main__":
    download_arxiv_papers(query="cat:quant-ph AND cs.DS", max_results=10)
```
可以修改 `query` 参数来搜索不同的论文类别，`max_results` 参数控制下载数量。

## 依赖
- requests
- beautifulsoup4
- lxml
- arxiv
