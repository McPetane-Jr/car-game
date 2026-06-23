#Let's make a function that can take an image and return to us a rotated image
import pygame
pygame.init()




def blit_rotate_center4(screen, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle) #we're storing the pygame function that transforms(rotates) an image in the shown variable

    #The problem now is that pygame.transform.rotate(image, angle) works exactly like pygame itself
    #It rotates the image from the top left corner
    #Here's how we center that

    new_rect = rotated_image.get_rect(
        center=image.get_rect(top_left=top_left).center)
    #watch the "Pygame Car Racing Tutorial #1 - Moving The Car" at 28 min for further explanation
    #But the whole point of new_rect is so we find the correct x,y coors so when the image rotates it rotates from the center
    #now draw the rotated image at new_rect

    screen.blit(rotated_image, new_rect.topleft)

def blit_rotate_center(screen, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    screen.blit(rotated_image, new_rect.topleft)