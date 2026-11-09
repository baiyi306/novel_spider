from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, HTTPException,Request
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import re

app = FastAPI(title="小说爬虫API", description="提供搜索、目录、正文提取接口")
# 挂载 templates 文件夹
templates = Jinja2Templates(directory="templates")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 这里放你之前写的 cn_to_int 等辅助函数
CN_NUM = {'零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}
CN_UNIT = {'十': 10, '百': 100, '千': 1000, '万': 10000}


def cn_to_int(cn_str):
    if not cn_str: return None
    if cn_str.isdigit(): return int(cn_str)
    total = 0;
    section = 0;
    number = 0
    for char in cn_str:
        if char in CN_NUM:
            number = CN_NUM[char]
        elif char in CN_UNIT:
            unit = CN_UNIT[char]
            if unit == 10000:
                section = (section + number) * unit
                total += section
                section = 0
            else:
                if number == 0: number = 1
                section += number * unit
            number = 0
    return total + section + number


# ================= 接口 1：搜索小说 =================
@app.get("/search")
def search_api(keyword: str):
    """传入书名，返回搜索结果列表"""
    search_url = f"http://www.ibiqugu.net/modules/article/waps.php?searchkey={keyword}"
    try:
        resp = requests.get(search_url, headers=HEADERS, timeout=15)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, "html.parser")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    results = []
    table = soup.find("table")
    if table:
        rows = table.find_all("tr")[1:]
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 3:
                a_tag = cols[0].find("a")
                if a_tag:
                    title = a_tag.get_text(separator="", strip=True)
                    href = a_tag.get("href")
                    author = cols[2].get_text(separator="", strip=True)
                    if not href: continue
                    full_url = "http://www.ibiqugu.net" + href if href.startswith("/") else href
                    results.append({"title": title, "author": author, "url": full_url})

    return {"code": 200, "data": results}


# ================= 接口 2：提取单章正文 =================
class ChapterRequest(BaseModel):
    book_url: str  # 小说目录页网址
    chapter_num: int  # 章节号


@app.post("/get_chapter")
def get_chapter_api(req: ChapterRequest):
    """
    传入小说目录页URL和章节号，返回提取好的正文。
    (因为要传入URL，用 POST 请求更合适)
    """
    # 1. 加载目录
    try:
        resp = requests.get(req.book_url, headers=HEADERS, timeout=15)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, "html.parser")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"目录加载失败: {e}")

    chapter_tags = soup.select("#list a") or soup.select(".listmain a") or soup.select("dl dd a")
    target_url = None
    target_title = ""

    # 2. 匹配章节
    for a in chapter_tags:
        title = a.get_text(strip=True)
        match = re.search(r'第\s*([零一二三四五六七八九十百千万0-9]+)\s*章', title)
        if match:
            num = cn_to_int(match.group(1))
            if num == req.chapter_num:
                href = a.get("href")
                target_url = "http://www.ibiqugu.net" + href if href.startswith("/") else href
                target_title = title
                break

    if not target_url:
        raise HTTPException(status_code=404, detail="未找到该章节")

    # 3. 爬取并清洗正文
    try:
        content_resp = requests.get(target_url, headers=HEADERS, timeout=15)
        content_resp.encoding = 'utf-8'
        content_soup = BeautifulSoup(content_resp.text, "html.parser")
        content_tag = content_soup.find("div", id="content")

        tip = content_tag.find("div", id="content_tip")
        if tip: tip.decompose()

        text = content_tag.get_text(separator="\n", strip=True)
        text = text.replace('\xa0', ' ').replace('\u3000', ' ')
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'亲,点击进去.*', '', text)
        text = re.sub(r'手机站全新改版.*', '', text)
        text = text.replace('最新网址：www.ibiqugu.net', '')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"正文提取失败: {e}")

    return {
        "code": 200,
        "chapter_name": target_title,
        "content": text.strip()
    }

# ================= 把网页发出去的路由 =================
# 注意：这里的 @app.get("/") 代表网页的根目录（也就是 http://127.0.0.1:8000/）
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
# =====================================================

# 运行入口
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)