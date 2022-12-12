import os
import shutil
from bs4 import BeautifulSoup
import requests
import time
import re
from urllib.parse import urljoin
from mutagen.mp3 import MP3 # To Retrieve the length of each song
from humanfriendly import format_timespan # For a simple way to show total playlist length
import progressbar


class Birpdownloader():

      """A class for downloading a playlist from BIRP.fm
      
      Attributes:
          year(str): The year of the playlist to download.
          month(str): The month of the playlist to download.
      """

      #absolute link from stream songs
      DOWNLOAD_LINK = 'https://d1e5xmqmk0w5rl.cloudfront.net/playlists/'


      def __init__(self, year, month):
          self.year = year
          self.month = month


      def get_song_urls(self):

          """Get the URLs of the songs in the playlist.

          Returns:
              Three lists:
              - A list of valid URLs of the songs in the playlist.
              - A list of invalid URLs of the songs in the playlist.
              - A list of all URLs of the songs in the playlist (valid and invalid).
          """

          playlist_url = f'https://www.birp.fm/playlist/{self.year}/{self.month}-{self.year}'
          r = requests.get(playlist_url)
          soup = BeautifulSoup(r.text, 'lxml')
          if r.ok:
              songs_elements = soup.find_all("div", attrs={"class": "track-playbutton"})
              valid_urls = []
              invalid_urls = []
              total_urls = []
              for i in songs_elements:
                  url = urljoin(self.DOWNLOAD_LINK, i.get('id'))
                  r = requests.get(url)
                  total_urls.append(url)
                  if r.ok:
                      valid_urls.append(url)
                  else:
                      invalid_urls.append(url)

          return valid_urls, invalid_urls, total_urls

      def get_indexes(self, valid_urls, invalid_urls, total_urls, clean_songs, raw_songs):
          """Get the indexes of the downloadable and undownloadable songs in the playlist.

          Returns:
              A tuple containing two lists:
              - A list of downloadable songs in the playlist.
              - A list of undownloadable songs in the playlist.
          """
          idx_good = [total_urls.index(idx) for idx in valid_urls]
          idx_bad = [total_urls.index(idx) for idx in invalid_urls]

          downloadable_songs = [clean_songs[idx] for idx in idx_good]
          undownloadable_songs = [raw_songs[idx] for idx in idx_bad]
          return downloadable_songs, undownloadable_songs
      

      def get_song_name(self):

          """Get the names of the songs in the playlist.

          Returns:
              - A list of song names in the playlist, with special characters removed.
              - A list of raw song names in the playlist.
          """

          playlist_url = f'https://www.birp.fm/playlist/{self.year}/{self.month}-{self.year}'
          r = requests.get(playlist_url)
          soup = BeautifulSoup(r.text, 'lxml')
          song_title = soup.find_all('span', attrs={'class':'song-title'})
          song_artist = soup.find_all('span', attrs={'class':'song-artist'})
          song_title = [x.text for x in song_title]
          song_artist = [x.text for x in song_artist]
          clean_artist= [re.sub(r'[^a-zA-Z0-9 ]', '', i) for i in song_artist]
          clean_title = [re.sub(r'[^a-zA-Z0-9 ]', '', i) for i in song_title]

          #It's important to separate clean and raw songs because some songs have special characters
          #that would prevent them from given an error when saved them.

          clean_songs = [f'{val+1:03} - {x} - {y}' for val, (x, y) in enumerate(zip(clean_artist, clean_title))]
          raw_songs = [f'{val+1:03} - {x} - {y}' for val, (x, y) in enumerate(zip(song_artist, song_title))]
              
          return clean_songs, raw_songs


      def song_downloader(self, PATH, valid_urls, downloadable_songs):
        """Download the songs in the playlist.

          Valid urls and songs cleaned are used to download and save the downloadable songs.

          It's important to use the cleaned songs instead of the raw songs because some songs have titles 
          or artists with special characters that could cause errors when trying to save the songs in the folder.

        """
        widgets = [progressbar.Percentage(), progressbar.Bar(), progressbar.Timer()]

        bar = progressbar.ProgressBar(max_value=len(valid_urls), 
                                    widgets=widgets).start()
        os.chdir(PATH)
        for val, (url, song) in enumerate(zip(valid_urls, downloadable_songs)):
            time.sleep(0.1)
            music = requests.get(url, stream=True)
            with open(f"{song}.mp3", "wb") as f:
                for chunk in music.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk) 
            bar.update(val+1)


      def get_status(self, valid_urls, invalid_urls):
          """
          Print the status of the playlist, including the number of songs available 
          for download and the number of songs unavailable for download.
          
          """

          print(f'BIRP! {self.month.capitalize()} {self.year}')
          print(f'{len(valid_urls)} songs are available for download')
          print(f'{len(invalid_urls)} songs are unavailable for download')
                          
      def create_folder(self, path):

          """Create a folder to save the songs and additional content for the playlist.

          The folder is named after the month and year of the playlist, and is created at the specified path. If the folder already exists, it is not created again.

          Args:
              path: The path where the folder should be created.

          Returns:
              The absolute path to the created folder.
          """

          folder_name = os.path.join(path, f'Various Artists - BIRP! {self.month.capitalize()} {self.year}')
          if not os.path.exists(folder_name):
              os.mkdir(folder_name)
          return os.path.abspath(folder_name)                        

      def additional_content(self, PATH, downloadable_songs, undownloadable_songs):

          """
          This part performs three different tasks:

          1.Downloads the album cover from the selected playlist.

          2.Creates a text file named "external links" that contains links to download the playlist from other sources. 
          This is highly recommended for newer playlists, as they may not have all the songs available on the streaming site.

          3.Creates a text file named "BIRP! month and year" that contains the social media information of BIRP, 
          as well as the songs that are not available for download (in their raw format). 

          """

          #Downloads the album cover from the selected playlist.
          os.chdir(PATH)
          img_data = requests.get(f'https://www.birp.fm/images/albumart/{self.month}{self.year}.jpg').content
          with open('albumcover.jpg', 'wb') as img:
              img.write(img_data)


          #Creates a text file named "external links" that contains links to download the playlist from other sources.
          playlist_url = f"https://www.birp.fm/playlist/{self.year}/{self.month}-{self.year}"
          r = requests.get(playlist_url)
          soup = BeautifulSoup(r.text, 'lxml')
          data = soup.findAll(class_='playlist-options')
          links = []
          name = []
          for a in data[0].findAll(attrs={'class':"btn playlist-btn"}):
            links.append(a.get('href'))
            name.append(a.text)
          for idx, i  in enumerate(links):
              if i.endswith('.torrent'):
                a =  urljoin('https://www.birp.fm', i.replace(' ', '%20'))
                links[idx] = a
          clean_links = [f"{x}: {y}" for  x, y in zip(name, links)]
          clean_links = clean_links[1::]
          with open(f"External Links BIRP! {self.month.capitalize()} {self.year}.txt", 'w') as f:
            f.write(f'External Links Various Artists - BIRP! {self.month.capitalize()} {self.year}' + '\n')
            f.write('\n')
            for line in clean_links:
              f.write(line+"\n")


            #Creates a text file named "BIRP! month and year" that contains the social media information of BIRP and 
            #the songs that are not available for download 
            sum_sec = 0
            pct = (len(downloadable_songs)/(len(undownloadable_songs) + len(downloadable_songs))) * 100
            for i in os.listdir():
                if i.endswith('mp3'):
                    sum_sec+= MP3(i).info.length
            with open(f'BIRP! {self.month.capitalize()} {self.year}.txt', 'w') as f:
                f.write(f"BIRP! {self.month.capitalize()} {self.year}" + '\n' + '\n')
                f.write('Follow BIRP!' + '\n')
                f.write('YOUTUBE: https://www.youtube.com/channel/UC-HHJWCzskrsPdEjYulBg4w' + '\n')
                f.write('TWITTER: https://twitter.com/birp' + '\n')
                f.write('SPOTIFY: https://open.spotify.com/user/1217281510' + '\n')
                f.write('FACEBOOK: https://www.facebook.com/birp.fm' + '\n')
                f.write('SOUNDCLOUD: https://soundcloud.com/birp' + '\n')
                f.write('INSTAGRAM: https://www.instagram.com/birpfm/' + '\n' + '\n')
                f.write(f"Downloaed {len(downloadable_songs)} songs" + '\n' + '\n')
                f.write(f'Downloaed {pct:.2f}% of total playslist' + '\n' + '\n')
                f.write(f'Album lenght is {format_timespan(sum_sec, max_units=2)}' + '\n' + '\n')
                f.write("List of songs not availiable to download:" + '\n' + '\n')
                for line in undownloadable_songs:
                    f.write(line)
                    f.write('\n')  

      def make_zip(self, PATH):
        """
        This function creates a ZIP archive of playlist folder.

        """
        return shutil.make_archive(PATH, 'zip', PATH)  
