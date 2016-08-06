"""
test 2048
"""
import msvcrt
import random

flajs = {"proceeding": 0, "lose": 1, "win": 2}  # flaj 是一个梗，详见B站超炮弹幕
game_flaj = flajs["proceeding"]
WIN_NUMBER = 2048


class The2048Panel(object):
    def __init__(self, p_data):
        self.data = p_data
        self.height = len(p_data)
        self.width = len(p_data[0])
        self.change_flag = False

    def generate(self):
        while True:
            random_row = random.randint(0, 3)
            random_column = random.randint(0, 3)
            if self.data[random_row][random_column] == 0:
                self.data[random_row][random_column] = 2
                break

    def check_game_status(self):
        empty_block_count = 0
        for x in range(self.width):
            for y in range(self.height):
                if self.data[x][y] == WIN_NUMBER:
                    global game_flaj
                    game_flaj = flajs["win"]
                    return
                if self.data[x][y] == 0:
                    empty_block_count += 1

        if empty_block_count == 0:
            global game_flaj
            game_flaj = flajs["lose"]

    def change(self, direction: str):
        '''
        When the user presses tke key,
        :param direction: "U" for up, "D" for down, "L" for left, "R" for right
        :return:
        '''
        self.change_flag = False
        if direction == "U":
            for x in range(self.height):  # 自上而下、自左而右相加
                for y in range(self.width):
                    for down_num in range(1, 4):  # 向上查看的格数
                        if self.data[x][y] != 0 and (self.height - 1) - x >= down_num:
                            if self.data[x][y] == self.data[x + down_num][y]:
                                self.data[x][y] = self.data[x + down_num][y] * 2
                                self.data[x + down_num][y] = 0
                                self.change_flag = True
                                break
                            elif self.data[x + down_num][y] != 0:
                                break
            for times in range(4):  # 上浮4次
                for x in range(self.height):
                    for y in range(self.width):
                        if self.data[x][y] != 0 and x > 0:
                            if self.data[x - 1][y] == 0:
                                self.data[x - 1][y], self.data[x][y] = self.data[x][y], self.data[x - 1][y]  # 互换
                                self.change_flag = True
        elif direction == "D":
            for x in range(self.height - 1, -1, -1):  # 自下而上、自右而左相加
                for y in range(self.width - 1, -1, -1):
                    for up_num in range(1, 4):  # 向上查看的格数
                        if self.data[x][y] != 0 and x >= up_num:
                            if self.data[x][y] == self.data[x - up_num][y]:
                                self.data[x][y] = self.data[x - up_num][y] * 2
                                self.data[x - up_num][y] = 0
                                self.change_flag = True
                                break
                            elif self.data[x - up_num][y] != 0:
                                break
            for times in range(4):  # 下沉4次
                for x in range(self.height - 1, -1, -1):
                    for y in range(self.width - 1, -1, -1):
                        if self.data[x][y] != 0 and x < 3:
                            if self.data[x + 1][y] == 0:
                                self.data[x + 1][y], self.data[x][y] = self.data[x][y], self.data[x + 1][y]  # 互换
                                self.change_flag = True
        elif direction == "L":
            for y in range(len(self.data[0])):  # 自左而右、自上而下相加
                for x in range(len(self.data)):
                    for right_num in range(1, 4):  # 向右查看的格数
                        if self.data[x][y] != 0 and (self.width - 1) - y >= right_num:
                            if self.data[x][y] == self.data[x][y + right_num]:
                                self.data[x][y] = self.data[x][y + right_num] * 2
                                self.data[x][y + right_num] = 0
                                self.change_flag = True
                                break
                            elif self.data[x][y + right_num] != 0:
                                break
            for times in range(4):  # 左移4次
                for y in range(self.width):
                    for x in range(self.height):
                        if self.data[x][y] != 0 and y > 0:
                            if self.data[x][y - 1] == 0:
                                self.data[x][y - 1], self.data[x][y] = self.data[x][y], self.data[x][y - 1]  # 互换
                                self.change_flag = True
        elif direction == "R":
            for y in range(self.width - 1, -1, -1):  # 自右而左、自上而下相加
                for x in range(self.height):
                    for left_num in range(1, 4):  # 向左查看的格数
                        if self.data[x][y] != 0 and y >= left_num:
                            if self.data[x][y] == self.data[x][y - left_num]:
                                self.data[x][y] = self.data[x][y - left_num] * 2
                                self.data[x][y - left_num] = 0
                                self.change_flag = True
                                break
                            elif self.data[x][y - left_num] != 0:
                                break
            for times in range(4):  # 右移4次
                for y in range(self.width - 1, -1, -1):
                    for x in range(self.height):
                        if self.data[x][y] != 0 and y < 3:
                            if self.data[x][y + 1] == 0:
                                self.data[x][y + 1], self.data[x][y] = self.data[x][y], self.data[x][y + 1]  # 互换
                                self.change_flag = True
        # 在空白区域随机生成一个2
        if self.change_flag is True:
            self.generate()

    def __str__(self):
        self.check_game_status()
        if game_flaj == flajs["proceeding"]:
            print_str = "\n" * 10
            print_str += "-" * 4 * 9 + "-\n"
            for row in self.data:
                print_str += "|{}|{}|{}|{}|\n".format(" " * 8, " " * 8, " " * 8, " " * 8)
                print_str += "|{:^8}|{:^8}|{:^8}|{:^8}|\n".format(
                    *["" if column == 0 else str(column) for column in row])
                print_str += "|{}|{}|{}|{}|\n".format(" " * 8, " " * 8, " " * 8, " " * 8)
                print_str += "-" * 4 * 9 + "-\n"
            return print_str
        elif game_flaj == flajs["lose"]:
            return "You lose!"
        elif game_flaj == flajs["win"]:
            return "You win!"
        else:
            raise Exception("unknown game status: {}".format(game_flaj))


def main():
    a = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    a = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1024, 0, 0, 0],
        [1024, 0, 0, 0],
    ]
    panel = The2048Panel(a)
    panel.generate()
    print(panel)
    debug = False
    while game_flaj == flajs["proceeding"] and not debug:
        t = msvcrt.getch()
        if t == b'H':
            panel.change("U")
        elif t == b'P':
            panel.change("D")
        elif t == b'K':
            panel.change("L")
        elif t == b'M':
            panel.change("R")
        print(panel)
    input()


if __name__ == '__main__':
    main()
