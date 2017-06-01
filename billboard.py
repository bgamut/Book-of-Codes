import billboard
import amen
import yaml
import urllib
chart = billboard.ChartData('hot-100')
hits=[]
misses=[]
for i in range(len(chart)):
    if i<30:
        hits.append(chart[i])
    else:
        misses.append(chart[i])
url="http://headers.jsontest.com/"
data=urllib.urlopen(url)
output=yaml.safe_load(data)
print(data)
