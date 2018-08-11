f=open("news.txt","r")
l=[]
l1=[]
x=(f.readlines())
l=x[0].split(". ")
for i in range(len(l)):
	l1.append(l[i].split())
print(l1)
