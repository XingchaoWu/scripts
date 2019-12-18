#_*_coding:UTF-8_*_

from matplotlib import pyplot as plt

x_1 = ["sample.list_1","sample.list_2"]
x_2 = [1, 2]
y_1 = [2359.162, 2625.951]
y_2 = [2063.249, 2144.28]

# plt.figure(figsize=(20,8),dpi=80)
plt.bar(x_2,y_1)
plt.bar(x_2,y_2)
plt.show()
