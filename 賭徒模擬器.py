import random

m = 100    # 錢
a = 0      # 回合數 (天數)
pm = 0     # 賄賂警察次數
ro = 0     # 不賠錢機台次數
pa = 0     # 房屋保險單

print("=== 歡迎來到賭徒模擬器 ===")

while a < 30:
    print(f"\n--- 第 {a+1} 天 ---")
    q = input("要做點什麼? (work, steal, guess, bag, store, exit): ").lower()

    # --- 查詢類指令 (不消耗回合) ---
    if q == "bag":
        print("======== 你的背包 ========")
        print(f"💰 現金：{m} 元")
        print(f"👮 賄賂次數：{pm} 次")
        print(f"🎰 不賠錢機台：{ro} 個")
        print(f"🏠 房屋保險單：{pa} 張")
        print(f"📅 目前天數：第 {a} 輪")
        print("==========================")
        continue # 跳過後面的回合計算，直接回到迴圈開頭

    elif q == "store":
        print(f"歡迎來到商店！你現在有 {m} 元")
        print("1. 賄賂警察 (500元) - 失敗時免罰")
        print("2. 不賠錢機台 (750元) - 賭博失敗不扣錢")
        print("3. 房屋保險單 (1000元) - 免付一次房租")
        try:
            w = int(input("請輸入購買編號 (輸入0取消): "))
            if w == 1 and m >= 500:
                m -= 500; pm += 1; print("購買成功！")
            elif w == 2 and m >= 750:
                m -= 750; ro += 1; print("購買成功！")
            elif w == 3 and m >= 1000:
                m -= 1000; pa += 1; print("購買成功！")
            elif w == 0:
                print("離開商店")
            else:
                print("錢不夠或輸入錯誤")
        except:
            print("請輸入數字！")
        continue # 買東西也不消耗回合

    # --- 行動類指令 (會消耗回合 a += 1) ---
    action_happened = False # 用來標記是否真的做了消耗回合的動作

    if q == "work":
        n = random.randint(50, 100)
        print(f"你辛苦工作，獲得了 {n} 元")
        m += n
        action_happened = True

    elif q == "steal":
        r = random.randint(0, 100)
        if r > 90:
            print("偷竊成功！獲得 150 元")
            m += 150
        else:
            if pm > 0:
                print("偷竊失敗被逮！但你賄賂了警察，平安無事。")
                pm -= 1
            else:
                print("偷竊失敗！被罰款 150 元")
                m -= 150
        action_happened = True

    elif q == "guess":
        try:
            bet = int(input(f"你想賭多少錢？(目前餘額: {m}): "))
            if bet > m or bet <= 0:
                print("金額不合法！")
            else:
                s = random.randint(1, 10)
                t = int(input("猜一個 1-10 的數字: "))
                if t == s:
                    print(f"猜對了！贏得 {bet} 元")
                    m += bet
                else:
                    if ro > 0:
                        print("猜錯了！幸好有機台保護，沒賠錢。")
                        ro -= 1
                    else:
                        print(f"猜錯了！賠了 {bet} 元")
                        m -= bet
                action_happened = True
        except:
            print("請輸入數字！")

    elif q == "exit":
        break

    # --- 結算回合 (只有執行行動後才執行) ---
    if action_happened:
        a += 1
        
        # 檢查是否破產
        if m <= 0:
            print("\n你破產了！遊戲結束。")
            break
            
        # 房租機制 (每 4 輪一次)
        if a % 4 == 0:
            print("\n🔔 房東敲門了！")
            if pa > 0:
                print("你有房屋保險單，這期房租免了！")
                pa -= 1
            else:
                if m >= 200:
                    print("支付房租 200 元。")
                    m -= 200
                else:
                    print("你付不起房租，被踢出家門！")
                    m = 0 # 標記破產
                    break

# 遊戲最終判定
if m > 0 and a >= 30:
    print(f"\n恭喜通關！你成功撐過了 30 輪，最後財產：{m}")
else:
    print(f"\n遊戲結束。最後紀錄：第 {a} 輪，財產：{m}")