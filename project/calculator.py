"""简易计算器"""
def calculator():
    print('*'*50)
    print('简易计算器（+，-，*，/）')
    try:
        num1=int(input('输入你的数据1:'))
        op=input('输入符号（+，-，*，/）：')
        num2=int(input('输入你的数据2:'))
        if op=='+':
            print(f'结果：{num1+num2}')
        elif op=='-':
            print(f'结果：{num1-num2}')
        elif op=='*':
            print(f'结果：{num1*num2}')
        elif op=='/':
            if num2==0:
                print('除数不能为0')
            else:
                print(f'结果：{num1/num2}')
        else:
            print('请输入有效运算符')
    except ValueError:
        print('请输入有效数字')
calculator()
