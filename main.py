import math
import os
import random as rand
import sys
import time
import pygame
from pygame.locals import *

pygame.init()

waiting_for_user_input = pygame.image.load("Image files/Other images/waiting for user input.png")
background = pygame.image.load("Image files/Other images/mountainsbackdrop.png")
panda_image = pygame.image.load("Image files/Player and Zombie images/Player images/walking player 1.png")
walking_player_1 = pygame.image.load("Image files/Player and Zombie images/Player images/walking player 1.png")
walking_player_2 = pygame.image.load("Image files/Player and Zombie images/Player images/walking player 2.png")
walking_player_3 = pygame.image.load("Image files/Player and Zombie images/Player images/walking player 3.png")
walking_player_4 = pygame.image.load("Image files/Player and Zombie images/Player images/walking player 4.png")
walking_player_5 = pygame.image.load("Image files/Player and Zombie images/Player images/walking player 5.png")
bandage = pygame.image.load("Image files/Pickup item images/bandage.png")
coin = pygame.image.load("Image files/Pickup item images/coin.png")
medkit = pygame.image.load("Image files/Pickup item images/medkit.png")
shield = pygame.image.load("Image files/Pickup item images/shield.png")
bullet_image = pygame.image.load("Image files/Other images/bullet.png")

width = 800
height = 512

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Zombie Shooter')
pygame.display.update()

player_speed = 1
xposition = 0
yposition = 0

zombies = []
bullets = []
knifeswipes = []
knife_damage = 10

def run_game():
    global moving, firing, xposition, yposition, zombies, bullets, knifeswipes
    moving = False
    firing = False

    os.system("clear")

    panda_image = pygame.image.load("Image files/Player and Zombie images/Player images/walking player 1.png")

    xposition = screen.get_width() / 2 + panda_image.get_width() / 2
    yposition = screen.get_height() / 2 + panda_image.get_height() / 2

    zombies = []
    bullets = []
    knifeswipes = []
    number_of_zombies = 0
    health = 100
    max_health = 100
    shield_up = False

    while True:
        reblit()

        if health <= 0:
            menu(UDIED=True)

        if len(zombies) < number_of_zombies and time.time() - 1 >= Zombie.last_zombie_killed:
            number_of_zombies += 1
            if rand.randint(1, 7) != 7:
                zombies.append(Normal(rand.randint(0, screen.get_width()), rand.randint(0, screen.get_height())))
            elif rand.randint(1, 7) != 7:
                zombies.append(Ninja(rand.randint(0, screen.get_width()), rand.randint(0, screen.get_height())))
            else:
                zombies.append(Tank(rand.randint(0, screen.get_width()), rand.randint(0, screen.get_height())))

        for zombie in zombies:
            player_x = xposition + panda_image.get_width() / 2
            player_y = yposition + panda_image.get_height() / 2
            distance_x = player_x - zombie.x
            distance_y = player_y - zombie.y
            angle = math.atan2(distance_x, distance_y)
            zombie.x += math.cos(angle) * zombie.speed
            zombie.y += math.sin(angle) * zombie.speed

            if zombie.health == 0:
                zombie.died = True
                zombie.speed = 0
                zombie.damage = 0
                if rand.randint(1, 5) != 4 or 5:
                    zombie.image_file = coin
                elif rand.randint(1, 5) != 4 or 5:
                    zombie.image_file = bandage
                elif rand.randint(1, 5) != 4 or 5:
                    zombie.image_file = shield
                else:
                    zombie.image_file = medkit

            if zombie.died == True:
                distance = math.sqrt((player_x - zombie.x)**2 + (player_y - zombie.y)**2)
                threshold_distance = 10
                if distance < threshold_distance:
                    pickup = zombie
                    zombies.remove(zombie)
                    if pickup.image_file == coin:
                        MONEYMONEYMONEY += 2
                    elif pickup.image_file == bandage:
                        health += 35
                        if health >= max_health:
                            health = max_health
                    elif pickup.image_file == shield:
                        if shield_up:
                            destroy_shield_time += 5
                        else:
                            destroy_shield_time = time.time() + 5
                            shield_up = True
                    elif pickup.image_file == medkit:
                        max_health += 50
                        health = max_health

                    if shield_up and time.time() < destroy_shield_time:
                        pygame.draw.circle(screen, (75, 75, 255), (player_x, player_y), 50)
                        for zombie in zombies:
                            for i in range(player_x - 50, player_x + 50):
                                for j in range(player_y - 50, player_y + 50):
                                    if zombie.x == i and zombie.y == j:
                                        zombie.health = 0

        for bullet in bullets:
            bullet.move()
            for zombie in zombies:
                if check_collision(bullet, zombie):
                    zombie.health -= bullet.damage
                    bullets.remove(bullet)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    moving = True
                    yposition -= player_speed
                elif event.key == pygame.K_a:
                    moving = True
                    xposition -= player_speed
                elif event.key == pygame.K_s:
                    moving = True
                    yposition += player_speed
                elif event.key == pygame.K_d:
                    moving = True
                    xposition += player_speed
                else:
                    moving = False
                if event.key == pygame.K_e:
                    weapons["smg"].player_holding = not weapons["smg"].player_holding
                    weapons["sniper"].player_holding = not weapons["sniper"].player_holding
                elif event.key == pygame.K_q:
                    menu()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            firing = True
                            mouse_pos = pygame.mouse.get_pos()
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            player_x = xposition + panda_image.get_width() / 2
                            player_y = yposition + panda_image.get_height() / 2
                            distance_x = mouse_pos[0] - player_x
                            distance_y = mouse_pos[1] - player_y
                            angle = math.degrees(math.atan2(distance_y, distance_x))
                            if firing:
                                bullet_x = xposition + panda_image.get_width() / 2
                                bullet_y = yposition + panda_image.get_height() / 2
                                bullet_direction = math.atan2(mouse_y - bullet_y, mouse_x - bullet_x)
                                current_weapon_name = current_weapon()
                                if current_weapon_name is not None:
                                    bullets.append(
                                        Bullet(
                                            bullet_x, bullet_y, bullet_direction, weapons[current_weapon_name].speed
                                        )
                                    )
                                firing = False
                        if event.button == 3:
                            knifeswipes.append(KnifeSwipe(xposition + panda_image.get_width() / 2, yposition + panda_image.get_height() / 2))
            if event.type == QUIT:
                pygame.quit()

        pygame.display.update()

