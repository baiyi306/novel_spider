# 全局变量：存储所有名片，每个名片是一个字典
cards = []


def show_menu():
    """显示欢迎界面和功能菜单"""
    print("*" * 50)
    print("欢迎使用【名片管理系统】V1.0")
    print()
    print("1. 新建名片")
    print("2. 显示全部")
    print("3. 查询名片")
    print()
    print("0. 退出系统")
    print("*" * 50)


def new_card():
    """新建名片"""
    print("【新建名片】")
    name = input("请输入姓名：")
    phone = input("请输入电话：")
    qq = input("请输入QQ：")
    email = input("请输入邮件：")

    # 构建名片字典
    card = {
        "name": name,
        "phone": phone,
        "qq": qq,
        "email": email
    }

    cards.append(card)
    print(f"名片【{name}】添加成功！")


def show_all():
    """显示全部名片"""
    if len(cards) == 0:
        print("当前没有任何名片记录！")
        return

    # 打印表头
    print("-" * 50)
    print("姓名\t\t电话\t\tQQ\t\t\t邮件")
    print("=" * 50)

    for card in cards:
        print(f"{card['name']}\t\t{card['phone']}\t\t{card['qq']}\t\t{card['email']}")

    print("-" * 50)


def search_card():
    """查询名片"""
    print("【查询名片】")
    find_name = input("请输入要查询的姓名：")

    for card in cards:
        if card["name"] == find_name:
            print("找到了！名片信息如下：")
            print("-" * 50)
            print("姓名\t\t电话\t\tQQ\t\t\t邮件")
            print("=" * 50)
            print(f"{card['name']}\t\t{card['phone']}\t\t{card['qq']}\t\t{card['email']}")
            print("-" * 50)

            # 查询到后，提供修改/删除选项
            handle_card(card)
            break
    else:
        print(f"没有找到姓名为【{find_name}】的名片！")


def handle_card(card):
    """对查询到的名片进行修改或删除操作"""
    while True:
        print("\n请选择要执行的操作：")
        print("1. 修改名片")
        print("2. 删除名片")
        print("0. 返回上一级")

        choice = input("请输入操作编号：")

        if choice == "1":
            # 修改名片
            print("【修改名片】（直接回车表示不修改该项）")
            new_name = input(f"请输入新姓名[{card['name']}]：") or card["name"]
            new_phone = input(f"请输入新电话[{card['phone']}]：") or card["phone"]
            new_qq = input(f"请输入新QQ[{card['qq']}]：") or card["qq"]
            new_email = input(f"请输入新邮件[{card['email']}]：") or card["email"]

            card["name"] = new_name
            card["phone"] = new_phone
            card["qq"] = new_qq
            card["email"] = new_email
            print("名片修改成功！")
            break

        elif choice == "2":
            # 删除名片
            cards.remove(card)
            print("名片已删除！")
            break

        elif choice == "0":
            # 返回上一级
            break

        else:
            print("输入有误，请重新选择！")


def main():
    """主程序入口"""
    while True:
        show_menu()
        choice = input("请输入功能编号：")

        if choice == "1":
            new_card()
        elif choice == "2":
            show_all()
        elif choice == "3":
            search_card()
        elif choice == "0":
            print("退出系统，感谢使用！")
            break
        else:
            print("输入有误，请重新选择！")

        # 按回车继续
        input("\n按回车键继续...")


if __name__ == "__main__":
    main()