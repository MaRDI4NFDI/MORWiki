from morb_fetch import MORLABDownloader

downloader = MORLABDownloader()
print("Available versions:", downloader.list_available_versions())
downloader.retrieve_version("6.0")
