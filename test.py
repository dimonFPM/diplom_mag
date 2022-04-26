import numpy as np

a = 1

xx = np.arange(0, 100.001, 0.001)

yy_cos = np.copy(xx)
yy_ch = np.copy(xx)

yy_cos = yy_cos * a
yy_cos = np.cos(yy_cos)

yy_ch = yy_ch * a
yy_ch = np.cosh(yy_ch)
yy_ch = 1 / yy_ch

# print(yy_cos[:10])
# print(yy_ch[:10])
col = 0
for i in range(len(yy_cos)):
    # if -0.001 < yy_cos[i] < 0.001:
    if yy_cos[i] ==0:
        col += 1
        print(yy_cos[i])
print(col)

import matplotlib.pyplot as plt

fig = plt.Figure()
plt.plot(xx, yy_ch)
plt.plot(xx, yy_cos)
plt.show()
