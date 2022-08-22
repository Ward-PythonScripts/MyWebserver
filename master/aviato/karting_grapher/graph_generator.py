from io import StringIO
import matplotlib.pyplot as plt



def plotData(amountOfYTicks,headers,times):
    valid_colors = ["b","g","r","c","m","y","darkgreen","lime","navy","slateblue","turqouise"]
    color_selector = 0
    plt.clf()
    fig = plt.figure()
    plt.style.use("dark_background")
    fig.clf()
    for i in range(0,len(times)):
        laps = range(0,len(times[i]))
        plt.plot(laps,times[i], marker='o', label=headers[i],color=valid_colors[color_selector])
        color_selector += 1
        plt.legend()
        plt.xlabel("lap")
        plt.ylabel("lap time")
        plt.xticks(laps)
        plt.yticks(getYTicks(times[i],amountOfYTicks))
        plt.grid(True,color='0.1')
    imgdata = StringIO()
    fig.savefig(imgdata,format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data


def isHeader(strToCheck):
    for char in strToCheck:
        if str(char).isalpha():
            return True
    return False
def getYTicks(t :list,amountOfYTicks:int):
    amountOfYTicks -= 2
    inBetween = []
    maxT = max(t,default=0)
    minT = min(t,default=0)
    diff = maxT - minT
    diffOnScale = diff/amountOfYTicks
    for x in range(-1,amountOfYTicks+1):
        inBetween.append(minT + x*diffOnScale)
    return inBetween

def generate_graph(data):
    headers = []
    times = []

    index = -1
    for line in data:
        line = line.strip()
        if line != "":
            if isHeader(line):
                headers.append(line)
                times.append([])
                index +=1
            else:
                times[index].append(float(line))
    return plotData(20,headers,times)
