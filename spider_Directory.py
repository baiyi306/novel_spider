import requests
from bs4 import BeautifulSoup
import re

# 1. 填入小说的【目录页】网址
BOOK_URL = "http://www.ibiqugu.net/15/15021/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def get_all_chapters():
    """获取目录页所有章节"""
    print("正在分析目录，请稍等...")
    resp = requests.get(BOOK_URL, headers=HEADERS, timeout=15)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, "html.parser")

    chapter_tags = soup.select("#list a")
    if not chapter_tags:
        chapter_tags = soup.select(".listmain a")
    if not chapter_tags:
        chapter_tags = soup.select("dl dd a")

    chapters = []
    if not chapter_tags:
        return chapters

    for a in chapter_tags:
        title = a.get_text(strip=True)
        href = a.get("href")

        if not href or not title or "javascript" in href:
            continue

        if href.startswith("/"):
            full_url = "http://www.ibiqugu.net" + href
        elif href.startswith("http"):
            full_url = href
        else:
            base = BOOK_URL.rstrip("/")
            full_url = base + "/" + href

        chapters.append({"title": title, "url": full_url})

    return chapters


def extract_chapter_number(title):
    """
    从标题中提取真实的章节数字。
    如果提取不到（比如是“作品相关”），返回 None。
    """
    # 匹配类似“第一百三十章”、“第131章”这样的格式
    match = re.search(r'第\s*([零一二三四五六七八九十百千万0-9]+)\s*章', title)
    if match:
        num_str = match.group(1)
        # 如果是阿拉伯数字，直接转int
        if num_str.isdigit():
            return int(num_str)
        # 如果是中文数字，这里做个简单的处理（只处理常见的千位以内）
        # 为了简单，我们这里只依赖网站按顺序排列，提取不到数字就直接返回字符串去匹配
        return num_str
    return None


def main():
    all_chapters = get_all_chapters()

    if not all_chapters:
        print("获取目录失败。")
        return

    print(f"✅ 目录解析成功！网站原始列表有 {len(all_chapters)} 个链接。\n")

    try:
        target_start = int(input("请输入你想获取的【起始章节序号】(例如输入 131): "))
        target_end = int(input("请输入你想获取的【结束章节序号】(例如输入 131): "))
    except ValueError:
        print("⚠️ 输入错误！请输入纯数字。")
        return

    print(f"\n🔍 正在为你精准匹配第 {target_start} 章 到 第 {target_end} 章...\n")
    print("-" * 60)

    found_count = 0

    # 遍历整个目录，只寻找真正的章节
    for i, chapter in enumerate(all_chapters):
        title = chapter['title']

        # 获取标题里的数字
        ch_num = extract_chapter_number(title)

        if ch_num is None:
            continue  # 提取不到“第X章”的，直接跳过

        # 尝试将提取到的数字转换为整数进行比较
        # 注意：如果遇到“第一百三十一章”，直接转 int 会报错。
        # 但我们可以利用列表的顺序！网站一般是从头到尾顺序排列的。
        # 既然你要找 131，我们就按顺序数到第 131 个带有“第...章”的链接。

        if "章" in title:
            found_count += 1
            # 如果当前数到的顺序，正好在你想要的范围内
            if target_start <= found_count <= target_end:
                print(f"[{found_count}] {title}")
                print(f"    🔗 {chapter['url']}\n")

        # 如果已经找够了，就提前结束循环
        if found_count > target_end:
            break

    print("-" * 60)
    if found_count == 0:
        print("⚠️ 没找到符合条件的章节，可能是标题格式特殊。")
    else:
        print("提取完毕！")


if __name__ == "__main__":
    main()