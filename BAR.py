#_*_coding:UTF-8_*_

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


# labels = ['clean_reads\n_human_rRNA', 'clean_reads\n_bacteria_16S_rRNA', 'unmapped_reads\n_bacteria_16S_rRNA']
# x1 = [54966, 84865, 6.91]
# x2 = [71309, 24253, 5.17]
#
#
labels = ['A191018PAPN002-KY1','A191018PAPN002-KY2',]
x1 = [8.4865, 2.4253]
x2 = [6.7686, 1.8775]




x = np.arange(len(labels))  # the label locations
width = 0.2  # the width of the bars

fig, ax = plt.subplots()
# rects1 = ax.bar(x - width/2, x1, width, label='A191018PAPN002-KY1', color="#00BFFF")
# rects2 = ax.bar(x + width/2, x2, width, label='A191018PAPN002-KY2', color="#C0FF3E")
rects1 = ax.bar(x - width/2, x1, width, label='clean_reads\n_bacteria_16S_rRNA')
rects2 = ax.bar(x + width/2, x2, width, label='unmapped_reads\n_bacteria_16S_rRNA')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('rRNA_mapped_num(×10^4)')
ax.set_title('rRNA_count')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects1)
autolabel(rects2)

fig.tight_layout()
plt.savefig("./bacteria_16S_rRNA_ratio.png")

plt.show()