import requests
from bs4 import BeautifulSoup
import re
import time

# 1. 填入小说的【目录页】网址
BOOK_URL = "http://www.ibiqugu.net/15/15021/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 全局缓存，避免每次输入都重新请求目录
ALL_CHAPTERS = []


def get_all_chapters():
    """获取目录页所有章节（包含杂项）"""
    try:
        resp = requests.get(BOOK_URL, headers=HEADERS, timeout=15)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, "html.parser")
    except Exception as e:
        return []

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
            full_url = BOOK_URL.rstrip("/") + "/" + href

        chapters.append({"title": title, "url": full_url})
    return chapters


def get_content(chapter_url):
    """提取单章正文"""
    try:
        resp = requests.get(chapter_url, headers=HEADERS, timeout=15)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, "html.parser")

        content_tag = soup.find("div", id="content")
        if not content_tag:
            return "⚠️ 未找到正文内容。"

        tip = content_tag.find("div", id="content_tip")
        if tip:
            tip.decompose()
        for unwanted in content_tag.find_all(["script", "style"]):
            unwanted.decompose()

        text = content_tag.get_text(separator="\n", strip=True)
        text = text.replace('\xa0', ' ').replace('\u3000', ' ')
        text = re.sub(r'\n+', '\n', text)

        # 清理底部牛皮癣广告
        text = re.sub(r'亲,点击进去.*', '', text)
        text = re.sub(r'手机站全新改版.*', '', text)
        text = text.replace('最新网址：www.ibiqugu.net', '')

        return text.strip()
    except Exception as e:
        return f"⚠️ 提取正文失败: {e}"


def main():
    global ALL_CHAPTERS

    # 第一次运行前先静默加载目录
    if not ALL_CHAPTERS:
        print("📚 首次启动，正在加载小说目录，请稍等...")
        ALL_CHAPTERS = get_all_chapters()
        if not ALL_CHAPTERS:
            print("❌ 目录加载失败，请检查网址是否正确。")
            return
        print("✅ 加载完成！你可以开始输入章节序号了。\n")

    while True:
        try:
            user_input = input("👉 请输入你想看的章节序号 (输入 q 退出): ")

            # 退出机制
            if user_input.lower() == 'q':
                print("退出阅读，再见！")
                break

            target_chapter = int(user_input)

            found_count = 0
            chapter_found = False

            # 遍历目录寻找对应的章节
            for chapter in ALL_CHAPTERS:
                title = chapter['title']
                if "章" in title:  # 过滤掉杂项
                    found_count += 1
                    if found_count == target_chapter:
                        print("\n" + "=" * 60)
                        print(f"📖【{title}】")
                        print("-" * 60)
                        content = get_content(chapter['url'])
                        print(content)
                        print("=" * 60 + "\n")
                        chapter_found = True
                        break  # 找到了就跳出遍历

            if not chapter_found:
                print(f"⚠️ 没找到第 {target_chapter} 章，可能是超出了总章节数。\n")

            time.sleep(0.5)  # 稍微停顿一下

        except ValueError:
            print("⚠️ 请输入纯数字！(例如 131)\n")
        except KeyboardInterrupt:
            print("\n程序已手动终止。")
            break


if __name__ == "__main__":
    main()