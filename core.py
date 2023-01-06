import random


class Game:
    # map = [
    #     [2, 0, 0, 2],
    #     [4, 2, 0, 2],
    #     [2, 4, 2, 4],
    #     [0, 4, 0, 4],
    # ]

    def __init__(self):
        self.map = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.generate(rand=False)
        self.generate(rand=False)

    def generate(self, rand=True) -> bool:
        # 找到0正常，找不到0 return False
        flag = False
        for line in self.map:
            for item in line:
                if item == 0:
                    flag = True
                    break
        if not flag:
            return flag

        x = random.randint(0, 3)
        y = random.randint(0, 3)
        while self.map[x][y] != 0:
            x = random.randint(0, 3)
            y = random.randint(0, 3)
        # print(x, y)
        if rand:
            self.map[x][y] = random.choice([2, 4])
        else:
            self.map[x][y] = 2
        return True

    def zero_to_end(self, line) -> bool:
        flag = False
        for i in range(len(line) - 1, -1, -1):
            if line[i] == 0:
                flag = True
                line.remove(line[i])
                line.append(0)
        return flag

    def merge(self, line) -> bool:
        flag = False
        flag = self.zero_to_end(line) or flag
        for i in range(len(line) - 1):
            if line[i] == line[i + 1]:
                flag = True
                line[i] += line[i]
                del line[i + 1]
                line.append(0)
        return flag

    def left_move(self) -> bool:
        flag = False
        for i in self.map:
            flag = self.merge(i) or flag
        return flag

    def right_move(self) -> bool:
        flag = False
        for i in self.map:
            tmp = i[::-1]
            flag = self.merge(tmp) or flag
            i[::-1] = tmp
        return flag

    def up_move(self) -> bool:
        flag = False
        self.matrix_transpose()
        flag = self.left_move() or flag
        self.matrix_transpose()
        return flag

    # 转置
    def matrix_transpose(self):
        new_map = [list(i) for i in zip(*self.map)]
        self.map[:] = new_map

    def down_move(self) -> bool:
        flag = False
        self.matrix_transpose()
        flag = self.right_move() or flag
        self.matrix_transpose()
        return flag

    def print(self):
        print("*" * 100)
        for i in self.map:
            print(i)

    def have_empty(self) -> bool:
        flag = False
        for line in self.map:
            if 0 in line:
                flag = True
                break
        return flag

    def movable(self):
        for line in self.map:
            for i in range(4-1):
                if line[i] == line[i+1]:
                    return True

        for i in range(len(self.map)):
            for j in range(len(self.map)-1):
                if self.map[j][i] == self.map[j+1][i]:
                    return True

        return False


if __name__ == '__main__':
    game = Game()
    game.print()
    print("*" * 100)
    # 调用变换函数
    game.right_move()
    # 输出变换后的map
    game.print()
