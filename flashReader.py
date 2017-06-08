import urllib2
import time
import sys
import subprocess

def print_centered(s):
	terminal_width=int(subprocess.check_output(['stty','size']).split()[1])
	print (s.center(terminal_width))

def flashReader(a):
	url=str(a)
	data=urllib2.urlopen(url)
	subprocess.call(["tput","civis","--invisible"])
	for line in data:
		for word in line.split():
			subprocess.call('clear')
			time.sleep(0.03)
			print("\n"*3)
			print_centered (word)
			print("\n"*3)
			#subprocess.call(["say","-v","Vicki","-r","2500",str(word)])
			time.sleep(0.03)
	subprocess.call(["tput", "cnorm","--normal"])
if __name__ == "__main__":
	if sys.argv[1]:
		flashReader(sys.argv[1])
	
