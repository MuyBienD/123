"""
基于两端圆弧拟合的平行泊车路径规划
"""

from park_func import *
from utils import *

if __name__ == '__main__':
    # 停车位位置
    park = dict()
    park_length = 6.5
    park_width = 2.5
    park["park_left"] = [[-park_length, 0, 0, -park_length, -park_length], [0, 0, park_width, park_width, 0]]
    park["park_target"] = [[0, park_length, park_length, 0, 0], [0, 0, park_width, park_width, 0]]
    park["park_right"] = [[park_length, 2 * park_length, 2 * park_length, park_length, park_length],
                          [0, 0, 2.5, 2.5, 0]]

    # 弧长确定
    ## 根据最小转弯半径确定圆弧2的圆心
    circle2 = np.array([end_park_point[0], end_park_point[1] + r_min])

    ## 以初始点和泊车点连线为直径确定的圆弧为转弯最大半径
    k1 = (init_park_point[1] - end_park_point[1]) / (init_park_point[0] - end_park_point[0])
    k2 = -1 / k1
    b = ((init_park_point[1] + end_park_point[1]) / 2) - k2 * ((init_park_point[0] + end_park_point[0]) / 2)
    r_max = y_start - (k2 * x_start + b)

    ## 弧1，根据最大最小的转弯半径确定的圆心
    circle1_rmin = np.array([x_start, y_start - r_min])
    circle1_rmax = np.array([x_start, y_start - r_max])

    ## 计算最小的转弯半径对应的圆心circle1_rmin到circle2圆心的距离l 减去 r_min的距离
    ## 对应的转角 alpha
    l_coord_min = circle1_rmin - circle2
    l_min = np.linalg.norm(l_coord_min) - r_min
    d_min = y_start - circle1_rmin[1]
    alpha_min = np.pi / 2 - np.arctan2(np.abs(l_coord_min[1]), np.abs(l_coord_min[0]))

    ## 计算最大的转弯半径对应的圆心circle1_rmax到circle2圆心的距离l 减去 r_min的距离
    ## 对应的转角 alpha

    l_coord_max = circle1_rmax - circle2
    l_max = np.linalg.norm(l_coord_max) - r_min
    d_max = y_start - circle1_rmax[1]
    alpha_max = np.pi / 2 - np.arctan2(np.abs(l_coord_max[1]), np.abs(l_coord_max[0]))

    ##利用二分法查找满足相切的两个圆弧
    d_middle, alpha, y_middle = FindR1R2(l_min, d_min, l_max, d_max, alpha_min, alpha_max, circle2)

    ## 轨迹点生成
    circle1_r = d_middle
    circle1 = np.array([x_start, y_middle])

    circle2_r = r_min
    circle2 = np.array([end_park_point[0], end_park_point[1] + r_min])

    num = 10  # 每段路径生成的路径点的个数
    distance = 1  # 泊车结束后上前距离
    alpha_arr = np.linspace(0, alpha, num)
    print(alpha)
    print(alpha_arr)
    circle1_data = np.array(
        [x_start - d_middle * np.sin(alpha_arr), y_middle + d_middle * np.cos(alpha_arr), alpha_arr])
    alpha_arr = np.linspace(alpha, 0, num)
    circle2_data = np.array([circle2[0] + r_min * np.sin(alpha_arr), circle2[1] - r_min * np.cos(alpha_arr), alpha_arr])
    adjust_data = np.array([np.linspace(x_end, x_end + 1, num), [y_end] * num, [0] * num])
    data_traj = np.concatenate((circle1_data, circle2_data, adjust_data), axis=1)
    plt.figure()
    plt.gca().set_aspect('equal', adjustable='box')
    for item in range(len(data_traj[0])):
        c_o = np.array([data_traj[0][item], data_traj[1][item]])
        plt.plot(c_o[0], c_o[1], "g.")
        car = car_p(car_length, car_width, c_o)
        new_car = RotTheta(car, data_traj[2][item], c_o)
        ParkDrawParallel(park, new_car)

    plt.show()
