import math

def Txt_process():
    fr = open("./jet.vecT", "r", encoding="utf-8")
    txt = list()
    vector = list()
    #map = dict()
    line = fr.readlines()
    fr.close()
    for l in range(len(line)):
        data = line[l].strip("\n").split(' ')
        if l == 0:
            txt.append(line[l])
            width = int(data[0])
            height = int(data[1])
        else:
            Norm = []
            temp = []
            for i in range(width):
                x = float(data[0 + 2*i])
                y = float(data[1 + 2*i])
                norm = math.sqrt(x**2 + y**2)
                Norm.append(str(norm))
                Value = [x, y, norm]
                temp.append(Value)
            vector.append(temp)
            txt.append(' '.join(Norm) + '\n')

            # Key = (l-1)*width + i
            # Value = [x, y, norm]
            # map[Key] = Value
            #ls = list(map.items())
            #ls.sort(key=lambda x: x[0])
    fw = open("./jetMag.txt", "w+")
    fw.write("".join(txt))
    fw.close()
    return width, height, vector