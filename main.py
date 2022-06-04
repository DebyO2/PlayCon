import asyncio
from youtubesearchpython.__future__ import VideosSearch
import os
import downloader
import player
import playlist_manager

#Global
SongLink = ""

destiny = "music"
branch = os.path.join(os.getcwd(),destiny)+"\\"

def showSongs(mode:int):
    if mode == 0:
        playlists = list(os.listdir(destiny))
        a = len(str(len(playlists)))

        for i in range(len(playlists)):

            print(f"{' '*(a-len(str(i+1)))}{i+1} || {playlists[i]}")
        return playlists
    elif mode == 1:
        poth = "playlists"
        playlist = list(os.listdir(poth))
        a = len(str(len(playlist)))

        for i in range(len(playlist)):

            print(f"{' '*(a-len(str(i+1)))}{i+1} || {playlist[i]}")
        return playlist
    elif mode == 2:
        poth = "playlists"
        playlist = list(os.listdir(poth))
        for i in playlist:
            print(f"({playlist.index(i)+1}) playlist : {i}")
            with open(os.path.join(poth,i),"r") as f:
                songs = f.read().split("\n")
                a = len(str(len(songs)))
                for line in range(len(songs)):
                    if songs[line]:
                        print(f"\t{' '*(a-len(str(line+1)))}{line+1} || {songs[line].removeprefix(branch)}")
        return playlist



async def search(play):
    query = input("Enter the music name and if possible then add by (artist): ")
    videosSearch = VideosSearch(query, limit = 3)
    videosResult = await videosSearch.next()
    
    result = videosResult["result"]

    if len(result) == 0:
        print("No results found")
        return

    Songs = {}

    for i in result:
        print("\n")
        print(f'({list(result).index(i)+1}) By: {i["channel"]["name"]} ||\n    Title: "{i["title"]}" ||\n    Duration: "{i["duration"]}" ||\n    Link : "{i["link"]}"')

        Songs.update({i["title"] : i["link"]})
    
    songIndex = int(input("\nWhich song do u want (1 || 2 || 3): ")) - 1

    SongLink = Songs[list(Songs)[songIndex]]
    
    sung = downloader.DownloadMusic(SongLink)
    if play:
        print(f"playing: {sung[2]} ....")

        if sung[0] == True:
            
            player.playSong(sung[1],offline=False)
        elif sung[0] == False:
            print("the song is already downloaded,will be played from the database")
            
            player.playSong(sung[1],offline=True)
    
    elif not play:
        print(f"song downloaded")


if __name__ == '__main__':

    while True:
        try:
            command = input("\nEnter your command(use help to know the commands): ").lower()
            if command == 'play':
                mode = input("\nEnter your mode(offline/online): ")

                if mode == 'offline':
                
                    
                    foles = showSongs(0)

                    try:
                        songtoplay = int(input("\nWhich song do u want to play(1,2,3...): ")) - 1
                        
                        sang = foles[songtoplay]

                        poth = os.path.join(destiny,sang).replace('\\',r"\\")
                        
                        print(f"\nplaying: {sang} ....\n")

                        player.playSong(poth,offline=True)
                    except:
                        print("oops something went wrong")
                
                elif mode == "online":
            
                    asyncio.run(search(play=True))

            elif command == "exit" or command == "e":
                break
                

            elif command == "delete":
                sucns = list(os.listdir(destiny))
                sunc = ""
                
                for w in sucns:
                    print(f"{sucns.index(w) + 1} || {w}")
                
                try:
                    songtodel = int(input("\nWhich song do u want to delete(1,2,3...): ")) - 1
                    sunc = sucns[songtodel]

                    puth = os.path.join(destiny,sunc).replace('\\',r"\\")
                    
                    os.remove(puth)

                    print(f"deleted: {sunc} ....")
                except Exception as e:
                    print("oops something went wrong")
                    print(e)
            
            elif command == "show":
            
                showSongs(0)
            

            elif command == "help":
                print('| play : to play the songs\n| exit/e : to exit\n| delete : to delete a song from the database\n| show : shows all the songs in database\n| download : download songs\n| playlist show : show all the playlists\n| playlist show songs : show playlists with all the songs inside them\n| playlist add songs : add songs to your playlist')

            elif command == "download":
                asyncio.run(search(play=False))

            elif command.startswith("playlist"):
                if command == "playlist show":
                    showSongs(1)
                
                if command == "playlist show songs":
                    showSongs(2)
                
                if command == "playlist create":
                    name = input("\nEnter the name of the new playlist: ")
                    playlist_manager.create_playlist(name)

                if command == "playlist delete":
                    playlists = showSongs(2)
                    pl = int(input("\nEnter the name of the playlist you want to delete: ")) - 1
                    name = playlists[pl]
                    # print(name)
                    playlist_manager.delete_playlist(name)
                
                if command == "playlist delete songs":
                    
                    playlists = showSongs(2)
                    pl = int(input("\nEnter the name of the playlist you want to delete the songs from(1,2,3,..): ")) - 1
                    playlist_name = playlists[pl]
                    # print(pl)
                    # print(playlists)
                    # print(playlist_name)
                    path = os.path.join("playlists",playlist_name)
                    songhs = []
                    with open(path,"r") as f:
                        print("\n")
                        songs = f.read().split("\n")
                        a = len(str(len(songs)))
                        for line in range(len(songs)):
                            if songs[line]:
                                print(f"{' '*(a-len(str(line+1)))}{line+1} || {songs[line].removeprefix(branch)}")
                                songhs.append(songs[line].removeprefix(branch))
                        
                    nu = list(map(lambda x: int(x) -1,input("\nEnter the song number you want to delete(1,2,3...): ").strip().split(' ')))
                    for yo in nu:
                        # print(songhs[yo])
                        song = songhs[yo]
                        playlist_manager.delete_song(song,playlist_name)
                if command == "playlist add songs":
                    # pass
                    # print("which playlist do u want to add to? ")
                    playlists = showSongs(2)
                    pl = int(input("\nWhich playlist do u want to add to ? (1,2,3...): ")) - 1
                    playlist_name = playlists[pl]
                    # print("which song do u want to add to the playlist? ")
                    songs = showSongs(0)
                    
                    sl = list(map(lambda x: int(x) -1,input("\nwhich songs do u want to add to the playlist? (1,2,3...): ").strip().split(' ')))

                    for hmm in sl:
                        song_name = songs[hmm]
                        song_path = os.path.join("music",song_name)
                        playlist_manager.add_song(song_path,playlist_name)
                    # print(sl)
                
            else:
                print("give the computer to your mom kid")
        except Exception as e:
            print("oops something went wrong")
            print(e)
