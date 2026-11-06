"""笔记记录"""
notes=[]
def note_display():
    print('*'*50)
    print()
    print('1.添加待办')
    print('2.查看待办')
    print('3.退出')
def note_add():
    note_time = input('输入截止时间：')
    note_content=input('输入你的待办内容：')
    note_state=input('输入你的完成情况：')
    note={
        '截止时间':note_time,
        '待办内容':note_content,
        '完成情况':note_state
    }
    notes.append(note)
    print('添加完成')
    """查询待办内容"""
def note_show():
    if not notes:
        print('暂无待办事项，请添加')
        return
    for note in notes:
        print()
        print('截止时间\t\t\t待办内容\t\t\t完成情况')
        print(f"{note['截止时间']}\t\t\t{note['待办内容']}\t\t\t{note['完成情况']}")
        note_edit(note)
        break
def note_edit(note):
    print()
    print('1.删除')
    print('2.编辑')
    cz=input('选择操作编号：')
    if cz=='1':
        notes.remove(note)
    elif cz=='2':
        note['截止时间']=input()
def main():
    while True:
        note_display()
        op=input('输入选项编号：')
        if op=='1':
            note_add()
        elif op=='2':
            note_show()
        elif op=='3':
            print("感谢使用!再见！")
            break
        input("\n按回车继续")
if __name__=='__main__':
    main()