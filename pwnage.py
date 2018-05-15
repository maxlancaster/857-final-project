import requests
import sys

if len(sys.argv)==2:

	passwordTest=sys.argv[1]
	cleaned = str(passwordTest).strip()
	print cleaned
	req=requests.get("https://api.pwnedpasswords.com/pwnedpassword/"+cleaned)
	print req.text

else:

	myFile=open("passwords.txt",'r')
	passwords=myFile.readlines()
	myFile.close()

	passwordSecurity={}

	i=0
	for password in passwords:
		cleaned = str(password).strip()
		try:
			req=requests.get("https://api.pwnedpasswords.com/pwnedpassword/"+cleaned)
		except:
			print "Failed after "+str(i)+" requests."
		passwordSecurity[cleaned]=int(req.text)
		i+=1

	maxPwn=0
	for key in passwordSecurity.keys():
		maxPwn+=passwordSecurity[key]

	for key in passwordSecurity.keys():
		passwordSecurity[key] = float(passwordSecurity[key])/maxPwn

	print passwordSecurity

	output = open("frequencies.txt", 'w')

	for key in passwordSecurity.keys():
		output.write(str(key)+" has a risk measure of "+str(passwordSecurity[key])+"\n")

	output.close()