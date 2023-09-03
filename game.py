import pygame
import characterbuilder
import bestiary
import itemoptions
import utilities
import config
import map_functions
import random

class Game():
    def __init__(self, screen, map):
        self.screen = screen
        self.objects = []
        self.playstate = utilities.PlayState.MENU
        self.map = map
        self.camera = [0, 0]
        self.player_moved = False
    
    def set_up(self, charclass):
        character = charcreator(charclass)
        self.player = character
        self.objects.append(character)
        self.playstate = utilities.PlayState.MAP
        print(str(self.playstate))
        self.map.load_map("map01")
    
    def determine_camera(self):
        pass

    def update(self):
        self.player_moved = False
        self.screen.fill(config.black)
        self.handle_events()

        self.map.render_map(self.screen, self)

        for object in self.objects:
            object.render(self.screen, self.camera)
        
        if self.player_moved:
            self.determine_game_events()
    
    def determine_game_events(self):
        map_tile = self.map.maplist[self.player.position[1]][self.player.position[0]]

        if map_tile == config.MAP_TILE_ROAD:
            return
        
        self.determine_monster(map_tile)
    
    def determine_monster(self, tile):
        random_number = random.randint(1, 10)
        if random_number <= 2:
            match tile:
                case "G":
                    monsterhome = "Grassland"
                case "M":
                    monsterhome = "Mountains"
                case "f":
                    monsterhome = "Fairy Forest"
                case "S":
                    monsterhome = "Swamp"
                case "c":
                    monsterhome = "Cave"
                case "F":
                    monsterhome = "Forest"
                case "t":
                    monsterhome = "Town"
            found_monster = bestiary.choosemonster(monsterhome)
            print("You Found a Monster!")
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                utilities.end_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    utilities.end_game()
                elif event.key == pygame.K_w: #move up
                    self.move_unit(self.player, [0, -1])
                elif event.key == pygame.K_s: #move down
                    self.move_unit(self.player, [0, 1])
                elif event.key == pygame.K_a: #move left
                    self.move_unit(self.player, [-1, 0])
                elif event.key == pygame.K_d: #move right
                    self.move_unit(self.player, [1, 0])
    
    def move_unit(self, unit, position_change):
        new_position = [unit.position[0] + position_change[0], unit.position[1] + position_change[1]]
        if new_position[0] < 0 or new_position[0] > (len(self.map.maplist[0]) - 1):
            return
        if new_position[1] < 0 or new_position[1] > (len(self.map.maplist) - 1):
            return
        if self.map.maplist[new_position[1]][new_position[0]] == "W":
            return
        
        self.player_moved = True
        unit.update_position(new_position)

    def get_monster(self):
        pass

#Update and move these functions as appropriate to interface with a visual UI
def statsokay(prio):
    charstats = characterbuilder.buildstatblock(prio)
    print("Your player stats are: " + str(charstats))
    answer = input("Would you like to reroll? (y/n)")
    while answer == "y":
        charstats = characterbuilder.buildstatblock(prio)
        print("Your player stats are: " + str(charstats))
        answer = input("Would you like to reroll? (y/n)")
    return charstats

def charcreator(charclass):
    print(charclass)
    if (charclass == 1):
        playerstats = statsokay("melee")
        hdie = 10
        armor = itemoptions.chain
        weapon = itemoptions.sword
        playerclass = "Fighter"
    elif charclass == 2:
        playerstats = statsokay("ranged")
        hdie = 8
        armor = itemoptions.leather
        weapon = itemoptions.bow
        playerclass = "Archer"
    elif charclass == 3:
        playerstats = statsokay("caster")
        hdie = 6
        armor = itemoptions.padded
        weapon = itemoptions.wand
        playerclass = "Wizard"
    
    charname = input("What would you like to name your character? ")
    return characterbuilder.Player(charname, playerclass, playerstats, hdie, armor, 1, weapon, [], 0, 1, 1)