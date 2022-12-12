# <div  align="center"> BIRP Playlist Downloader</div>

BIRP is a monthly compilation of over 100 tracks that are available to stream or download for free. Many of the playlists have a download option, such as a torrent or zip file. However, some of the older playlists are only available to stream, making it difficult to download each songs manually.

This downloader can help you easily download older playlists. Note that some newer playlists may not have all of the songs available for streaming, so it's best to use the official download option if it's available.

Try on google colab
 [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1z0-5bqUPRCSIWU6oB3xpy5nZw92-5X5D#scrollTo=EQe1PbhfcDc4&forceEdit=true&sandboxMode=true) 
 [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/17QHVXsrQUdjAQVX-_ffprfgoxYZrwhKw#forceEdit=true&sandboxMode=true) 

## Requirements

- BeautifulSoup
- Humanfriendly
- Mutagen
- Progressbar
- Requests

  
  

## Usage

* Install the required libraries

```python
#Code in playlist_downloader.py

from birpdownloader import Birpdownloader

#Instantiate the class, pass the year and month as strings
p = Birpdownloader('2018',  'april')

#Get the URLs of the songs in the playlist
valid_urls, invalid_urls, total_urls = p.get_song_urls()

#Print the number of available songs for download
p.get_status(valid_urls, invalid_urls)

#Get the names of the songs in the playlist
clean_songs, raw_songs = p.get_song_name()

#Get the indexes of the downloadable and undownloadable songs in the playlist
downloadable_songs, undownloadable_songs = p.get_indexes(valid_urls, invalid_urls, total_urls, clean_songs, raw_songs)

#Create a folder to save the download songs.
PATH = p.create_folder('your_path')

#Download the selected playlist
p.song_downloader(PATH, valid_urls, downloadable_songs)

#Create a txt file with additional content and external links
p.additional_content(PATH, downloadable_songs, undownloadable_songs)

```

For data analysis purposes, I have downloaded all of the songs as a CSV file. The code for the scraper is also available here as `birp_all_songs.py`, and you can try it out in Google Colab.

The scraper will generate two CSV files: `all_raw_songs` and `all_clean_songs`. The difference between the two is that `clean_songs` does not contain any special characters, while `raw_songs` does.
