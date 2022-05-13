"""
基于两端圆弧拟合的平行泊车路径规划
"""

from park_func import *
from utils import *
import numpy as np
from sympy import *

if __name__ == '__main__':
    # 停车位位置
    park = dict()
    park_length = 6.5
    park_width = 2.5
    park["park_left"] = [[-park_width / 2, -park_width / 2, -park_width * 1.5, -park_width * 1.5, -park_width / 2],
                         [0, -park_length, -park_length, 0, 0]]
    park["park_target"] = [[park_width / 2, park_width / 2, -park_width / 2, -park_width / 2, park_width / 2],
                           [0, -park_length, -park_length, 0, 0]]
    park["park_right"] = [[park_width * 1.5, 1.5 * park_width, park_width / 2, park_width / 2, park_width * 1.5],
                          [0, -park_length, -park_length, 0, 0]]

    # 弧长确定
    ## 根据最小转弯半径确定圆弧1的圆心
    circle1 = np.array([x_start, y_start - r_min])
    circle3 = np.array([x_end + r_min, y_end])
    R = 2 * r_min
    theta1 = Symbol("theta1")
    theta3 = Symbol("theta3")
    result = solve([cos(theta3) - sin(theta1) - (circle3[0] - circle1[0]) / R,
                    cos(theta1) - sin(theta3) - (circle3[1] - circle1[1]) / R],
                   [theta1, theta3])

    for res in result:
        print(res)
        if (res[0] < np.pi / 2) and (res[0] > 0) and (res[1] < np.pi / 2) and (res[1] > 0):
            theta1 = float(res[0])
            theta3 = float(res[1])

    Circle2 = np.array([circle3[0] - 2 * r_min * cos(theta3), circle3[1] + 2 * r_min * sin(theta3)])
    theta2 = float(np.pi / 2 - theta1 - theta3)

    num = 15
    # print(type(theta1))
    # print(type(theta2))
    # print(type(0.323434385700017))
    alpha_arr = np.linspace(0, float(theta1), num)
    print(alpha_arr)
    circle1_data = np.array(
        [x_start - r_min * np.sin(alpha_arr), y_start - r_min + r_min * np.cos(alpha_arr), alpha_arr])
    alpha_arr = np.linspace(theta1, np.pi / 2 - theta3, num)
    circle2_data = np.array([Circle2[0] + r_min * np.sin(alpha_arr), Circle2[1] - r_min * np.cos(alpha_arr), alpha_arr])
    alpha_arr = np.linspace(theta3, 0, num)
    circle3_data = np.array(
        [circle3[0] - r_min * np.cos(alpha_arr), circle3[1] + r_min * np.sin(alpha_arr), np.pi / 2 - alpha_arr])
    adjust_data = np.array([[x_end] * num, np.linspace(y_end, y_end - 4, num), [np.pi / 2] * num])

    data_traj = np.concatenate((circle1_data, circle2_data, circle3_data, adjust_data), axis=1)

    plt.figure()
    plt.gca().set_aspect('equal', adjustable='box')
    for item in range(len(data_traj[0])):
        c_o = np.array([data_traj[0][item], data_traj[1][item]])
        plt.plot(c_o[0], c_o[1], "g.")
        car = car_p(car_length, car_width, c_o)
        new_car = RotTheta(car, data_traj[2][item], c_o)
        ParkDrawPerpe(park, new_car)

    plt.show()
