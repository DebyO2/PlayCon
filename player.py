import pygame
import keyboard
from win32gui import GetWindowText, GetForegroundWindow
import os
from main import destiny

pygame.init()
running = True
paused = False
number_of_time_space_pressed = 0
name = ""

MUSIC_END = pygame.USEREVENT+1
# name = "playboi"
def toggle(Global : bool):
    global number_of_time_space_pressed
    global paused
    global name
    if Global:
        if(GetWindowText(GetForegroundWindow()) == name):
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                paused = True
                number_of_time_space_pressed +=1
            else:
                pygame.mixer.music.unpause()
                paused = False
                number_of_time_space_pressed +=1
    else :
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            paused = True
            number_of_time_space_pressed +=1
        else:
            pygame.mixer.music.unpause()
            paused = False
            number_of_time_space_pressed +=1

def leave(Global : bool):
    global running
    global name
    
    if Global:
        if(GetWindowText(GetForegroundWindow()) == name):
            running = False
            pygame.mixer.music.stop()
            
    else :
        running = False
        pygame.mixer.music.stop()


def playSong(path : str,offline :bool):
    global number_of_time_space_pressed
    number_of_time_space_pressed = 0
    global name
    name = GetWindowText(GetForegroundWindow())
    volume = int(input("Volume(1-150): "))/100
    Toloop = int(input("To Loop? (0||1): "))*-1
    # print(name)
    global paused
    global running
    running = True
    print("spacebar         : pause/unpause (within the window)")
    print("ctrl + spacebar  : pause/unpause (global shortcut)")
    print("esc              : stop          (within the window)")
    print("shift + esc      : stop          (global shortcut)\n")
    try :
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(Toloop)
    except:
        print("oops looks like the song doesn't exist are u drunk or something? ")
        return
    keyboard.add_hotkey('space', toggle,args=[(True)])
    keyboard.add_hotkey('escape', leave,args=[(True)])
    keyboard.add_hotkey('ctrl+space', toggle,args=[(False)])
    keyboard.add_hotkey('shift+escape', leave,args=[(False)])
   
    while running:              
        if paused or pygame.mixer.music.get_busy():
            
            continue   
        else:
            print("finished playing")
            break
    
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    keyboard.unhook_all_hotkeys()

    if offline:
        pass
    else:
        todelete = input("save song? (y/n) : ")
        if todelete == "y":
            print("saved")
        elif todelete == "n":
            os.remove(path)
            print("deleted")
    
    for _ in range(number_of_time_space_pressed):
        keyboard.press_and_release('backspace')


def playPlaylist(playlist : str):
    global number_of_time_space_pressed
    number_of_time_space_pressed = 0
    global name
    name = GetWindowText(GetForegroundWindow())
    volume = int(input("Volume(1-150): "))/100
    Toloop = int(input("To Loop? (0||1): "))*-1
    # print(name)
    global paused
    global running

    running = True

    print("spacebar         : pause/unpause (within the window)")
    print("ctrl + spacebar  : pause/unpause (global shortcut)")
    print("esc              : stop          (within the window)")
    print("shift + esc      : stop          (global shortcut)\n")

    keyboard.add_hotkey('space', toggle,args=[(True)])
    keyboard.add_hotkey('escape', leave,args=[(True)])
    keyboard.add_hotkey('ctrl+space', toggle,args=[(False)])
    keyboard.add_hotkey('shift+escape', leave,args=[(False)])

    try :
        path = os.path.join("playlists",f"{playlist}.txt")
        with open(path) as f:
            songs = f.read().split("\n")
        # print(songs)
        print("songs going to be played")
        a = len(str(len(songs)))
        cd = os.path.join(os.getcwd(),'music')
        for i in range(len(songs)):
            # print("shit")
            name0 = songs[i].removeprefix(os.path.join(os.getcwd() ,'music').lstrip('\\')).lstrip("\\")
            print(f"{' '*(a-len(str(i+1)))}{i+1} || {name0}")
            # pass

        
        if Toloop == -1:
            
            pygame.mixer.music.set_volume(volume)
            
            playlist = iter(songs)
            
            pygame.mixer.music.load(next(playlist))
            pygame.mixer.music.queue(next(playlist))
            pygame.mixer.music.play()
            pygame.mixer.music.set_endevent(MUSIC_END)
            while running:
                
                
                for event in pygame.event.get():
                    
                   
                    if event.type == MUSIC_END:
                        print('Song Finished')
                        val = next(playlist,"end")
                        if val == "end":
                            playlist = iter(songs)
                            val = next(playlist)
                        pygame.mixer.music.queue(val)
                        
                    if not pygame.mixer.music.get_busy() and not paused:
                        
                        running = False
                        break
        elif Toloop == 0:
            pygame.mixer.music.load(songs[0])
        
            songs.pop(0)
        
            pygame.mixer.music.play()

            pygame.mixer.music.queue(songs[0])
            songs.pop(0)
        
            pygame.mixer.music.set_endevent(MUSIC_END)
            
            while running:
                
                for event in pygame.event.get():
                    
                    if event.type == MUSIC_END:
                        print('Song Finished')
                        
                        if len(songs) > 0:
                            

                            pygame.mixer.music.queue(songs[0])
                            songs.pop(0)
        
                    
                    if not pygame.mixer.music.get_busy() and not paused:
                        print("Playlist completed")
                        pygame.mixer.music.stop()
                        pygame.mixer.music.unload()
                        running = False
                        break
        
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        keyboard.unhook_all_hotkeys()
        
        for _ in range(number_of_time_space_pressed):
            keyboard.press_and_release('backspace')
    except:
        print("oops some shit happened")
        return
        
if __name__ == '__main__':
    option = input("what do you wanna play? playlist(0) or a music file(1): ")
    if option == "0":
        playlist = input("playlist name: ")
        playPlaylist(playlist)
    elif option == "1":
        porth = input("Enter the path of the song: ")
        playSong(porth,offline=True)