def menu(start=False, UDIED=False):
    global MONEYMONEYMONEY
    if UDIED:
        print("U died lol\n\nEMOTIONAL DAMAGE")
    if start:
        MONEYMONEYMONEY = 100
        print("Welcome to Panda vs Zombies!\n\n")
    screen.fill((0, 0, 0))
    screen.blit(waiting_for_user_input,
                (500 - (waiting_for_user_input.get_width() / 2), 400 - (waiting_for_user_input.get_height() / 2)))
    os.system("clear")
    print("This is the menu, please select one of the options below:")
    while True:
        try:
            option = int(
                input(
                    "•1: Start a new round.\n•2: Upgrade a weapon.\n•3: Quit the game.\n\n(Just type 1, 2 or 3 to choose an option.)\n\n"
                ))
            break
        except:
            print("Please just choose 1, 2 or 3.")
            time.sleep(1)
            os.system("clear")
    if option == 1:
        run_game()
    if option == 2:
        os.system("clear")
        print("Which weapon do you want to upgrade?")
        while True:
            try:
                option = int(
                    input(
                        "•1: Sniper.\n•2: SMG.\n\n(Just type 1 or 2 to choose an option.\n\n"
                    ))
                break
            except:
                print("Please just choose 1 or 2.")
                time.sleep(1)
                os.system("clear")
        if option == 1:
            if weapons["sniper"].level != 5:
                if weapons["sniper"].time_to_wait <= MONEYMONEYMONEY:
                    print(
                        f"The upgrade costs {weapons['sniper'].time_to_wait} coins and you have {MONEYMONEYMONEY}."
                    )
                    while True:
                        option = input(
                            "Would you like to buy it?\n\n(Type \"y\" for yes or \"n\" for no.\n\n"
                        )
                        if option == "y":
                            MONEYMONEYMONEY -= weapons['sniper'].time_to_wait
                            weapons['sniper'].level += 1
                            print("Your purchase has been completed.")
                            time.sleep(1)
                            menu()
                        elif option == "n":
                            os.system("clear")
                            menu()
                        else:
                            print("Please select a valid option.")
                else:
                    print(
                        f"The upgrade costs {weapons['sniper'].time_to_wait} gold, but you only have {MONEYMONEYMONEY} gold, meaning you don't have enough money to purchase this."
                    )
                    time.sleep(2)
                    menu()
            else:
                print(
                    "Your level for this item is already maxed. Try upgrading another item, or if you already have, just try stacking coins."
                )
                time.sleep(2)
                menu()
        if option == 2:
            if weapons["smg"].level != 5:
                if weapons["smg"].time_to_wait <= MONEYMONEYMONEY:
                    print(
                        f"The upgrade costs {weapons['smg'].time_to_wait} coins and you have {MONEYMONEYMONEY}."
                    )
                    while True:
                        option = input(
                            "Would you like to buy it?\n\n(Type \"y\" for yes or \"n\" for no.\n\n"
                        )
                        if option == "y":
                            MONEYMONEYMONEY -= weapons["smg"].time_to_wait
                            weapons["smg"].level += 1
                            print("Your purchase has been completed.")
                            time.sleep(1)
                            menu()
                        elif option == "n":
                            os.system("clear")
                            menu()
                        else:
                            print("Please select a valid option.")
                else:
                    print(
                        f"The upgrade costs {weapons['smg'].time_to_wait} gold, but you only have {MONEYMONEYMONEY} gold, meaning you don't have enough money to purchase this."
                    )
                    time.sleep(2)
                    menu()
            else:
                print(
                    "Your level for this item is already maxed. Try upgrading another item, or if you already have, just try stacking coins."
                )
                time.sleep(2)
                menu()
    if option == 3:
        os.system("clear")
        sys.exit()

