from matplotlib.ticker import MultipleLocator
import matplotlib.pyplot as plt
import numpy as np
import Preprocessing


def Data_Input():
    Width, Height, Vector = Preprocessing.Txt_process()
    Data_X = np.zeros((Width, Height))
    Data_Y = np.zeros((Width, Height))
    Nome = np.zeros((Width, Height))
    for t0 in range(0, Height, 1):
        for t1 in range(0, Width, 1):
            Data_X[t0, t1] = Vector[t0][t1][0]
            Data_Y[t0, t1] = Vector[t0][t1][1]
            Nome[t0, t1] = Vector[t0][t1][2]


    return Width, Height, Data_X, Data_Y, Nome


Width, Height, Data_X, Data_Y, Nome= Data_Input()
Y, X = np.mgrid[1:Width:complex(Width), 1:Height:complex(Height)]
U = Data_X
V = Data_Y
fig, ax = plt.subplots(figsize=(16, 16), dpi=50, edgecolor="white", facecolor="white", frameon=False)
Q = ax.quiver(X, Y, U, V, color="black", units = "dots",
              angles = 'xy', pivot = "tail", scale_units = "dots", scale = 2.8, width = 1.1)
#Q = ax.quiver(X[::2, ::2], Y[::2, ::2], U[::2, ::2], V[::2, ::2], Nome[::2, ::2], Nome, units = "dots",
              #angles = 'xy', pivot = "tail", scale_units = "dots", scale = 1, width = 4 )
#不显示边框及坐标值
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
plt.savefig("./Vector1.jpg")


"""fig, ax = plt.subplots(figsize=(32, 32), dpi=80, edgecolor="black", facecolor="white", frameon=True)
ax.set_title("Figure1  2D VECTOR VISUALIZATION", fontproperties="Arial", fontsize=56, color="black")
Q = ax.quiver(X, Y, U, V, color="#2D1E6C", units = "dots",
              angles = 'xy', pivot = "tail", scale_units = "dots", scale = 1/2, width = 2)
#Q = ax.quiver(X[::2, ::2], Y[::2, ::2], U[::2, ::2], V[::2, ::2], Nome[::2, ::2], Nome, units = "dots",
              #angles = 'xy', pivot = "tail", scale_units = "dots", scale = 1, width = 4 )
ax.tick_params(axis = "both", labelsize=38, length=8, width=8, zorder=8, )
majorlocator = MultipleLocator(16)
ax.xaxis.set_major_locator(majorlocator)
ax.yaxis.set_major_locator(majorlocator)
ax.set_xlim(0,Width)
ax.set_ylim(0,Height)
plt.savefig("./Vector.jpg")"""