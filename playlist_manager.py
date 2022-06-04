import os

def clean(playlist:str):
    path = os.path.join("playlists",playlist)
    try:
        with open(path,"w") as f:
            
            with open(path,"r") as r:

                content = r.read()
                new_content = content.replace("\n","")
                f.write(new_content)
    except Exception as e:
        print("Error")
        print(e)

def create_playlist(name:str):
    path = os.path.join("playlists",f"{name}.txt")
    if not os.path.exists(path):
        f = open(path,"w+")
        print(f"Created playlist {name}")
        return
    else:
        print("Playlist already exists")

# create_playlist("favs")

def add_song(name_with_path:str,playlist_name:str):
    path = os.path.join("playlists",playlist_name)

    try :
        with open(path,"r+") as f:
            if name_with_path in f.read():
                print("Song already exists in the playlist")
                
            elif name_with_path not in f.read():
                with open(path,"r") as r:
                    content = r.read()
                if content:
                    f.write("\n"+name_with_path)
                else:
                    f.write(name_with_path)
                
                print("Song added to the playlist")

    except Exception as e:
        print("something went wrong")
        print(e)

# add_song("song2.mp3","favs")

def delete_song(name_with_path:str,playlist_name:str):
    path = os.path.join("playlists",playlist_name)
    try:
        with open(path,"r+") as f:
            prev_content = f.read()
            if name_with_path in prev_content:
                new_content = prev_content.replace(name_with_path,"").replace("\n\n","\n")
                f.seek(0)
                f.truncate()
                f.write(new_content)
                clean(playlist_name)
                print("Song deleted from the playlist")
                return
            elif name_with_path not in prev_content:
                print("Song not found in the playlist")
                return
    except Exception as e:
        print("something went wrong")
        print(e)
# delete_song("song2.mp3","favs")

def delete_playlist(name:str):
    path = os.path.join("playlists",name)
    try:
        os.remove(path)
        print("Playlist deleted")
    except:
        print("playlist not found")
# delete_playlist("favs2")
