#!/usr/bin/env python3

import re
import csv
import operator

err=["Error","Count"]
use=["Username","INFO","ERROR"]
error={}
per_user={}
info={}
with open("syslog.log","r") as file:
	files=file.readlines()
	for line in files:
		line=line.rstrip("\n")
		res=re.search(r"ticky: ERROR ([\w ']*) (\([\w .]*\))",line)
		if res is not None:
			a=res.group(2)
			b=a[1:len(a)-1]

			if res.group(1) not in error:
				error[res.group(1)]=1
			else:
				error[res.group(1)]+=1

			if b not in per_user:
				per_user[b]=[1]
			else:
				per_user[b].append(len(per_user[b])+1)
		else:
			res=re.search(r"ticky: INFO ([\w ']*) (\[#\d*\]) (\([\w .]*\))",line)
			if res is not None:
				a=res.group(3)
				b=a[1:len(a)-1]
				if b not in info:
					info[b]=1
				else:
					info[b]+=1

for user in per_user.keys():
	per_user[user]=[per_user[user][-1]]
	if user in info.keys():
		per_user[user].append(info[user])
	else:
		per_user[user].append(0)

per_user=sorted(per_user.items())
error=sorted(error.items(), key=operator.itemgetter(1), reverse=True)

with open('error_message.csv', 'w') as f:
	writer=csv.DictWriter(f,err)
	writer.writeheader()
	for i in error:
		f.write("%s,%s\n"%(i[0],i[1]))

with open("user_statistics.csv",'w') as f1:
	writer=csv.DictWriter(f1,use)
	writer.writeheader()
	for i in per_user:
		f1.write("%s,%s,%s\n"%(i[0],i[1][1],i[1][0]))

# sudo chmod +x csv_to_html.py
# sudo chmod o+w /var/www/html
#./csv_to_html.py error_message.csv /var/www/html/error.html
#./csv_to_html.py user_statistics.csv /var/www/html/stat.html