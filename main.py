import os
import argparse
from pkg_downloader import download_release

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Archive download utility')
    parser.add_argument('url', help='download/repository url of the package')
    parser.add_argument('--latest-release-file', help='if specified, the url is expected to point to a github '
                                                      'repository in which case the downloader will attempt to '
                                                      'retrieve the specified file from the latest github release.')
    parser.add_argument('--path', help='path where the archive is going to be saved.')
    parser.add_argument('--file', help='the filename of the saved archive', )
    parser.add_argument('--extract', help='extract the downloaded zip file into the download directory',
                        action='store_true')
    parser.set_defaults(extract=False)

    args = parser.parse_args()

    path = args.path or os.getcwd()
    if not os.path.exists(path):
        os.makedirs(path)

    file_name = args.file or args.url.split('/')[-1]
    url = args.url

    download_release(url, path, file_name, args.latest_release_file, args.extract)
    print("done.")
