# 绘制停车位
import matplotlib.pyplot as plt
import numpy as np
from utils import *
from scipy.interpolate import make_interp_spline


def ParkDrawParallel(park, car):
    plt.plot(park["park_left"][0], park["park_left"][1], color='black', linewidth=2.0)
    plt.plot(park["park_target"][0], park["park_target"][1], color='black', linewidth=2.0)
    plt.plot(park["park_right"][0], park["park_right"][1], color='black', linewidth=2.0)
    plt.plot(car["rectangle"][0], car["rectangle"][1], color='blue')
    plt.axis([-7, 15, 0, 7])
    plt.pause(0.1)


def ParkDrawPerpe(park, car):
    plt.plot(park["park_left"][0], park["park_left"][1], color='black', linewidth=2.0)
    plt.plot(park["park_target"][0], park["park_target"][1], color='black', linewidth=2.0)
    plt.plot(park["park_right"][0], park["park_right"][1], color='black', linewidth=2.0)
    plt.plot(car["rectangle"][0], car["rectangle"][1], color='blue')
    plt.axis([-5, 8, -7, 7])
    plt.pause(0.1)


def car_p(car_length, car_width, c_o):
    """

    :param car_length:
    :param car_width:
    :param c_o:
    :param car:
    :return:
    """
    x = c_o[0]
    y = c_o[1]
    car = dict()
    car["rectangle"] = [[x - car_lr, x - car_lr + car_length, x - car_lr + car_length, x - car_lr,
                         x - car_lr],
                        [y - car_width / 2, y - car_width / 2, y + car_width / 2,
                         y + car_width / 2, y - car_width / 2]]
    car["rear_axle"] = [[x, x], [y - car_br / 2, y + car_br / 2]]
    car["front_axle"] = [[x + car_l, x + car_l], [y - car_br / 2, y + car_br / 2]]
    car["connect"] = [[x, x + car_l], [y, y]]

    return car


def RotTheta(car, theta, c_o):
    """
    线条绕着某点旋转到一定角度，计算旋转完成后线条的坐标
    :param car:待旋转的线条
    :param theta: 绕旋转中心点转到的角度
    :param x: 旋转中心的横坐标
    :param y: 旋转中心的纵坐标
    :return: 旋转完成之后线条
    """
    x = c_o[0]
    y = c_o[1]
    new_car = dict()
    new_car["rectangle"] = [[], []]
    new_car["rear_axle"] = [[], []]
    new_car["front_axle"] = [[], []]
    new_car["connect"] = [[], []]
    for i in car:
        for j in range(len(car[i][0])):
            x_final = (car[i][0][j] - x) * np.cos(theta) - (car[i][1][j] - y) * np.sin(theta) + x
            y_final = (car[i][0][j] - x) * np.sin(theta) + (car[i][1][j] - y) * np.cos(theta) + y
            new_car[i][0].append(x_final)
            new_car[i][1].append(y_final)
    return new_car


def FindR1R2(l_min, d_min, l_max, d_max, alpha_min, alpha_max, circle2):
    l_middle = np.inf
    d_middle = 0
    if l_min > d_min and l_max < d_max:
        while np.abs(l_middle - d_middle) > 0.000001:
            # print(l_middle,d_middle)
            # 根据中间角度对应的射线与x = x_start的交点为圆心，计算l和d
            alpha_middle = (alpha_min + alpha_max) / 2
            k_middle = -np.tan(np.pi / 2 - alpha_middle)
            y_middle = k_middle * init_park_point[0] + (-k_middle * circle2[0] + circle2[1])
            d_middle = y_start - y_middle
            l_coord_middle = np.array([x_start, y_middle]) - circle2
            l_middle = np.linalg.norm(l_coord_middle) - r_min

            if l_middle > d_middle:
                l_coord_min = l_coord_middle
                l_min = l_middle
                d_min = d_middle
                alpha_min = np.pi / 2 - np.arctan2(np.abs(l_coord_min[1]), np.abs(l_coord_min[0]))

            else:
                l_coord_max = l_coord_middle
                l_max = np.linalg.norm(l_coord_max) - r_min
                d_max = d_middle
                alpha_max = np.pi / 2 - np.arctan2(np.abs(l_coord_max[1]), np.abs(l_coord_max[0]))

        d_middle = d_max
        alpha = alpha_max
        return d_middle, alpha, y_middle

    else:
        print("路径规划失败")


def B_Spline(x, y):
    x_smooth = np.linspace(x.min(), x.max(), 50)
    y_smooth = make_interp_spline(x, y)(x_smooth)
    return x_smooth[::-1], y_smooth
