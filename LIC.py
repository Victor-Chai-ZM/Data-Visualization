import random
import math
import numpy as  np
from PIL import Image,ImageDraw


def Data_Input():
    fr = open("./jet.vecT", "r", encoding="utf-8")
    line = fr.readlines()
    Width = int((line[0].strip("\n").split(' '))[0])
    Height = int((line[0].strip("\n").split(' '))[1])
    line = line[1:]
    fr.close()
    Data_x = list()
    Data_y = list()
    for t0 in range(0, Height, 1):
        record = line[t0].strip("\n").split(' ')
        for t1 in range(0, Width, 1):
            record[(2*t1)] = float(record[(2*t1)])
            record[(2*t1 + 1)] = float(record[(2*t1 + 1)])
            Norm = math.sqrt(record[(2*t1)]**2 + record[(2*t1 + 1)]**2)
            if Norm != 0:
                X = record[(2*t1)] / Norm
                Y = record[(2*t1 + 1)] / Norm
            else:
                X = 0.0
                Y = 0.0
            Data_x.append(X)
            Data_y.append(Y)

    return Width, Height, Data_x, Data_y


def MakeWhiteNoise(Width, Height):
    Noise = np.zeros((Height, Width))
    for line_num in range(Height):
        for item_num in range(Width):
            random.seed()
            r = random.randint(0,256)
            Noise[line_num, item_num] = r
    return Noise


def GaussianFilter(Kernelsize = 16, sigma=2):
    Filter_Ker = np.zeros((Kernelsize, Kernelsize))
    center = Kernelsize // 2
    if sigma <= 0:
        sigma = ((Kernelsize-1)*0.5-1)*0.3+0.8
    S = sigma**2
    Sum = 0
    for Yloc in range(Kernelsize):
        for Xloc in range(Kernelsize):
            x, y = Xloc-center, Yloc-center
            Filter_Ker[Xloc, Yloc] = np.exp(-(x**2 + y**2)/(2*S))
            Sum += Filter_Ker[Xloc, Yloc]
    Filter_Ker = Filter_Ker/Sum
    return Filter_Ker


def GenBoxFilterLUT(Kernelsize = 16):
    Filter_Forward = list()
    Filter_Back = list()
    for Num in range(1024*Kernelsize**2):
        Filter_Forward.append(float(Num))
        Filter_Back.append(float(Num))
    return Filter_Forward, Filter_Back


