import zipfile
import argparse
import os
import urllib
import urlparse
import json


asset_size = -1

def showprogress(block_count, block_size, file_size):
	size = asset_size if file_size == -1 else file_size
	if size >= 0:
		progress_string = str(min(block_count * block_size * 100 / (size * 8), 100)) + "%"
	else:
		progress_string = str(block_count * block_size) + "bytes"
	print "Downloading {}...".format(progress_string)

def find_github_api_url(url):
		repo_url = urlparse.urlparse(url)
		netloc = repo_url.netloc or repo_url.path
		netloc = "api." + netloc
		netpath = repo_url.path
		netpath = "/repos" + netpath + "/releases/latest"
		return urlparse.ParseResult(repo_url.scheme, netloc, netpath, *repo_url[3:]).geturl()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Archive download utility')
	parser.add_argument('url', help='download url of the package')
	parser.add_argument('--latest-release-file', help='if specified, the url is expected to point to a ' + \
		'github repository in which case the downloader will attempt to retrieve the specified file from the latest github release.')
	parser.add_argument('--path', help='path where the archive is going to be saved.')
	parser.add_argument('--file', help='the filename of the saved archive',)


	args = parser.parse_args()

	path = args.path or os.getcwd()
	if not os.path.exists(path):
		os.makedirs(path)

	file_name = args.file or args.url.split('/')[-1]
	url = args.url

	if args.latest_release_file is not None:
		file_name = args.latest_release_file

		api_url = find_github_api_url(args.url)

		response = urllib.urlopen(api_url)
		found_asset = False
		try:
			json_data = json.loads(response.read())
			for asset in json_data["assets"]:
				if asset["name"] == file_name:
					url = asset["browser_download_url"]
					asset_size = asset['size']
					found_asset = True
					break;
		except:
			raise Exception("An error occured, while parsing the github API!")

		if not found_asset:
			raise Exception("Asset {} could not be found in latest release of {}!".format(file_name, args.url))

	dl_path = os.path.join(path, file_name)

	if os.path.isfile(dl_path):
		os.remove(dl_path)

	if os.path.exists(dl_path):
		raise Exception("File '{}' exists and could not be removed!".format(file_name))

	print "Downloading {} to {}...".format(url, dl_path)
	safe_url = urllib.quote(args.url)
	try:
		urllib.urlretrieve(args.url, dl_path, showprogress)
	except urllib.ContentTooShortError:
		raise Exception("Download failed!")
	print "done."

	