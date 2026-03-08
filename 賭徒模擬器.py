import random

m = 100    # 身上現金
bm = 0     # 銀行存款 (新增)
a = 0      # 回合數 (天數)
pm = 0     # 賄賂警察次數
ro = 0     # 不賠錢機台次數
pa = 0     # 房屋保險單
heat = 0   # 警戒值
inf = 1.0  # 通膨倍率 (新增，初始為 1.0 倍)

# 偷竊目標資料結構
steal_targets = {
    'drunk': {
        'name': '路邊醉漢',
        'base_prob': 0.85,
        'min_reward': 20, 'max_reward': 50,
        'fine': 50,
        'heat_add': 10
    },
    'store': {
        'name': '雜貨店',
        'base_prob': 0.55,
        'min_reward': 150, 'max_reward': 300,
        'fine': 200,
        'heat_add': 25
    },
    'bank': {
        'name': '銀行',
        'base_prob': 0.20,
        'min_reward': 800, 'max_reward': 1500,
        'fine': 1000,
        'heat_add': 50
    }
}

# Helper function to calculate typing errors
def calculate_typing_errors(expected_phrase, typed_phrase):
    errors = abs(len(expected_phrase) - len(typed_phrase))
    min_len = min(len(expected_phrase), len(typed_phrase))
    for i in range(min_len):
        if expected_phrase[i] != typed_phrase[i]:
            errors += 1
    return errors

print("=== 歡迎來到賭徒模擬器 (通膨生存版) ===")

