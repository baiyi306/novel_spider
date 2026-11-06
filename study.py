import requests
from bs4 import BeautifulSoup
import re
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

CN_NUM = {'零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}
CN_UNIT = {'十': 10, '百': 100, '千': 1000, '万': 10000}


def cn_to_int(cn_str):
    """将中文数字字符串转为整数"""
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


def search_book(keyword):
    """搜索小说"""
    print(f"🔍 正在搜索: {keyword} ...")
    search_url = f"http://www.ibiqugu.net/modules/article/waps.php?searchkey={keyword}"
    try:
        resp = requests.get(search_url, headers=HEADERS, timeout=15)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, "html.parser")
    except Exception as e:
        print(f"❌ 搜索请求失败: {e}")
        return []

    results = []
    seen_urls = set()
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

                    if href.startswith("/"):
                        full_url = "http://www.ibiqugu.net" + href
                    elif href.startswith("http"):
                        full_url = href
                    else:
                        full_url = "http://www.ibiqugu.net/" + href

                    if full_url not in seen_urls:
                        seen_urls.add(full_url)
                        results.append({"title": title, "author": author, "url": full_url})
    return results


def load_chapters(book_url):
    """加载章节列表"""
    print("\n📚 正在加载该书目录，请稍等...")
    try:
        resp = requests.get(book_url, headers=HEADERS, timeout=15)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, "html.parser")
    except Exception as e:
        print(f"❌ 目录加载失败: {e}")
        return []

    chapter_tags = soup.select("#list a") or soup.select(".listmain a") or soup.select("dl dd a")
    chapters = []
    if not chapter_tags: return chapters

    for a in chapter_tags:
        title = a.get_text(strip=True)
        href = a.get("href")
        if not href or not title or "javascript" in href: continue
        if href.startswith("/"):
            full_url = "http://www.ibiqugu.net" + href
        elif href.startswith("http"):
            full_url = href
        else:
            full_url = book_url.rstrip("/") + "/" + href
        chapters.append({"title": title, "url": full_url})
    return chapters


def get_content(chapter_url):
    """提取正文"""
    try:
        resp = requests.get(chapter_url, headers=HEADERS, timeout=15)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, "html.parser")
        content_tag = soup.find("div", id="content")
        if not content_tag: return "⚠️ 未找到正文内容。"

        tip = content_tag.find("div", id="content_tip")
        if tip: tip.decompose()
        for unwanted in content_tag.find_all(["script", "style"]): unwanted.decompose()

        text = content_tag.get_text(separator="\n", strip=True)
        text = text.replace('\xa0', ' ').replace('\u3000', ' ')
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'亲,点击进去.*', '', text)
        text = re.sub(r'手机站全新改版.*', '', text)
        text = text.replace('最新网址：www.ibiqugu.net', '')
        return text.strip()
    except Exception as e:
        return f"⚠️ 提取正文失败: {e}"


def main():
    print("========= 📖 小说阅读器 =========")

    # 外层大循环：控制搜索和选书
    while True:
        keyword = input("\n👉 请输入你想看的小说书名或作者名 (输入 q 退出程序): ").strip()
        if not keyword: continue
        if keyword.lower() == 'q':
            print("退出程序，再见！")
            break

        search_results = search_book(keyword)
        if not search_results:
            print("\n⚠️ 没有找到相关小说或作者，请换个关键词试试。")
            continue

        print(f"\n✅ 找到 {len(search_results)} 个结果:")
        for i, res in enumerate(search_results):
            print(f"[{i + 1}] 《{res['title']}》 - 作者: {res['author']}")

        choice_str = input(f"\n👉 请选择正确的书籍序号 (1 - {len(search_results)})，或直接回车重新搜索: ").strip()
        if choice_str == "" or choice_str == "0":
            continue

        try:
            choice = int(choice_str)
            if 1 <= choice <= len(search_results):
                current_book = search_results[choice - 1]
                print(f"✅ 已进入: 《{current_book['title']}》")
                chapters = load_chapters(current_book['url'])
                if not chapters:
                    print("❌ 无法加载章节列表，请重试。")
                    continue
            else:
                print("⚠️ 序号超出范围。")
                continue
        except ValueError:
            print("⚠️ 输入错误，请输入数字。")
            continue

        # 内层循环：阅读阶段
        print("\n========= 开始阅读 =========")
        print("💡 提示: 输入数字看章节；输入其他文字（如书名）可直接换书；输入 q 退出程序。")

        while True:
            # 提示语里明确告诉用户怎么换书
            user_input = input("\n👉 请输入章节序号 (或输入书名换书): ").strip()

            if not user_input: continue

            if user_input.lower() == 'q':
                print("退出程序，再见！")
                return

                # 核心判断：如果输入的是纯数字，就是看章节
            if user_input.isdigit():
                target_chapter = int(user_input)
                chapter_found = False

                for chapter in chapters:
                    title = chapter['title']
                    match = re.search(r'第\s*([零一二三四五六七八九十百千万0-9]+)\s*章', title)
                    if match:
                        chapter_num = cn_to_int(match.group(1))
                        if chapter_num == target_chapter:
                            print("\n" + "=" * 60)
                            print(f"📖【{title}】")
                            print("-" * 60)
                            content = get_content(chapter['url'])
                            print(content)
                            print("=" * 60)
                            chapter_found = True
                            break

                if not chapter_found:
                    print(f"⚠️ 没找到第 {target_chapter} 章。")
                time.sleep(0.5)

            # 如果输入的不是数字（比如输入了“剑来”），直接默认用户想换书
            else:
                print(f"\n🔄 收到新关键词 '{user_input}'，正在退回搜索界面...")
                # 利用一个巧妙的变量覆盖，让外层循环直接去搜这个新词
                # 这里用 break 跳出内层循环，直接回到最外层的 while True
                break
                # 注意：因为外层循环一开始会 input，为了让用户不再重新敲一遍，我们可以考虑用变量传递。
                # 但最简单的做法是直接 break，让用户在上面再输入一次。
                # 为了极致体验，我们把 user_input 赋给一个全局变量或者利用参数传递。


if __name__ == "__main__":
    main()