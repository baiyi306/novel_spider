# 名片管理系统
cards=[]
version=1.0
def card_menu():
    """菜单选择"""
    print('*' * 35)
    print(f'欢迎使用【名片管理系统】V{version}')
    print()
    print('1.新建名片')
    print('2.显示全部')
    print('3.查询名片')
    print()
    print('0.退出系统')
    print('*' * 35)

def card_new():
    """新建名片"""
    print('新建名片')
    card_name = input('输入名字：')
    card_position = input('输入职位：')
    card_Tel = input('输入电话：')
    card_QQ = input('输入QQ：')
    card = {
        'card_name':card_name,
        'card_position':card_position,
        'card_Tel':card_Tel,
        'card_QQ':card_QQ
    }
    cards.append(card)
    print(f'{card_name}的名片添加成功')

def card_all():
    """显示全部"""
    if len(cards)==0:
        print('目前还没有任何名片')
        return
    """显示表头"""
    print('姓名\t\t职位\t\t电话\t\tQQ')
    for card in cards:
        print(f"{card['card_name']}\t\t{card['card_position']}\t\t{card['card_Tel']}\t\t{card['card_QQ']}")

def card_find():
    """查询名片"""
    find_name=input('输入你要查询的名字')
    found = False
    for card in cards:
        if card['card_name']==find_name:
            print(f'找到{find_name}的信息如下')
            print('姓名\t\t职位\t\t电话\t\tQQ')
            print(f"{card['card_name']}\t\t{card['card_position']}\t\t{card['card_Tel']}\t\t{card['card_QQ']}")
            card_handle(card)
            found = True
            break
    if not found:
        print(f'没有找到【{find_name}】的信息')
def card_handle(card):
    """对查询到的名片进行修改或删除"""
    while True:
        print('\t请选择你要执行的操作：')
        print('1.修改')
        print('2.删除')
        print('0.返回上一级')

        choose=input('输入操作的编号：')
        if choose=='1':
            #修改名片
            new_name=input(f"输入新的姓名【{card['card_name']}】:") or card['card_name']
            new_position=input(f"输入新的职位【{card['card_position']}】:") or card['card_position']
            new_Tel=input(f"输入新的电话【{card['card_Tel']}】:") or card['card_Tel']
            new_QQ=input(f"输入新的QQ【{card['card_QQ']}】:") or card['card_QQ']

            card['card_name']=new_name
            card['card_position']=new_position
            card['card_Tel']=new_Tel
            card['card_QQ']=new_QQ
            print('修改成功')
            break
        elif choose=='2':
            """删除名片"""
            cards.remove(card)
            print('删除成功')
            break
        elif choose=='0':
            """返回上一级"""
            break
        else:
            print('输入有误，请重新选择')
def main():
    """主程序入口"""
    while True:
        card_menu()
        choose=input('输入你要操作的编号：')
        if choose=='1':
            card_new()
        elif choose=='2':
            card_all()
        elif choose=='3':
            card_find()
        elif choose=='0':
            print('退出系统，感谢使用')
            break
        else:
            print('输入有误，请重新选择')
        input('\n按回车继续：')

if __name__ == '__main__':
    main()