def reblit():
    screen.blit(background, (0, 0))
    screen.blit(panda_image, (xposition, yposition))
    for zombie in zombies:
        screen.blit(zombie.image_file, (zombie.x, zombie.y))
    for bullet in bullets:
        bullet.draw()
    for swipe in knifeswipes:
        swipe.draw()

def check_collision(obj1, obj2):
    if isinstance(obj1, Bullet):
        return obj1.x > obj2.x and obj1.x < obj2.x + obj2.image_file.get_width() and obj1.y > obj2.y and obj1.y < obj2.y + obj2.image_file.get_height()
    if isinstance(obj1, KnifeSwipe):
        return obj1.x > obj2.x and obj1.x < obj2.x + obj2.image_file.get_width() and obj1.y > obj2.y and obj1.y < obj2.y + obj2.image_file.get_height()
    return False

class Gun:
    def __init__(self, name, damage, time_to_wait, automatic, speed):
        self.name = name
        self.damage = damage
        self.time_to_wait = time_to_wait
        self.automatic = automatic
        self.speed = speed
        self.level = 1
        self.player_holding = False

class Bullet:
    def __init__(self, x, y, direction, speed):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.damage = weapons[current_weapon()].damage

    def move(self):
        self.x += math.cos(self.direction) * self.speed
        self.y += math.sin(self.direction) * self.speed

    def draw(self):
        rotated_bullet = pygame.transform.rotate(bullet_image, -math.degrees(self.direction))
        screen.blit(rotated_bullet, (int(self.x), int(self.y)))

class Zombie:

    last_zombie_killed = time.time()

    def __init__(self, image_file, health, max_health, damage, speed, died, x, y):
        self.image_file = image_file
        self.health = health
        self.max_health = max_health
        self.damage = damage
        self.speed = speed
        self.died = died
        self.x = x
        self.y = y

class Ninja(Zombie):
    def __init__(self, x, y, image_file="Image files/Player and Zombie images/Zombie images/ninja zombie.png", health=10, max_health=10, damage=15, speed=3, died=False):
        super().__init__(image_file, health, max_health, damage, speed, died, x, y)

class Tank(Zombie):
    def __init__(self, x, y, image_file="Image files/Player and Zombie images/Zombie images/tank zombie.png", health=35, max_health=35, damage=10, speed=1, died=False):
        super().__init__(image_file, health, max_health, damage, speed, died, x, y)

class Normal(Zombie):
    def __init__(self, x, y, image_file="Image files/Player and Zombie images/Zombie images/original zombie.png", health=20, max_health=20, damage=10, speed=2, died=False):
        super().__init__(image_file, health, max_health, damage, speed, died, x, y)

class KnifeSwipe:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.damage = knife_damage

    def draw(self):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), 15)
        for zombie in zombies:
            if check_collision(self, zombie):
                zombie.health -= self.damage


def current_weapon():
    for weapon in weapons.values():
        if weapon.player_holding:
            return weapon.name
    return None

weapons = {
    "smg": Gun("smg", 5, 15, True, 10),
    "sniper": Gun("sniper", 20, 50, False, 20),
}

menu(start=True)