def StreamlineTrack(Width, Height, X0, Y0, Data_X, Data_Y, Noise, Kernel_Forward, Kernel_Back, Dir_Flag=0, Kernelsize = 16):
    Track_Steps = 0
    CurLen = 0.0
    Max_Step = 5 * Kernelsize
    Map_Len_To_Filter = (1024*Kernelsize**2 - 1)/Kernelsize
    P_Val = 0.0
    W_Val = 0.0

    if Dir_Flag == 0:
        Ker = Kernel_Forward
        Dir = 1


    if Dir_Flag == 1:
        Ker = Kernel_Back
        Dir = -1


    #循环终止条件：流线追踪的足够长或者到达了涡流的中心
    while ((Track_Steps < Max_Step) and (CurLen < Kernelsize)):

        Vctr_X = Dir*Data_X[X0 * Width + Y0]
        Vctr_Y = Dir*Data_Y[X0 * Width + Y0]

        #若为关键点即一般情况下为涡流的中心时，跳出本次追踪
        if (Vctr_X == 0 and Vctr_Y == 0):
            if Track_Steps == 0:
                P_Val = 0.0
                W_Val = 1.0
            return P_Val, W_Val

        SegLen = 100000.0
        VECTOR_COMPONENT_MIN = 0.05
        """if Vctr_X == 0:
            SegLen = float(1/abs(Vctr_Y))
        elif Vctr_Y == 0:
            SegLen = float(1/abs(Vctr_X))
        else:
            SegLen = min(float(1 / abs(Vctr_X)), float(1 / abs(Vctr_Y)))"""
        if Vctr_X < -VECTOR_COMPONENT_MIN:
            SegLen = -0.5 / Vctr_X
        if Vctr_X > VECTOR_COMPONENT_MIN:
            SegLen = 0.5 / Vctr_X
        if Vctr_Y < -VECTOR_COMPONENT_MIN:
            TemLen = -0.5 / Vctr_Y
            if TemLen < SegLen:
                SegLen = TemLen
        if Vctr_Y > VECTOR_COMPONENT_MIN:
            TemLen = 0.5 / Vctr_Y
            if TemLen < SegLen:
                SegLen = TemLen

        PrvLen = CurLen
        CurLen += SegLen
        SegLen += 0.0004   #如何不增加的话，还是会出现问题

        #判断本段流线的长度因子
        if CurLen > Kernelsize:
            SegLen = Kernelsize - PrvLen
            CurLen = Kernelsize

        # 获取下一个追踪点的位置
        X1 = int(round(X0 + Vctr_X * SegLen))
        Y1 = int(round(Y0 + Vctr_Y * SegLen))

        # 计算采样点位置
        Samp_X = int((X0 + X1) // 2)
        Samp_Y = int((Y0 + Y1) // 2)

        # 获取纹理采样点的灰度值
        Tex_Val = Noise[Samp_Y][Samp_X]
        W_Temp = Ker[int(CurLen * Map_Len_To_Filter)]
        W_Cur = W_Temp - W_Val
        W_Val = W_Temp
        P_Val = Tex_Val * W_Cur

        Track_Steps += 1
        X0 = X1
        Y0 = Y1


        if(X0 < 0 or X0 >= Width or Y0 < 0 or Y0 >= Width):
             break

    return P_Val, W_Val




def FlowImagingLIC(Width, Height, Data_X, Data_Y, Noise, Kernel_Forward, Kernel_Back, Kernelsize = 16):
    Oimage = np.zeros((Height, Width))

    for line_num in range(Height):
        for item_num in range(Width):
            Tex_Val = list()
            for Dir in range(2):
                X0 = item_num
                Y0 = line_num
                P_Temp, W_Temp = StreamlineTrack(Width=Width, Height=Height, X0=X0, Y0=Y0, Data_X=Data_X,Kernelsize = Kernelsize,
                                                 Data_Y=Data_Y, Noise=Noise, Dir_Flag=Dir, Kernel_Forward=Kernel_Forward,
                                                 Kernel_Back = Kernel_Back)
                Tex_Val.append([P_Temp, W_Temp])

            Tex = (Tex_Val[0][0] + Tex_Val[1][0]) / (Tex_Val[0][1] + Tex_Val[1][1])

            if Tex < 0:
                Tex = 0
            if Tex > 255:
                Tex = 255
            Oimage[line_num][item_num] = int(Tex)


    Max_E = Oimage.max()
    Oimage = Oimage / Max_E * 255
    return Oimage




def Data_Output(Width, Height, OImage, filename="./LIC.png"):
    Pic = Image.new("RGB", (Height,Width))
    ImageDraw.Draw(Pic)
    for line_num in range(Height):
        for item_num in range(Width):
            Color = int(OImage[line_num][item_num])
            Pic.putpixel((line_num, item_num),(Color, Color, Color))
    Pic.show()
    Pic.save(filename)
    print("The vector field has been visualized")



def Check(Width=400, Height=400):
    Width = Width
    Height = Height
    Data_X = np.zeros(Height * Width)
    Data_Y = np.zeros(Height * Width)
    for Line_Num in range(Height):
        for Item_Num in range(Width):
            vec_x = -(Line_Num) / Height + 0.5
            vec_y = (Item_Num) / Width - 0.5

            Norm = math.sqrt(vec_x ** 2 + vec_y ** 2)
            if Norm < 0.001:
                scale = 0.0
            else:
                scale = 1 / Norm

            vec_x *= scale
            vec_y *= scale
            Data_X[Line_Num * Width + Item_Num] = vec_x
            Data_Y[Line_Num * Width + Item_Num] = vec_y
    return Width, Height, Data_X, Data_Y





Kernelsize = 3
Width, Height, Data_X, Data_Y = Data_Input()
#Width, Height, Data_X, Data_Y = Check()
Noise = MakeWhiteNoise(Width, Height)
Kernel_Forward, Kernel_Back = GenBoxFilterLUT(Kernelsize = Kernelsize)
Oimage = FlowImagingLIC(Width, Height, Data_X, Data_Y, Noise, Kernel_Forward, Kernel_Back, Kernelsize = Kernelsize)
#numpy.savetxt("./LIC.txt",Oimage)
#Gaussian = GaussianFilter(Kernelsize = Kernelsize)
Data_Output(Width, Height, Oimage)
