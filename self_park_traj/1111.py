import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# list1 = np.array([2, 3])
# list2 = np.array([1, 1, 1])
# # print(list1 - list2)
#
# print(np.linalg.norm(list2))
#
# print(np.pi / 2 - np.arctan2(np.abs(-1), np.abs(5.5)))
#
# a = np.linspace(0, 10, 10)
# circle1_data = np.array(5 - np.sin(30*3.14/180) * a)
# circle1_data_1 = np.array(np.sin(30*3.14/180) * a)
# print(circle1_data)
# print(circle1_data_1)
#
#
# arr4=np.concatenate((circle1_data_1,circle1_data),axis=0)
# print('arr4',arr4)
#
# plt.plot([1],[1])
# plt.show()
# def drawanimationhist():
#     fig, ax = plt.subplots()
#     BINS = np.linspace(-5, 5, 100)
#     data = np.random.randn(1000)
#     n, _ = np.histogram(data, BINS)
#     _, _, bar_container = ax.hist(data, BINS, lw=2,
#                                   ec="b", fc="pink")
#     def update(bar_container):
#         def animate(frame_number):
#             data = np.random.randn(1000)
#             n, _ = np.histogram(data, BINS)
#             for count, rect in zip(n, bar_container.patches):
#                 rect.set_height(count)
#             return bar_container.patches
#         return animate
#
#     ax.set_ylim(top=55)
#
#     ani = animation.FuncAnimation(fig, update(bar_container), 50,
#                                   repeat=False, blit=True)
#     plt.show()
#
# drawanimationhist()

# a = {1:11,2:12,4:14}
# for i in a:
#     print(i)
# list_ = [1]*30
# print(list_)
print([np.pi / 2] * 20)
