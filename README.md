# package-downloader
Small python utility for downloading archives (especially github release assets)

## Usage

```
usage: pkg_downloader.py [-h] [--latest-release-file LATEST_RELEASE_FILE]
                         [--path PATH] [--file FILE] [--extract EXTRACT]
                         url

Archive download utility

positional arguments:
  url                   download url of the package

optional arguments:
  -h, --help            show this help message and exit
  --latest-release-file LATEST_RELEASE_FILE
                        if specified, the url is expected to point to a github
                        repository in which case the downloader will attempt
                        to retrieve the specified file from the latest github
                        release.
  --path PATH           path where the archive is going to be saved.
  --file FILE           the filename of the saved archive
  --extract EXTRACT     extract the downloaded zip file into the download
                        directory
```