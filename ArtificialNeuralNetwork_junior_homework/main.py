import random
import math

# 学习速度
η = 0.2
# 正交输入模式集
quadrature_inputs = (
    ((1, 0, 0, 0), -1),
    ((0, 1, 0, 0), 1),
    ((0, 0, 1, 0), 2),
    ((0, 0, 0, 1), 4),
)
# 最大误差
MAX_ERROR = 10e-5
# 最大学习次数
MAX_LOOP = 127


class Neuron(object):
    def __init__(self, p_name: str):
        self.name = p_name
        self.weight = random.randint(0, 0)

    def set_weight(self, p_weight):
        if p_weight == 0:
            return
        self.weight += p_weight
        print("\t神经{}修改权重: {} -> {}".format(self.name, self.weight - p_weight, self.weight))


def error_index(quadrature_inputs, neurons):
    outputs = []
    for single_input in quadrature_inputs:
        data = single_input[0]
        temp_sum = 0
        for i in range(len(neurons)):
            temp_sum += data[i] * neurons[i].weight
        outputs.append(temp_sum)

    temp_sum = 0
    for i in range(len(quadrature_inputs)):
        target = quadrature_inputs[i][1]
        temp_sum += (target - outputs[i]) ** 2
    e = math.sqrt(temp_sum)
    print("\n计算目标值与网络输出误差：{}".format(e))
    return e


def main():
    neurons = [Neuron(str(i)) for i in range(4)]
    loop_counter = 0
    while True:
        if math.fabs(error_index(quadrature_inputs, neurons)) <= math.fabs(MAX_ERROR):  # 是否达到误差要求
            break
        if loop_counter > MAX_LOOP:  # 如果达不到误差要求，检查最大循环次数要求
            break
        else:
            print("第{}轮学习".format(loop_counter + 1))
            loop_counter += 1
        # 开始学习
        for i in range(len(quadrature_inputs)):
            a = quadrature_inputs[i][0]
            t = quadrature_inputs[i][1]
            for j in range(len(neurons)):
                wij = η * a[j] * t
                neurons[j].set_weight(wij)

    print("\n\t".join([
        "学习成功!",
        "共训练{}次".format(loop_counter),
        "权重为{}".format([x.weight for x in neurons])
    ]))


if __name__ == '__main__':
    main()
