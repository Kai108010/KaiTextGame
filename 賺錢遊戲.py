import random
m=100
a=0
pm=0
ro=0
pa=0
while a!=30:
    q=input("要做點什麼?")
    if q=="work":
        n=random.randint(50,100)
        print("你獲得了" + str(n) + "元")
        m=m+n
    elif q=="steal":
        r=random.randint(0,100)
        if r>90:
            print("你偷竊成功了 因此你獲得了" + str(150) + "元")
            m=m+150
        else:
            if pm>0:
                print("你偷竊失敗了 因此你被警察逮捕了 但是你賄賂了警察 因此你沒有被罰")
                pm=pm-1
            else:   
                print("你偷竊失敗了 因此你被罰了" + str(150) + "元")
                m=m-150
    elif q=="money":
        print("你現在有" + str(m) + "元")
    elif q == "guess":
        bet = int(input(f"你現在有 {m} 元，想下注多少？"))
        
        if bet > m:
            print("你沒那麼多錢可以賭！")
        elif bet <= 0:
            print("請輸入正確的金額。")
        else:
            s = random.randint(1, 5)
            t = int(input("請猜 1-5 其中一個數字："))
            
            if t == s:
                # 贏了獲得賭注的兩倍
                reward = bet * 2
                print(f"🎊 恭喜！你猜對了，贏得 {reward} 元！")
                m += reward
            else:
                if ro > 0:
                    print(" 猜錯了！幸好你有【不賠錢機台】，保住了你的錢。")
                    ro -= 1
                else:
                    print(f" 慘！你猜錯了，損失了下注的 {bet} 元。")
                    m -= bet
    elif q=="store":
        print("歡迎來到商店 你可以購買以下物品 你現在有" + str(m) + "元")
        print("1.賄賂警察 500元")
        print("2.不賠錢機台 750元")
        print("3.房屋保險單 1000元")
        w=int(input("請輸入你要購買的物品編號"))
        if w==1:
            if m>=500:
                print("你購買了賄賂警察")
                m=m-500
                pm=pm+1
            else:
                print("你的錢不夠")
        elif w==2:
            if m>=750:
                print("你購買了不賠錢機台")
                m=m-750
                ro=ro+1
            else:
                print("你的錢不夠")
        elif w==3:
            if m>=1000:
                print("你購買了房屋保險單")
                m=m-1000
                pa=pa+1
            else:
                print("你的錢不夠")
    a=a+1
    if m<=0:
        print("你破產了 遊戲結束")
        break
    if a&3==0:
        if pa>0:
            print("房東來了 你需要支付房租 但是你有房屋保險單 因此你不需要支付房租 但是你的房屋保險單不能再用了")
            pa=pa-1
        else:
            if m>=200:
                print("房東來了 你需要支付房租 因此你損失了" + str(200) + "元")
                m=m-200
            else:
                print("房東來了 你需要支付房租 但你破產了 因此你被房東趕出了家門 遊戲結束")
                break

if m > 0 and a >= 30:   # 如果錢還夠且撐過 30 輪
    print("遊戲結束 你贏了！成功撐過 30 輪，你最後有 " + str(m) + " 元")
else:    
    print("遊戲結束 你輸了... 總共玩了 " + str(a) + " 輪，你最後有 " + str(m) + " 元")
    