while a < 30:
    print(f"\n--- 第 {a+1} 天 ---")
    if heat > 0:
        print(f"🚨 目前城市警戒值: {heat}/100")
    if inf > 1.0:
        print(f"📈 目前物價通膨率: {(inf - 1.0) * 100:.0f}% (商店與房租變貴了！)")
        
    q = input("要做點什麼? (work, steal, gamble, bank, bag, store, exit): ").lower()

    if q == "bag":
        print("======== 你的背包 ========")
        print(f"💰 現金：{m} 元")
        print(f"🏦 銀行存款：{bm} 元")
        print(f"👮 賄賂次數：{pm} 次")
        print(f"🎰 不賠錢機台：{ro} 個")
        print(f"🏠 房屋保險單：{pa} 張")
        print(f"🚨 城市警戒值：{heat}/100")
        print(f"📈 目前通膨倍率：{inf:.2f}x")
        print(f"📅 目前天數：第 {a} 輪")
        print("==========================")
        continue
        
    elif q == "bank":
        print(f"\n--- 🏦 國民銀行 ---")
        print(f"目前活存利率：每日 2%")
        print(f"身上的現金：{m} 元 | 銀行存款：{bm} 元")
        try:
            act = input("要 存款(1) 還是 提款(2)？(輸入0離開): ")
            if act == '1':
                amt = int(input("輸入存款金額: "))
                if 0 < amt <= m:
                    m -= amt; bm += amt; print(f"成功存入 {amt} 元！")
                else: print("金額無效或現金不足！")
            elif act == '2':
                amt = int(input("輸入提款金額: "))
                if 0 < amt <= bm:
                    bm -= amt; m += amt; print(f"成功提出 {amt} 元！")
                else: print("金額無效或存款不足！")
            elif act == '0': print("離開銀行。")
            else: print("無效的選擇！")
        except: print("請輸入數字！")
        continue

    elif q == "store":
        # 商店價格隨通膨浮動
        p_bribe = int(500 * inf)
        p_ro = int(750 * inf)
        p_pa = int(1000 * inf)
        
        print(f"歡迎來到商店！你現在身上有 {m} 元 (價格已受通膨影響)")
        print(f"1. 賄賂警察 ({p_bribe}元) - 失敗時免罰")
        print(f"2. 不賠錢機台 ({p_ro}元) - 賭博失敗不扣錢")
        print(f"3. 房屋保險單 ({p_pa}元) - 免付一次房租")
        try:
            w = int(input("請輸入購買編號 (輸入0取消): "))
            if w == 1 and m >= p_bribe: m -= p_bribe; pm += 1; print("購買成功！")
            elif w == 2 and m >= p_ro: m -= p_ro; ro += 1; print("購買成功！")
            elif w == 3 and m >= p_pa: m -= p_pa; pa += 1; print("購買成功！")
            elif w == 0: print("離開商店")
            else: print("錢不夠或輸入錯誤")
        except: print("請輸入數字！")
        continue

    action_happened = False

    if q == "work":
        heat = max(0, heat - 15)
        print("你選擇了安分工作，城市警戒值下降了！(但薪水沒有因為通膨變多...)")
        
        typing_phrases = ["我今天要好好的服從老闆", "努力工作才能賺大錢", "客人永遠是對的", "準時下班是我的目標", "工作帶來成就感"]
        phrase_to_type = random.choice(typing_phrases)
        print(f"請輸入以下句子來工作：\n「{phrase_to_type}」")
        user_typed = input("你的輸入：")
        if user_typed == phrase_to_type:
            n = random.randint(100, 150)
            print(f"你打字正確，獲得了 {n} 元！")
        else:
            num_errors = calculate_typing_errors(phrase_to_type, user_typed)
            if num_errors >= 5: n = 0; print(f"你打字錯誤太多 ({num_errors} 處)，沒有獲得報酬。")
            else:
                base_earnings = random.randint(100, 150)
                deduction = num_errors * 10
                n = max(0, base_earnings - deduction)
                print(f"打字錯誤 ({num_errors} 處)，獲得 {n} 元。")
        m += n
        action_happened = True

    elif q == "steal":
        print("\n--- 選擇你的偷竊目標 ---")
        for key, target in steal_targets.items():
            actual_prob = max(0.05, target['base_prob'] - (heat * 0.005))
            print(f"[{key.upper()}] {target['name']}: 實際成功率 {int(actual_prob*100)}%, 預估獎勵 {target['min_reward']}~{target['max_reward']}元, 罰款 {target['fine']}元")
        
        chosen = input("請輸入目標關鍵字: ").lower()
        if chosen not in steal_targets:
            print("無效的目標！")
            continue
            
        target = steal_targets[chosen]
        actual_prob = max(0.05, target['base_prob'] - (heat * 0.005))
        
        if random.random() <= actual_prob:
            reward = random.randint(target['min_reward'], target['max_reward'])
            print(f"✅ 偷竊成功！在 {target['name']} 獲得了 {reward} 元！")
            m += reward
            heat = min(100, heat + target['heat_add'])
            print(f"🚨 你的犯行引起了注意，警戒值上升了 {target['heat_add']} 點！")
        else:
            print(f"❌ 糟糕！你在 {target['name']} 被發現了！")
            if pm > 0:
                print("警車來了，但你偷偷塞了錢給認識的警察...")
                print("你消耗了 1 次賄賂，平安無事，但被警告近期安分點。")
                pm -= 1
            else:
                choice = input("你要乖乖繳交罰款 (輸入 1)，還是拔腿就跑 (輸入 2)？: ")
                if choice == '2':
                    if random.random() <= 0.4:
                        print("🏃‍♂️ 驚險刺激！你翻過了巷子的牆，成功甩掉了追兵！(未扣錢)")
                        heat = min(100, heat + 20)
                    else:
                        penalty = target['fine'] * 2
                        print(f"🚓 逃跑失敗！你被警察撲倒在地，罰款加倍！扣除現金 {penalty} 元！")
                        m -= penalty
                else:
                    print(f"💸 你無奈地舉起雙手，被扣除現金 {target['fine']} 元。")
                    m -= target['fine']
        action_happened = True

    elif q == "gamble":
        print("\n--- 🎰 歡迎來到地下賭場 ---")
        print("1. 🎲 擲骰大小 (勝率 50%，賠率 1:1)")
        print("2. 🔢 幸運數字 (勝率 20%，賠率 1:4)")
        print("3. 🔫 俄羅斯輪盤 (免賭金！83.3% 贏 500 元，16.7% 直接破產)")
        print("0. 離開賭場")
        
        try:
            g_choice = input("請選擇你要玩的遊戲 (0-3): ")
            if g_choice == '0': continue
            elif g_choice == '1':
                bet = int(input(f"你想賭多少錢？(目前餘額: {m}): "))
                if bet > m or bet <= 0: print("金額不合法！")
                else:
                    guess = input("猜大 (大於3) 還是猜小 (小於等於3)？(輸入 '大' 或 '小'): ")
                    dice = random.randint(1, 6)
                    print(f"🎲 骰子停在了【 {dice} 】！")
                    is_big = dice > 3
                    if (guess == '大' and is_big) or (guess == '小' and not is_big):
                        print(f"🎉 猜對了！贏得 {bet} 元")
                        m += bet
                    else:
                        if ro > 0: print("幸好有機台保護，沒賠錢。"); ro -= 1
                        else: print(f"💸 猜錯了！賠了 {bet} 元"); m -= bet
                    action_happened = True
            elif g_choice == '2':
                bet = int(input(f"你想賭多少錢？(目前餘額: {m}): "))
                if bet > m or bet <= 0: print("金額不合法！")
                else:
                    s = random.randint(1, 5)
                    t = int(input("猜一個 1-5 的數字: "))
                    if t == s:
                        print(f"🎉 幸運女神眷顧！贏得 {bet * 4} 元！")
                        m += bet * 4
                    else:
                        if ro > 0: print("幸好有機台保護，沒賠錢。"); ro -= 1
                        else: print(f"💸 猜錯了！賠了 {bet} 元"); m -= bet
                    action_happened = True
            elif g_choice == '3':
                print("🔫 你拿起了一把左輪手槍，裡面只有一顆子彈...")
                input("按 Enter 鍵扣下扳機...")
                if random.randint(1, 6) == 1:
                    print("💥 砰！你中彈了！你身上的現金全部歸零...")
                    if ro > 0: print("「不賠錢機台」抵銷了致命傷！(消耗 1 個保護)"); ro -= 1
                    else: m = 0
                    action_happened = True
                else:
                    print("😅 咔嚓！是空槍！你在生死邊緣活了下來，獲得 500 元！")
                    m += 500
                    action_happened = True
            else: print("無效的選擇！")
        except: print("輸入錯誤！")

    elif q == "exit": break

    # 回合結算與事件
    if action_happened:
        a += 1
        
        # 結算銀行利息與通膨
        if bm > 0:
            interest = int(bm * 0.02)
            bm += interest  # 每日 2% 複利
        inf += 0.05  # 每天物價上漲 5%
        
        if m < 0: 
            print("\n💀 你身上的現金變成負數，被黑道抓走了！遊戲結束。")
            break
            
        if heat > 0: heat = max(0, heat - 2)

        if a % 4 == 0:
            current_rent = int(200 * inf) # 房租也受通膨影響！
            print(f"\n🔔 房東敲門了！(本期房租因通膨漲到了 {current_rent} 元)")
            if pa > 0: 
                print("你有房屋保險單，免付本期房租！"); pa -= 1
            else:
                if m >= current_rent: 
                    print(f"從現金支付房租 {current_rent} 元。")
                    m -= current_rent
                else: 
                    print(f"你身上的現金付不起 {current_rent} 元的房租！")
                    if bm >= current_rent:
                        print("房東發現你有銀行存款，強行拉著你去提款繳房租！")
                        bm -= current_rent
                    else:
                        print("你連銀行裡都沒錢，被踢出家門！遊戲結束！")
                        m = 0; break

if (m + bm) > 0 and a >= 30: 
    print(f"\n🏆 恭喜通關！最後總資產：{m + bm} 元")
elif (m + bm) <= 0: 
    print(f"\n遊戲結束。最後紀錄：第 {a} 輪破產。")
else:
    print(f"\n遊戲結束。最後紀錄：第 {a} 輪，總資產：{m + bm} 元")