import zipfile
import os
import urllib.parse
import urllib.request
import urllib.error
import json


global asset_size

asset_size = -1


def show_progress(block_count, block_size, file_size):
	global asset_size
	size = asset_size if file_size == -1 else file_size
	if size >= 0:
		progress_string = str(min(
			block_count * block_size * 100 / size, 100
			)) + "%"
	else:
		progress_string = str(block_count * block_size) + "bytes"
	print ("Downloading {}...".format( progress_string) )


def find_github_api_url(url):
		repo_url = urllib.parse.urlparse(url)
		netloc = repo_url.netloc or repo_url.path
		netloc = "api." + netloc
		netpath = repo_url.path
		netpath = "/repos" + netpath + "/releases/latest"
		return urllib.parse.ParseResult(repo_url.scheme, netloc, netpath, *repo_url[3:]).geturl()


def get_latest_release_file(url, asset_name):
	size = -1
	api_url = find_github_api_url(url)

	response = urllib.request.urlopen(api_url)
	try:
		json_data = json.loads(response.read())
		for asset in json_data["assets"]:
			if asset["name"] == asset_name:
				asset_url = asset["browser_download_url"]
				if "size" in asset:
					size = asset['size']
					print("Found size: {}".format( asset_size ))
				else:
					print("size is not present in json data: '{}'".format(json_data))
				return asset_url, size
	except Exception as e:
		raise Exception("An error occured, while parsing the github API:\n", e)

	raise Exception("Asset {} could not be found in latest release of {}!".format(asset_name, url))


def download_release(url, target_path, output_file=None, latest_release_file=None, extract=False):
	
	if latest_release_file is not None:
		print("Parsing github API...")
		file_name = output_file if output_file else latest_release_file
		url, asset_size = get_latest_release_file(url, latest_release_file)

	dl_path = os.path.join(target_path, output_file)

	if os.path.isfile(dl_path):
		os.remove(dl_path)

	if os.path.exists(dl_path):
		raise Exception("File '{}' exists and could not be removed!".format(output_file))

	print("Downloading {} to {}...".format(url, dl_path))
	try:
		urllib.request.urlretrieve(url, dl_path, show_progress)
		#r = requests.get(url, stream=True)
		#if r.status_code == 200:
		#	with open(dl_path, 'wb') as f:
		#		r.raw_decode_content = True
		#		f.write(r.raw)
	except urllib.error.ContentTooShortError:
		raise Exception("Download failed!")
	except IOError as e:
		raise Exception("An error occured while downloading!\n\n{}".format(e))

	print( "Download complete.")

	if extract:
		print("Extracting...")
		zip_ref = zipfile.ZipFile(dl_path, 'r')
		zip_ref.extractall(target_path)
		zip_ref.close()
		os.remove(dl_path)
