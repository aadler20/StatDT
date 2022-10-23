from sympy import diff, evalf, symbols
import matplotlib.pyplot as plt
import numpy as np
import random

# method from Group 7
x = symbols('x')
x0 = float(input('请输入起始值：'))
x_list = [x0]
x_values = []  # 设置x轴为迭代次数
y_values = []  # 设置y轴为每次迭代误差

i = 0  # 迭代次数


def f(x):
    return x ** 2 - 5 * x + 6


while True:
    x1 = diff(f(x), x).subs(x, x0)
    if x1 == 0:
        print('极值点：', x0)
        break
    else:
        x0 = x0 - f(x0) / x1  # 计算一次迭代后的x0的坐标
        x_list.append(x0)

    if len(x_list) > 1:
        i += 1
        error_1 = abs((x_list[-2] - x_list[-1]) / x_list[-1])  # 计算误差
        x_values.append(i)
        y_values.append(error_1)

        if error_1 == 0:
            print('迭代第{0}次后，误差为0'.format(i))
            break

    else:
        pass

print('所求方程式的根为{0}'.format(x_list[-1]))

plt.style.use('ggplot')
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 处理中文乱码
plt.rcParams['axes.unicode_minus'] = False
plt.plot(x_values,
         y_values,
         color='blue',
         marker='o',
         markersize=4,
         )
plt.xlabel('迭代次数')
plt.ylabel('误差值')
plt.show()

# method from Group 9
def f(x):
    return x**2 - 5*x + 6
m = np.linspace(0.05,6,100)
y = f(m)
plt.plot(m,y,ls="-.",color="r",marker=",",lw=2)
def NewtonsMethod4(f, x0, tol=1e-8):
    x = symbols('x')
    dx = diff(f(x), x)
    print("First Derivative : {}".format(dx))
    while True:
        x1 = x0 - f(x0) / float(dx.subs(x, x0))
        xpoints = np.array([x0, x1])
        ypoints = np.array([f(x0), 0])
        plt.plot(xpoints, ypoints)
        if abs(x1 - x0) < tol:
            break
        x0 = x1
    return x1

s = random.getstate()
count = 5
while count > 0:
    random.randint(0,6)
    count = count - 1
random.setstate(s)
count = 5
y0 = []
while count > 0:
    x = random.randint(0,6)
    count = count - 1
    y0.append(x)
print(y0)   #输出列表
y0.sort()   #升序排序
print(y0)

res = []
for i in range(4):
    x = NewtonsMethod4(f, y0[i])
    print(x)
    res.append(x)

plt.show()

# method from Group 6
def solveFun(fun, min_x=0, max_x=1, n_step=1000, max_lter=64, max_error=1e-6, plot=False, print_log=False):
    """
    :param fun: 需要求解的函数
    :param min_x: 自变量求解区间下限
    :param max_x: 自变量求解区间上限
    :param n_step: 查找解的步数，区间长度/步长
    :param max_lter: 最大迭代次数
    :param max_error: 容许相对误差
    :param plot: True绘制曲线图, False,绘制曲线
    :param print_log: True输出求解信息,False不输出求解信息
    :return: numpy.array()对象，包含解集
    """
    x_list = np.linspace(min_x, max_x, n_step)
    y_list = np.zeros(n_step)
    solve_list = []
    N_solve = 0
    for i in range(n_step):
        y_list[i] = fun(x_list[i])
        if 0 < i and y_list[i] * y_list[i - 1] <= 0:
            N_solve += 1
            temp1_x = x_list[i]
            temp2_x = x_list[i - 1]
            temp1_y = y_list[i]
            temp2_y = y_list[i - 1]
            dy = (temp1_y - temp2_y) / (temp1_x - temp2_x)
            error_ = abs((temp1_x - temp2_x) / (abs(temp1_x) + 1e-10))  # 给分母加上一个较小数值，以免出现除零的情况
            lter_n = 0
            if print_log:
                print("找到第 %d个解位于 %11.4E 附近，进入迭代...\n"
                      "     迭代次数         相对误差                x               fun" % (N_solve, temp1_x))

            while lter_n < max_lter and error_ > max_error:
                lter_n += 1
                temp2_x = temp1_x
                temp1_x = temp2_x - temp1_y / dy
                temp2_y = temp1_y
                temp1_y = fun(temp1_x)
                dy = (temp1_y - temp2_y) / (temp1_x - temp2_x)
                error_ = abs((temp1_x - temp2_x) / (abs(temp1_x) + 1e-10))
                if print_log:
                    print(" %8d   %16.4E    %16.4E   %16.4E" % (lter_n, error_, temp1_x, temp1_y))
                temp2_x = temp1_x
            if lter_n < max_lter:
                solve_list.append(temp1_x)
                if plot:
                    plt.plot(temp1_x, temp1_y, marker=".", markersize=16, color="r")
                    # plt.text(temp1_x, temp1_y, "%6.4E" % temp1_x, color="k")
                # print("迭代次数: %2d; res %d: kr= %6.4E, form4=%6.4E, error= %6.4E" % (
                #     max_in, len(res_list), temp1_kr, temp1_f4, error_i))
            else:
                print("达到最大迭代次数，相对误差 %16.4E" % error_)
        # print(res_list[i])
    if plot:
        plt.plot(x_list, y_list, color="b")
        plt.show()
    return np.array(solve_list)


def myFun(x):
    return x ** 2 - 5 * x + 6


print(solveFun(fun=myFun, min_x=0, max_x=20.0, print_log=True, plot=True))
