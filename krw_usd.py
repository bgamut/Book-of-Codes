import os
import datetime
import matplotlib.pyplot as plt
from forex_python.converter import CurrencyRates
import click
def best_fit(x,y):
    xbar = sum(x)/len(x)
    ybar = sum(y)/len(y)
    n=len(x)
    numer=sum([xi*yi for xi,yi in zip(x,y)])-n*xbar*ybar
    denum=sum([xi**2 for xi in x]) - n * xbar**2
    a=numer/denum
    b=ybar-a*xbar
    
    return a,b
def clear():
    os.system('cls' if os.name=='nt' else 'clear')
currency=CurrencyRates()
date=datetime.date.today()
date-=datetime.timedelta(365*5)
halfDecade=[]
with click.progressbar(range(365*5)) as bar:
    for i in bar:
        rate=currency.get_rate('KRW','USD',date)
        date+=datetime.timedelta(days=1)
        halfDecade.append(rate)
        j=(i)*100/(365*5)
year=halfDecade[-365:]
quarter=halfDecade[-120:]
month=halfDecade[-30:]
week=halfDecade[-5:]
halfDecadeCut=halfDecade
time0=[]
for i in range(len(halfDecade)):
    time0.append(i)
time1=[]    
for i in range(len(halfDecadeCut)):
    time1.append(i)
a,b=best_fit(time1,halfDecadeCut)
HDLine=[a*xi+b for xi in time1]
time2=[]

for i in range(len(year)):
    time2.append(i)
c,d=best_fit(time2,year)
YLine=[c*xi+d for xi in time2]
for i in range(len(halfDecadeCut)-len(year)):
    YLine.insert(0,0)

time3=[]
for i in range(len(quarter)):
    time3.append(i)
e,f=best_fit(time3,quarter)
QLine=[e*xi+f for xi in time3]
for i in range(len(halfDecadeCut)-len(quarter)):
    QLine.insert(0,0)


time4=[]
for i in range(len(month)):
    time4.append(i)
g,h=best_fit(time4,month)
MLine=[g*xi+h for xi in time4]
for i in range(len(halfDecadeCut)-len(month)):
    MLine.insert(0,0)

time5=[]
for i in range(len(week)):
    time5.append(i)
i,j=best_fit(time5,week)
WLine=[i*xi+j for xi in time5]
for i in range(len(halfDecadeCut)-len(week)):
    WLine.insert(0,0)

plt.title('KRW to USD') 
plt.scatter(time0,halfDecade)
plt.plot(time1,HDLine,'red',time1,YLine,'orange',time1,QLine,'yellow',time1,MLine,'green',time1,WLine,'blue')
plt.show()

