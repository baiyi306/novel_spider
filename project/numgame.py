"""猜数字游戏"""
import random
def game_num():
    print('小游戏为猜数字游戏，需要猜整数，（0～100），猜中即通关！\n游戏开始')
    generatednum = random.randint(1,100)
    count=0
    while True:
        try:
            younum=int(input('输入你猜的数：'))
            count+=1
            if younum>generatednum:
                print('大了!再试试')
            elif younum<generatednum:
                print('小了！再试试')
            else:
                print (f'恭喜你猜对了！总共猜了{count}次\n游戏结束！通关')
                break
        except ValueError:
            print('请输入正确的整数')
game_num()
