import zipfile
import argparse
import os
import urllib
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
	except:
		raise Exception("An error occured, while parsing the github API!")

	raise Exception("Asset {} could not be found in latest release of {}!".format(file_name, args.url))


def download_release(latest_release_file, extract=False):
	
	if latest_release_file is not None:
		print("Parsing github API...")
		file_name = latest_release_file
		url, asset_size = get_latest_release_file(args.url, file_name)

	dl_path = os.path.join(path, file_name)

	if os.path.isfile(dl_path):
		os.remove(dl_path)

	if os.path.exists(dl_path):
		raise Exception("File '{}' exists and could not be removed!".format(file_name))

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
		zip_ref.extractall(path)
		zip_ref.close()
		os.remove(dl_path)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Archive download utility')
	parser.add_argument('url', help='download/repository url of the package')
	parser.add_argument('--latest-release-file', help='if specified, the url is expected to point to a ' + \
		'github repository in which case the downloader will attempt to retrieve the specified file from the latest github release.')
	parser.add_argument('--path', help='path where the archive is going to be saved.')
	parser.add_argument('--file', help='the filename of the saved archive',)
	parser.add_argument('--extract', help='extract the downloaded zip file into the download directory', action='store_true')
	parser.set_defaults(extract=False)


	args = parser.parse_args()

	path = args.path or os.getcwd()
	if not os.path.exists(path):
		os.makedirs(path)

	file_name = args.file or args.url.split('/')[-1]
	url = args.url


	download_release(args.latest_release_file, args.extract)
	print("done.")

	