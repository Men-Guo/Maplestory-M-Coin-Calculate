import random
import datetime

fight = 160
card = [200, 190, 180, 170, 150]
swim = [80, 85, 90, 95, 100, 110, 120, 140, 160, 200]


class secondcoin(object):
    def __init__(self, day_count, coin, coin_remain, print_sign):
        self.day_count = day_count
        self.coin = coin
        self.wheel = [0, 0, 0, 0, 0, 0, 0, 0]
        self.wheel_count = 0
        self.tri = True
        self.print_sign = print_sign
        self.day = datetime.date(2020,7,28)

    def daily_extra_check(self):
        # 每日送 50 币
        today_coin = 0
        if self.day_count >= 3:
            self.coin += 50
            today_coin += 50
        self.day_count += 1
        self.day += datetime.timedelta(days=1)
        # 第一次七日签到送 1000, 后续登陆签到送4000 总计 5000
        if self.day_count in [6, 7, 11, 13, 18]:
            self.coin += 1000
            today_coin += 1000
            if self.print_sign: print('第{0}天, 送1000币'.format(self.day_count))
        # 第二次七日签到送3500，登陆签到送 2000, 共计5500
        if self.day_count == 22:
            self.coin += 3500
            today_coin += 3500
            if self.print_sign: print('第{0}天, 送3500币'.format(self.day_count))
        # 登陆送2000, 共计4000
        if self.day_count in [20, 25, 27]:
            self.coin += 2000
            today_coin += 2000
            if self.print_sign: print('第{0}天, 送2000币'.format(self.day_count))
        # 登陆第七天补偿 500, 但是少一次one card活动
        if self.day_count == 7:
            self.coin += 500
            today_coin += 500
            miss_card = random.choice(card)
            self.coin -= miss_card
            if self.print_sign: print('第{0}天, 补偿500币'.format(self.day_count))
        # 蛋糕活动 每日有150
        if 9 <= self.day_count <= 22:
            self.coin += 150
            today_coin += 150
        # 蛋糕活动第10次, 第20次 送700
        if self.day_count in [13, 16]:
            self.coin += 700
            today_coin += 700
            if self.print_sign: print('第{0}天, 蛋糕700币'.format(self.day_count))
        return today_coin

    def print_information(self, today_coin, level):
        print('时间为：{0}'.format(self.day))
        print("VIP{1},第{0}天".format(self.day_count,level))
        print('今日获得硬币数:{0}'.format(today_coin))
        print("硬币数量:{0}".format(self.coin))
        print("\n")

    @property
    def simulate_coin(self):
        if self.day_count != 31:
            daily_coin = self.daily_extra_check()
            if self.day_count <= 16:
                if 0 <= self.coin <= 4000:
                    todays_coin = 550 + random.choice(card) + random.choice(swim) + fight
                    self.coin += todays_coin
                    self.coin_remain = self.coin
                    if self.print_sign: self.print_information(todays_coin+daily_coin,'经典')
                    self.simulate_coin
                if 4000 < self.coin <= 17000:
                    todays_coin = 650 + random.choice(card) + random.choice(swim) + fight + random.choice(card)
                    self.coin += todays_coin
                    if self.print_sign: self.print_information(todays_coin+daily_coin,'精英')
                    self.simulate_coin
                if 17000 < self.coin <= 37000:
                    todays_coin = 800 + random.choice(card) + random.choice(swim) + random.choice(
                        swim) + fight * 2 + random.choice(card)
                    self.coin += todays_coin
                    if self.print_sign: self.print_information(todays_coin+daily_coin,'尊荣')
                    self.simulate_coin
            if self.day_count > 16:
                if 4000 < self.coin <= 17000:
                    todays_coin = 650 + random.choice(swim) + fight + self.reel()
                    self.coin += todays_coin
                    if self.print_sign: self.print_information(todays_coin+daily_coin,'经典')
                    self.simulate_coin
                if 17000 < self.coin <= 37000:
                    todays_coin = 800 + random.choice(swim) + random.choice(swim) + fight * 3 + self.reel()
                    self.coin += todays_coin
                    if self.print_sign: self.print_information(todays_coin+daily_coin,'精英')
                    self.simulate_coin
                if self.coin > 37000 and self.day_count < 31:
                    todays_coin = 1000 + random.choice(swim) + random.choice(swim) + fight * 3 + self.reel()
                    self.coin += todays_coin
                    if self.print_sign: self.print_information(todays_coin+daily_coin,'威望')
                    self.simulate_coin
        return self.coin

    def reel(self):
        daily_coin = 0
        for _ in range(7):
            index = random.choice(range(8))
            if self.wheel[index] == 0:
                daily_coin += 50
            if self.wheel[index] == 2:
                daily_coin += 70
            self.wheel[index] += 1
            if 4 in self.wheel:
                self.wheel = [0, 0, 0, 0, 0, 0, 0, 0]
                self.wheel_count += 1
                if self.wheel_count > 4:
                    daily_coin += 100

        if self.wheel_count == 2 and self.tri:
            daily_coin += 300
            self.tri = False
        if self.wheel_count == 4 and not self.tri:
            daily_coin += 3500
        return daily_coin

if __name__ == '__main__':
    a = secondcoin(0, 0, 0, True)
    a.simulate_coin

    avg_coin = 0
    for i in range(0, 10000, 1):
        a = secondcoin(0, 0, 0, False)
        d = a.simulate_coin
        avg_coin += d
    avg_coin = avg_coin/len(range(0,10000,1))
    print('最终可获取硬币平均值为:{0}'.format(avg_coin))
