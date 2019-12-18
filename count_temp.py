#_*_coding:UTF-8_*_
# sample_1:A190909OTPN009
# sample_2:R190909PUPN006
from matplotlib import pyplot as plt
import numpy as np
labels = ["trim", "mpg", "mpm"]
# 数据
samp1_trim_1 = [653.351,635.687,701.796]
samp1_trim_2 = [512.016,489.329,474.389]
samp1_mpg_1 = [580.236,	554.56,566.461]
samp1_mpg_2 = [503.352,	525.766,540.705]
samp1_mpm_1 = [314.655,356.879,278.667]
samp1_mpm_2 = [1209.824,1209.831,1209.799]

samp1_trim_1_ave = float(sum(samp1_trim_1)/len(samp1_trim_1))
samp1_trim_2_ave = float(sum(samp1_trim_2)/len(samp1_trim_2))

samp1_mpg_1_ave = float(sum(samp1_mpg_1)/len(samp1_mpg_1))
samp1_mpg_2_ave = float(sum(samp1_mpg_2)/len(samp1_mpg_2))

samp1_mpm_1_ave = float(sum(samp1_mpm_1)/len(samp1_mpm_1))
samp1_mpm_2_ave = float(sum(samp1_mpm_2)/len(samp1_mpm_2))


y_1 = [samp1_trim_1_ave, samp1_mpg_1_ave, samp1_mpm_1_ave]
y_2 = [samp1_trim_2_ave, samp1_mpg_2_ave, samp1_mpm_2_ave]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, y_1, width, label='1')
rects2 = ax.bar(x + width/2, y_2, width, label='2')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Run_time(s)')
ax.set_xlabel("Process")
ax.set_title('Sample:R190909PUPN006')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()

        ax.annotate('{:.2f}'.format(height),  # 小数点后保留两位小数
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects1)
autolabel(rects2)

fig.tight_layout()
plt.savefig("R190909PUPN006.PNG")
plt.show()
