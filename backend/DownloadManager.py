from zipfile import ZipFile
import requests
import json
import sys
import os

# This class manages downloading digital elevation files from USGS
class DownloadManager:
	def __init__(self) -> None:
		self.serviceUrl = "https://m2m.cr.usgs.gov/api/api/json/stable/"

	# Sends request to USGS api and handles any request errors that may occur
	# Returns data on successful request
	def sendRequest(self, url, data, apiKey=None):
		json_data = json.dumps(data)

		if apiKey == None:
			response = requests.post(url, json_data)
		else:
			headers = {'X-Auth-Token': apiKey}          
			response = requests.post(url, json_data, headers = headers)    

		try:
			httpStatusCode = response.status_code 
			if response == None:
				print("No output from service")
				return None
			output = json.loads(response.text)	
			if output['errorCode'] != None:
				print(output['errorCode'], "- ", output['errorMessage'])
				return None
			if  httpStatusCode == 404:
				print("404 Not Found")
				return None
			elif httpStatusCode == 401: 
				print("401 Unauthorized")
				return None
			elif httpStatusCode == 400:
				print("Error Code", httpStatusCode)
				return None
		except Exception as e: 
			response.close()
			print(e)
			return None
		response.close()
		
		return output['data']

	# Logs into USGS account
	# You must successfully login before attempting to download files
	# Returns an api key that must be passed in thru the "X-Auth-Token" param in header
	def login(self, username, password):
		payload = {"username" : username,
					"password" : password}
		url = self.serviceUrl + "login"
		output = self.sendRequest(url, payload)

		if output == None:
			print("Failed to login")
			return False
		
		print("Logged in successfully")
		self.apiKey = output
		return True


	# Searches for datasets that fit certain criteria
	# Returns a list of datasets that fit the criteria
	def searchDatasets(self):
		pass

	# Downloads all necessary datasets from USGS api
	def downloadDatasets(self, minX:int, minY: int, maxX:int, maxY:int):
		# Converts bounding box to string that USGS server can accept
		bbox=','.join([str(minX), str(minY), str(maxX), str(maxY)])
		
		payload = dict(bbox=bbox, datasets="National Elevation Dataset (NED)")
		links = self.getDownloadLinks(payload)
		self.downloadAndExtractFiles(links)

	def getDownloadLinks(self, payload):
		r = self.sendRequest(self.serviceUrl + "download", payload, apiKey=self.apiKey)
		requests.get(self.serviceUrl,
							params=payload)

		links = []
		if r.status_code == 200:
			for item in r.json()["items"]:
				links.append(item["downloadURL"])
		return links
		
	def downloadAndExtractFiles(self, links):
		for link in links:
			# Name of the directory that stores the DEM files
			dirname = "Elevation_Files/"
			# Creates filename from the end of the download link
			filename = link.rsplit('/', 1)[-1]

			# Downloads from each link one at a time
			if not os.path.isfile(dirname + filename):
				r = requests.get(link)
				# Saves the zip files contents
				with open(dirname + filename, 'wb') as f:
					f.write(r.content)
				with ZipFile(dirname + filename, "r") as data_zip:
					data_zip.extractall(dirname)

if __name__ == "__main__":
	downloadManager = DownloadManager()
	downloadManager.login("Suheyb21", "C5YJR3txZpue2Xq")