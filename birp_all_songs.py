import csv
import time
import requests 
from bs4 import BeautifulSoup
import re 

# Record the starting time
start_time = time.perf_counter()
months = ["january", "february", "march", "april", 
          "may", "june", "july", "august", "september", 
          "october", "november", "december"]
          
for year in range(2009, 2022+1):
  for month in months:
    # Playlist URL
    playlist_url = f"https://www.birp.fm/playlist/{str(year)}/{month}-{str(year)}"
    r = requests.get(playlist_url)
    if r.ok:
      # Get the HTML content of the playlist
      r = requests.get(playlist_url)
      soup = BeautifulSoup(r.text, "lxml")
      # Find all song titles and song artists in the HTML
      song_title = soup.find_all("span", attrs={"class":"song-title"})
      song_artist = soup.find_all("span", attrs={"class":"song-artist"})

      # Extract the text from each song title and artist
      song_title = [x.text for x in song_title]
      song_artist = [x.text for x in song_artist]

      # Clean the text of each song title and artist
      clean_artist= [re.sub(r"[^a-zA-Z0-9 ]", "", i) for i in song_artist]
      clean_title = [re.sub(r"[^a-zA-Z0-9 ]", "", i) for i in song_title]

      # Open a CSV file for writing
      with open("playlistbirp_raw.csv", "a+", newline="") as file_1, \
           open("playlistbirp_clean.csv", "a+", newline="") as file_2:
          # Create a CSV writer object with the fieldnames "title", "artist", "month", "year"
          writer1 = csv.DictWriter(file_1, fieldnames=["title", "artist", "month", "year"])
          writer2 = csv.DictWriter(file_2, fieldnames=["title", "artist", "month", "year"])
          # Write the fieldnames to the CSV file
          writer1.writeheader()
          writer2.writeheader()
          # Loop through the song titles and artists
          for i in range(len(song_title)):
              # Write each song title and artist to the CSV file
              writer1.writerow({"title":song_title[i], "artist":song_artist[i], "month": month, "year":str(year)})
              writer2.writerow({"title":clean_title[i], "artist":clean_artist[i], "month": month, "year":str(year)})

# Calculate the time taken by the function in minutes
end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f"Elapsed time: {(elapsed_time) / 60:.2f} minutes")