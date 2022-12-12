from birpdownloader import Birpdownloader

#Instantiate the class, pass the year and month as strings
p = Birpdownloader('2018', 'april')
#Get the URLs of the songs in the playlist
valid_urls, invalid_urls, total_urls = p.get_song_urls()

#Print the number of available songs for download
p.get_status(valid_urls, invalid_urls)

#Get the names of the songs in the playlist
clean_songs, raw_songs = p.get_song_name()
#Get the indexes of the downloadable and undownloadable songs in the playlist
downloadable_songs, undownloadable_songs = p.get_indexes(valid_urls, invalid_urls, total_urls, clean_songs, raw_songs)
#Create a folder to save the download songs.
PATH = p.create_folder(r'C:\Users\pegas\tkinter_projetos\.tkinter\birp_downloader')
#Download the selected playlist
p.song_downloader(PATH, valid_urls, downloadable_songs)
#Create a txt with additional content and external links
p.additional_content(PATH, downloadable_songs, undownloadable_songs)