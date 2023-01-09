import os
import pygame
import subprocess
import shutil

# fetching variable data.
dir = "E:/Software/Games/Emulators"
os.chdir(f"{dir}/savestate_sharing/")

def receive():

    # this pulls the github repo to local drive.
    subprocess.run([f"{dir}/savestate_sharing/pull.bat"], shell=True)

    # this copies all the files from savestate_sharing/states into Mesen/SaveStates.
    files = os.listdir(f"{dir}/savestate_sharing/states_snes")
    for file in files:
        shutil.copyfile(f"{dir}/savestate_sharing/states_snes/{file}", f"{dir}/Snes9x/Saves/{file}")

    pygame.display.set_caption("Two-player SNES sharer (RECEIVED)")

def send():

    # this copies all the files from Mesen/SaveStates into savestate_sharing/states.
    files = os.listdir(f"{dir}/Snes9x/Saves")
    for file in files:
        shutil.copyfile(f"{dir}/Snes9x/Saves/{file}", f"{dir}/savestate_sharing/states_snes/{file}")

    # this pushes the savestate_sharing directory to github.
    subprocess.run([f"{dir}/savestate_sharing/push.bat"], shell=True)
    pygame.display.set_caption("Two-player SNES sharer (SENT)")

def main():

    bg = pygame.image.load(f"{dir}/savestate_sharing/UI.png")
    clicks = pygame.image.load(f"{dir}/savestate_sharing/UI_click_regions.png")
    send_click = pygame.image.load(f"{dir}/savestate_sharing/UI_send_clicked.png")
    receive_click = pygame.image.load(f"{dir}/savestate_sharing/UI_receive_clicked.png")

    click_timer = 0
    splash_duration = 1
    which_button_clicked = None

    while True:

        click_timer -= 1 if click_timer > 0 else 0

        # this is the click overlay which makes click region checking easy.
        screen.blit(clicks, (0,0))

        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                screen_surf = pygame.display.get_surface()
                px_array = pygame.PixelArray(screen_surf)
                pixel = pygame.Color(px_array[x, y])
                del px_array
                if pixel[1] == 255:
                    click_timer = splash_duration
                    which_button_clicked = "send"
                elif pixel[2] == 255:
                    click_timer = splash_duration
                    which_button_clicked = "receive"

            elif event.type == pygame.QUIT:
                exit()

        if click_timer == 0:
            screen.blit(bg, (0,0))
        else:
            if which_button_clicked == "send":
                screen.blit(send_click, (0,0))
                pygame.display.flip()
                if click_timer == splash_duration:
                    send()
            elif which_button_clicked == "receive":
                screen.blit(receive_click, (0,0))
                pygame.display.flip()
                if click_timer == splash_duration:
                    receive()

        pygame.display.flip()
        clock.tick(fps)

if __name__ == "__main__":
    # pygame defaults
    pygame.init()
    screen = pygame.display.set_mode((400, 162))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Two-player SNES sharer")
    fps = 60
    main()