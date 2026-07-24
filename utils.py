import sys
import os

import pygame

def resource_path(relative_path):

    ''' 
    Get absolute path to resource, works for dev (e.g. running a python script)
    and for PyInstaller (when packaged as an executable).
    '''

    try: # PyInstaller creates a temp folder containing your files and stores the path in sys._MEIPASS
        base_path = sys._MEIPASS

    except AttributeError:
        base_path = os.path.abspath(".")

        '''
            Since sys._MEIPASS is only available when the script is packaged with PyInstaller, 
            we use a try-except block to see it the variable exists. 

            If it does, we use it as the base path for our resource files.

            If it doesn't, we use the current working directory (os.path.abspath(".")) as the base path.

            The "base_path" variable is basically what comes before the relative path of the resource file.

            For example, if you have a resource file located at "images/icon.png", the relative path is "images/icon.png".
            The absolute path would be something like "C:/Users/YourUsername/YourProject/images/icon.png" when running the script directly, 

            or "C:/Users/YourUsername/AppData/Local/Temp/_MEIxxxxxx/images/icon.png" when running the packaged executable.

            Here's how we join them:            
            '''
    return os.path.join(base_path, relative_path)


def save_path(relative_path):

    if getattr(sys, 'frozen', False): 
        '''
        getattr() is a built-in Python function that returns the value of the named attribute of an object.
        In simple terms, it checks if the script is running in a "frozen" state, which means it's packaged as an executable (like with PyInstaller).
        It takes in two arguments: the object to check (in this case, sys) and the name of the attribute to look for ('frozen').
        "False" is the default value to return if the attribute doesn't exist.
        '''

        base_path = os.path.dirname(sys.executable)  # Get the directory of the executable

    else:

        base_path = os.path.abspath(".")  # Get the current working directory

    return os.path.join(base_path, relative_path)  # Join the base path with the relative path to get the full path




def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


def blit_rotate_center(screen, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    screen.blit(rotated_image, new_rect.topleft)


'''
    1. I'm adding a resource_path() helper function to get the absolute path of a resource file since when packaging
        with PyInstaller, the relative paths may not work as expected. This function will help locate the resource files 
         correctly whether the script is run directly or packaged.

    2. I'm adding a save_path() helper function to write the high score text file where it'll exist even after the game is closed. 
        This location need to be a place where the exe is allowed to write files. The current working directory is a good choice for this.
'''