# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 12:25:14 2023

@author: Josiah Hamilton
"""
import time
import random
import textwrap
import pickle
import os
from pathlib import Path

#%%Classes

class Player:
    def __init__(self):
        self.coin=1
        self.deaths=0
        self.chapterDeaths=0
        self.kills=0
        self.strength=1
        self.chapter=[]
        self.playerHP=1
        self.inventory=['map', 'compass']
        self.food=[]
        self.playerName='Lazy'
        self.visited=[]
        self.avatarName=''
        self.bearing=(-1,0,0)
        self.coordinates=(0,0,9)
        self.respawnPoint=(0,0,9)
        self.tick=0
        self.lastPlace=(0,0,9)

yo = Player()

#This defines the bare minimum to qualify as a location.
class Place:
    def __init__(self, icon, inshort):
        self.icon = icon
        self.inshort = inshort


class Wall(Place):
    def __init__(self, icon, inshort):
        super().__init__(icon, inshort)

    def __call__(self):
        goBack()


#This is the main class for places.
class Spot(Place):
    def __init__(self, icon, inshort, description, loot, supplies, npc):
        super().__init__(icon, inshort)
        self.description = description
        self.loot = loot
        self.supplies = supplies
        self.npc = npc

    def __call__(self):

        print('=============================================================================')

        self.describe()

        self.npcScenario()

    def npcScenario(self):
        NPCs = [obj for obj in self.npc if isinstance(obj, Character)]

        if NPCs:
            for x in NPCs:
                x()

    def dropLoot(self, item):
        if item in yo.food:
            yo.food.remove(item)
            self.supplies.append(item)
        elif item in yo.inventory:
            yo.inventory.remove(item)
            self.loot.append(item)
        else:
            dmCompact('You don\'t have any of that to drop.')

    def takeLoot(self, item):
        if item in self.supplies:
            self.supplies.remove(item)
            yo.food.append(item)
        elif item in self.loot:
            self.loot.remove(item)
            yo.inventory.append(item)
        else:
            dmCompact("That isn't here.")

    def describe(self):
        if yo.coordinates not in yo.visited:
            dmCompact(self.description)
            yo.visited.append(yo.coordinates)
        else:
            dmCompact(self.inshort)

        describeSurroundings()
        self.describeItems()

    def describeLong(self):
        dmCompact(self.description)
        describeSurroundings()
        self.describeItems()

    def describeItems(self):
        items = [", ".join(filter(None, [", ".join(self.loot), ", ".join(self.supplies)]))]

        if items[0]:
            print('-----------------------------------------------------------------------------')
            dmCompact(f'Items: {items[0]}')


# Named after the all-containing flat rocks, that appear to any adventurer in time of need.
class FlatRock(Spot):
    def __init__(self, icon, inshort, description, loot, supplies, npc):
        super().__init__(icon, inshort, description, loot, supplies, npc)

    def __call__(self):
        print('=============================================================================')

        self.visitFlatRock()
        self.describe()

        self.npcScenario()

    def describeItems(self):
        items = [", ".join(filter(None, [", ".join(self.loot), ", ".join(self.supplies)]))]
        if items[0]:
            print('-----------------------------------------------------------------------------')
            dmCompact(f'In the {self.inshort}: {items[0]}')

    def visitFlatRock(self):
        dmCompact(f'On the ground, you see a {self.inshort}.')
        choices = [f'Open {self.inshort}','Ignore']
        choice = forceChoice(choices)

        if choice == 0:
            dmCompact(f'You open the {self.inshort}.')
        else:
            goBack()


class Tree(FlatRock):
    def __init__(self, icon, inshort, description, loot, supplies, npc, fruit):
        super().__init__(icon, inshort, description, loot, supplies, npc)
        self.fruit = fruit

    def visitFlatRock(self):
        dmCompact(f'Standing before you is a tall {self.fruit} tree.')
        choice = forceChoice([f'Shake the {self.fruit} tree.', f'Who needs {self.fruit}s anyway?'])

        if choice == 0:
            dmCompact('You shake the tree, and a fruit hits you on the head.')
            self.supplies.append(self.fruit)
        else:
            goBack()

    def describe(self):
        # dmCompact(self.description)
        if yo.coordinates in yo.visited:
            yo.visited.remove(yo.coordinates)

        describeSurroundings()
        self.describeItems()

    def describeItems(self):
        items = [", ".join(filter(None, [", ".join(self.loot), ", ".join(self.supplies)]))]
        if items[0]:
            print('-----------------------------------------------------------------------------')
            dmCompact(f'On the ground: {items[0]}')


class Door(Place):
    def __init__(self,
                 icon,
                 inshort,
                 lock):
        self.icon = icon
        self.inshort = inshort
        self.lock = lock

    def __call__(self):
        # yo.inventory
        if self.lock < 1:
            enterDoor()
        else:
            if 'key' not in yo.inventory:
                dmCompact(f'The {self.inshort} is locked.')
                goBack()
            else:
                self.lock = 0
                dmCompact(f'{self.inshort} unlocked. Key consumed.')
                yo.inventory.remove('key')
                enterDoor()


class Portal(Place):
    def __init__(self,
                 icon,
                 portalTo,
                 inshort):
        super().__init__(icon, inshort)
        self.icon = icon
        self.portalTo = portalTo
    def __call__(self):
        teleport(self.portalTo)


# A Setting loads a scenario, and then teleports you to a location. NPCs can't enter here.
class Setting(Portal):
    def __init__(self,
                 icon,
                 portalTo,
                 inshort,
                 probability,
                 event):
        super().__init__(icon, portalTo,
                         inshort)
        self.probability = probability
        self.event = event

    def __call__(self):
        if rollDice(self.probability) == 0:
            self.event()
            teleport(self.portalTo)


# =============================================================================
# A Scene is somewhere that acts like a normal spot, but when you enter there,
# it loads a scenario. At the end of the scenario, you will be in the same place.
# I added the probability there, because I want to at some point add in some
# random events. To add a random event to a spot, all I have to change is the class,
# and add a probability and event.
# =============================================================================
class Scene(Spot):
    def __init__(self, icon, inshort, description, loot, supplies, npc, probability, event):
        super().__init__(icon, inshort, description, loot, supplies, npc)
        self.probability = probability
        self.event = event

    def __call__(self):
        print('=============================================================================')
        if yo.coordinates not in yo.visited:
            self.describe()
        else:
            self.describe()
        self.npcScenario()
        self.startEvent()

    def startEvent(self):
        if rollDice(self.probability) == 0:
            self.event()


# All NPCs are characters.
class Character:
    def __init__(self,
                 currentLocation,
                 home,
                 name,
                 level,
                 hitpoints,
                 gender,
                 description,
                 wanderlust,
                 possesions,
                 story):
        self.currentLocation = currentLocation
        self.home = home
        self.name = name
        self.level = level
        self.hitpoints = hitpoints
        self.gender = gender
        self.description = description
        self.wanderlust = wanderlust
        self.possesions = possesions
        self.story = story


# An enemy attacks you whenever it sees you, and as you get stronger, they do to.
class Enemy(Character):
    def __init__(self, currentLocation, home, name, level, hitpoints, gender, description, wanderlust, possesions, story):
        super().__init__(currentLocation, home, name, level, hitpoints, gender, description, wanderlust, possesions, story)

    def __call__(self):
        if self.level < yo.strength:
            self.level = yo.strength - 1

        self.encounterMessage()
        self.fightEnemy()

    def fightEnemy(self):
        global locations
        lair = locations.get(self.home)
        place = locations.get(yo.coordinates)
        outcome = performCombat(self.name, self.hitpoints, self.level)
        if outcome:
            self.currentLocation = self.home
            self.hitpoints = self.level ** 2
            if self in place.npc:
                place.npc.remove(self)
            lair.npc.append(self)
            dmSlow(f'You killed {self.name}.')
            place.loot.append(self.possesions)
            kill()
        else:
            self.defeatMessage()
            place.loot.append('human skull')
            die()

    def encounterMessage(self):
        dm(f'You encounter {self.name}.')

    def defeatMessage(self):
        dm(f'{self.name} killed you.')


class Bear(Enemy):
    def __init__(self,
                currentLocation,
                home,
                name,
                level,
                hitpoints,
                gender,
                description,
                wanderlust,
                possesions,
                story):
        super().__init__(currentLocation,
                home,
                name,
                level,
                hitpoints,
                gender,
                description,
                wanderlust,
                possesions,
                story)

    def defeatMessage(self):
        dm(f'{self.name} mauled you to death.')


class Worm(Enemy):
    def __init__(self,
                currentLocation,
                home,
                name,
                level,
                hitpoints,
                gender,
                description,
                wanderlust,
                possesions,
                story):
        super().__init__(currentLocation,
                home,
                name,
                level,
                hitpoints,
                gender,
                description,
                wanderlust,
                possesions,
                story)

    def encounterMessage(self):
        dm(f'The {self.name} throws itself at you.')

    def defeatMessage(self):
        dm(f'The {self.name} slithered down your throat and suffocated you.\
           It will probably lay eggs in you to raise more worms.')


class Trader(Character):
    def __init__(self,
                currentLocation,
                home,
                name,
                level,
                hitpoints,
                gender,
                description,
                wanderlust,
                possesions,
                story,
                supplies):
        super().__init__(currentLocation,
                home,
                name,
                level,
                hitpoints,
                gender,
                description,
                wanderlust,
                possesions,
                story)
        self.supplies = supplies

    def __call__(self):
        if self.name not in yo.visited:
            dm(f'{self.name}: "Hiya stranger! My name\'s {self.name}. Are you looking to trade?"')
            yo.visited.append(self.name)
        else:
            dm(f'{self.name}: "{yo.avatarName}! Good to see you again! Anything you want to trade?"')

        choice = makeChoice(['Yes',
                             'No'])

        if choice == 0:
            self.trade()
        else:
            dm(f'{self.name}: "Well, maybe next time then."')

    def trade(self):
        wares = ", ".join(self.possesions)
        foodwares = ", ".join(self.supplies)

        dm(f'{self.name}: "Great! I\'ve got: |{wares}|. And if you\'re hungry: |{foodwares}|. Fancy any of it?"')

        checkInventory()

        choice = makeChoice(['Buy',
                             'Sell',
                             'Swap'])

        if choice == 0:
            if yo.coin > 0:
                item = input('What to buy? ')
                if item in self.possesions:
                    self.possesions.remove(item)
                    yo.inventory.append(item)
                    yo.coin -= 1
                    dm(f'{self.name}: "The {item}? Great choice. It\'s yours!"')
                elif item in self.supplies:
                    self.supplies.remove(item)
                    yo.food.append(item)
                    yo.coin -= 1
                    dm(f'{self.name}: "You can\'t go wrong eating some {item}!"')
                else:
                    dm(f'{self.name}: "{item}? Never heard of it."')
            else:
                dmCompact('You\'re broke!')

        elif choice == 1:
            item = input('What to sell? ')
            if item in yo.inventory:
                yo.inventory.remove(item)
                self.possesions.append(item)
                yo.coin += 1
                dm(f'{self.name}: "The {item}? I\'ll gladly take it off your hands."')
            elif item in yo.food:
                yo.food.remove(item)
                self.supplies.append(item)
                yo.coin += 1
                dm(f'{self.name}: "The {item}? I could do with a snack. I\'ll gladly take it off your hands."')
            else:
                dmCompact('That\'s not in your possesion.')
        else:
            item = input('What to trade? ')

            if item in yo.food:
                yo.food.remove(item)
                self.supplies.append(item)
                dm(f'{self.name}: "Aah! The {item}!"')
                ware = input('For what? ')
                if ware in self.possesions or self.supplies:
                    dm(f'{self.name}: "The {item} for the {ware}? A wise decision."')
                    if ware in self.possesions:
                        self.possesions.remove(ware)
                        yo.inventory.append(ware)
                    elif ware in self.supplies:
                        self.supplies.remove(ware)
                        yo.food.append(ware)
                else:
                    dm(f'{self.name}: "I\'m afraid I don\'t have that."')

            elif item in yo.inventory:
                yo.inventory.remove(item)
                self.possesions.append(item)
                dm(f'{self.name}: "Aah! Your {item}!"')
                ware = input('For what? ')
                if ware in self.possesions or self.supplies:
                    dm(f'{self.name}: "The {item} for the {ware}? A wise decision."')
                    if ware in self.possesions:
                        self.possesions.remove(ware)
                        yo.inventory.append(ware)
                    elif ware in self.supplies:
                        self.supplies.remove(ware)
                        yo.food.append(ware)
                else:
                    dm(f'{self.name}: "I\'m afraid I don\'t have that."')

            else:
                dmCompact(f"You don't have {item}.")

        self.askContinueTrading()

    def askContinueTrading(self):
        choice = makeChoice([f'Browse {self.name}\'s wares',
                              f'Leave {self.name} alone'])
        if choice == 0:
            self.trade()
        else:
            dm(f'{self.name}: "All the best!"')


# I have yet to implement this. At the moment I just do the old 'if {item} in yo.inventory' thing.
class Object:
    def __init__(self, name, description):
        self.name = name
        self.description = description


# The original plan was to be able to increase yo.inventory size, but at the moment, I quite like having infinite yo.inventory. Also the enemies are pretty strong.
class Storage(Object):
    def __init__(self, name, description, contents):
        super().__init__(name, description)
        self.contents = contents


# Yes, one day I will make it so that weapons will increase damage.
class Weapon(Object):
    def __init__(self, name, description, power):
        super().__init__(name, description)
        self.power = power


#%%Saving and loading

def saveGame():
    global locations, characters

    gameState = {
        'yo.coin': yo.coin,
        'locations': locations,
        'characters': characters,
        'yo.deaths': yo.deaths,
        'yo.chapterDeaths': yo.chapterDeaths,
        'yo.kills': yo.kills,
        'yo.strength': yo.strength,
        'yo.chapter': yo.chapter,
        'yo.playerHP': yo.playerHP,
        'yo.inventory': yo.inventory,
        'yo.playerName': yo.playerName,
        'yo.visited': yo.visited,
        'yo.avatarName': yo.avatarName,
        'yo.bearing': yo.bearing,
        'yo.coordinates': yo.coordinates,
        'yo.respawnPoint': yo.respawnPoint
    }

    saveDirectory = os.path.join(Path.home(), 'DoctopusTextAdventureSavesModule')
    os.makedirs(saveDirectory, exist_ok=True)

    savePath = os.path.join(saveDirectory, 'DoctopusSaveModule.pkl')

    with open(savePath, 'wb') as file:
        pickle.dump(gameState, file)
    print(f"Game saved at: {savePath}")


def loadGame():
    global locations, characters

    saveDirectory = os.path.join(Path.home(), 'DoctopusTextAdventureSavesModule')
    savePath = os.path.join(saveDirectory, 'DoctopusSaveModule.pkl')

    try:
        with open(savePath, 'rb') as file:
            gameState = pickle.load(file)

        yo.coin = gameState['yo.coin']
        locations = gameState['locations']
        characters = gameState['characters']
        yo.deaths = gameState['yo.deaths']
        yo.chapterDeaths = gameState['yo.chapterDeaths']
        yo.kills = gameState['yo.kills']
        yo.strength = gameState['yo.strength']
        yo.chapter = gameState['yo.chapter']
        yo.playerHP = gameState['yo.playerHP']
        yo.inventory = gameState['yo.inventory']
        yo.playerName = gameState['yo.playerName']
        yo.visited = gameState['yo.visited']
        yo.avatarName = gameState['yo.avatarName']
        yo.bearing = gameState['yo.bearing']
        yo.coordinates = gameState['yo.coordinates']
        yo.respawnPoint = gameState['yo.respawnPoint']

        print(f"Game loaded from: {savePath}")

        visitPlace(yo.respawnPoint)
        processUserInput()

    except FileNotFoundError:
        print("No saved game found. Start a new game.")
        start()
    except Exception as e:
        print(f"Error loading game: {e}. Start a new game.")
        raise e

#%%Basic game functions


def randomVector(directions):
    chance = rollDice(directions-1)     # to make the first one zero.
    vector = (0,0,0)
    if chance == 0:
        vector = (0,1,0)
    elif chance == 1:
        vector = (1,0,0)
    elif chance == 2:
        vector = (0,-1,0)
    elif chance == 3:
        vector = (-1,0,0)
    elif chance == 4:                   # this means that I can stop NPCs going up and down if needed. could be useful for later.
        vector = (0,0,-1)
    elif chance == 5:
        vector = (0,0,1)
    else:
        vector = vector
    return vector


# This function was a real pain in the butt to get working properly, but I think I've got it working.
def wander():
    for character in characters.copy():
        lair = locations.get(character.home)
        lastCharacterPlace = character.currentLocation
        place = locations.get(character.currentLocation)

        if character not in place.npc:
            place.npc.append(character)

        if yo.tick / character.wanderlust < 1: # This is my way of making sure the characters don't wander too far.
            direction = randomVector(6)
            tried_location = (
                character.currentLocation[0] + direction[0],
                character.currentLocation[1] + direction[1],
                character.currentLocation[2] + direction[2]
            )
            new_place = locations.get(tried_location)

            if new_place is not None and hasattr(new_place, 'npc'):
                if character in place.npc:
                    place.npc.remove(character)
                new_place.npc.append(character)
                character.currentLocation = tried_location
                # print(f'{character.name} has wandered. {character.currentLocation}')
            else:
                character.currentLocation = lastCharacterPlace
                # print(f'{character.name} has bumped into a wall. {character.currentLocation}')
        else:
            if character in place.npc:
                place.npc.remove(character)
            lair.npc.append(character)
            character.currentLocation = character.home
            # print(f'{character.name} has gone home. {character.currentLocation}')

        # print(f'{character.name} acted')


def start():
    yo.coordinates = (0,0,9)

    if 'map' in yo.inventory:
        yo.inventory.remove('map')
    if 'compass' in yo.inventory:
        yo.inventory.remove('compass')

    dmSlow('To make a choice, type a number.')
    choices = ['Start a new game', 'Load a saved game', 'Instructions']
    choice = forceChoice(choices)

    if choice == 0:
        yo.playerName = input('Type your name: ')
        yo.avatarName = yo.playerName
        dmSlow(f'Welcome, {yo.playerName}. If no choice presents itself, type simple instructions.')
        wander()
        visitPlace(yo.coordinates)
        processUserInput()
    elif choice == 1:
        loadGame()
    else:
        showInstructions()
        start()


def teleport(portalTo):
    yo.lastPlace = yo.coordinates
    yo.coordinates = (portalTo[0],
                   portalTo[1],
                   portalTo[2])
    visitPlace(yo.coordinates)


# =============================================================================
# def checkDirection(direction):
#     if 'compass' in yo.inventory:
#         if any(x in direction for x in ['a']):
#             goDirection('west')
#         elif any(x in direction for x in ['w']):
#             goDirection('north')
#         elif any(x in direction for x in ['d']):
#             goDirection('east')
#         elif any(x in direction for x in ['s']):
#             goDirection('south')
#         else:
#             goDirection(direction)
#     else:
#         goDirection(direction)
# =============================================================================


def goDirection(direction):
    yo.tick += 1

    wander()

    yo.lastPlace = yo.coordinates
    i, j, k = yo.bearing

    if any(x in direction for x in ['left', 'a']):
        new_i = -j
        new_j = i
        yo.bearing = (new_i, new_j, 0)
        yo.coordinates = (yo.coordinates[0] + yo.bearing[0],
                       yo.coordinates[1] + yo.bearing[1],
                       yo.coordinates[2])
        visitPlace(yo.coordinates)

    elif any(x in direction for x in ['right', 'd']):
        new_i = j
        new_j = -i
        yo.bearing = (new_i, new_j, 0)
        yo.coordinates = (yo.coordinates[0] + yo.bearing[0],
                       yo.coordinates[1] + yo.bearing[1],
                       yo.coordinates[2])
        visitPlace(yo.coordinates)

    elif any(x in direction for x in ['back', 'behind', 's']):
        new_i = -i
        new_j = -j
        yo.bearing = (new_i, new_j, 0)
        yo.coordinates = (yo.coordinates[0] + yo.bearing[0],
                       yo.coordinates[1] + yo.bearing[1],
                       yo.coordinates[2])
        visitPlace(yo.coordinates)

    elif any(x in direction for x in ['ahead', 'straight','w']):
        new_i = i
        new_j = j
        yo.bearing = (new_i, new_j, 0)
        yo.coordinates = (yo.coordinates[0] + yo.bearing[0],
                       yo.coordinates[1] + yo.bearing[1],
                       yo.coordinates[2])
        visitPlace(yo.coordinates)

    elif any(x in direction for x in ['up', 'above', 'climb', 'z']):
        yo.coordinates = (yo.coordinates[0],
                       yo.coordinates[1],
                       yo.coordinates[2] + 1)
        visitPlace(yo.coordinates)

    elif any(x in direction for x in ['down','below','x']):
        yo.coordinates = (yo.coordinates[0],
                       yo.coordinates[1],
                       yo.coordinates[2] - 1)
        visitPlace(yo.coordinates)

    elif any(x in direction for x in ['north', 'south', 'east', 'west','i','j','k','l']):
        if 'compass' in yo.inventory:
            if any(x in direction for x in ['north', 'i']):
                yo.bearing = (0, 1, 0)
            elif any(x in direction for x in ['south', 'k']):
                yo.bearing = (0, -1, 0)
            elif any(x in direction for x in ['east', 'l']):
                yo.bearing = (1, 0, 0)
            elif any(x in direction for x in ['west', 'j']):
                yo.bearing = (-1, 0, 0)
            else:
                print("I don\'t know that direction.")
                return yo.bearing

            yo.coordinates = (yo.coordinates[0] + yo.bearing[0],
                           yo.coordinates[1] + yo.bearing[1],
                           yo.coordinates[2])
            visitPlace(yo.coordinates)
        else:
            dmCompact("If only there was some kind of device to tell you what direction that is.")
            return yo.bearing
    else:
        print("I don\'t know that direction.")

    if yo.tick < 99:
        return
    else:
        yo.playerHP = 0
        dmSlow(f'Health: {yo.playerHP}. You are hungry.')


def checkIfFood(item):
    if item in yo.food and yo.inventory:
        return 'food'
    elif item in yo.inventory and not yo.food:
        return 'notFood'
    else:
        return None


def turn(direction):
    yo.lastPlace = yo.coordinates
    i, j, k = yo.bearing

    if any(x in direction for x in ['left', 'a']):
        new_i = -j
        new_j = i
        yo.bearing = (new_i, new_j, 0)
        dmCompact('You turned left')
        describeSurroundings()

    elif any(x in direction for x in ['right', 'd']):
        new_i = j
        new_j = -i
        yo.bearing = (new_i, new_j, 0)
        dmCompact('You turned right')
        describeSurroundings()


    elif any(x in direction for x in ['back', 'behind', 's', 'around']):
        new_i = -i
        new_j = -j
        yo.bearing = (new_i, new_j, 0)
        dmCompact('You turned around')
        describeSurroundings()


    elif any(x in direction for x in ['ahead', 'straight','w']):
        new_i = i
        new_j = j
        yo.bearing = (new_i, new_j, 0)

    elif any(x in direction for x in ['north', 'south', 'east', 'west','i','j','k','l']):
        if 'compass' in yo.inventory:
            if any(x in direction for x in ['north', 'i']):
                yo.bearing = (0, 1, 0)
                takeBearing()
                describeSurroundings()
            elif any(x in direction for x in ['south', 'k']):
                yo.bearing = (0, -1, 0)
                takeBearing()
                describeSurroundings()
            elif any(x in direction for x in ['east', 'l']):
                yo.bearing = (1, 0, 0)
                takeBearing()
                describeSurroundings()
            elif any(x in direction for x in ['west', 'j']):
                yo.bearing = (-1, 0, 0)
                takeBearing()
                describeSurroundings()
            else:
                print("I don\'t know that direction.")
                return yo.bearing
        else:
            dmCompact("If only there was some kind of device to tell you what direction that is.")
    else:
        turnExplicit()


def enterDoor():
    yo.coordinates = (yo.coordinates[0] + yo.bearing[0],
                   yo.coordinates[1] + yo.bearing[1],
                   yo.coordinates[2])
    visitPlace(yo.coordinates)


# Once I set up the open world, I will need this. The idea is I can use the goBack()  function to lock the player to an area.
def goBack():
    dmCompact("You can't go there.")
    yo.coordinates = yo.lastPlace
    describeSurroundings()


def takeBearing():
    if 'compass' in yo.inventory:
        if yo.bearing == (0,1,0):
            dmCompact('You are facing North.')
        elif yo.bearing == (0,-1,0):
            dmCompact('You are facing South.')
        elif yo.bearing == (1,0,0):
            dmCompact('You are facing East.')
        elif yo.bearing == (-1,0,0):
            dmCompact('You are facing West.')
        else:
            dmCompact('Your compass doesn\'t seem to working.')
    else:
        dmCompact('If only there was some kind of device for knowing what direction you are facing.')


def checkStats():
    dm(f'    Name: {yo.playerName}')
    dmCompact(f'   Kills: {yo.kills}')
    dmCompact(f'  Deaths: {yo.deaths}')
    dmCompact(f'Strength: {yo.strength}')
    dmCompact(f'  Health: {yo.playerHP}')
    if len(yo.inventory) > 0:
        checkInventory()


#Below is how I want the dm functions to be, but I think it's uneccesary to do it all the time when I am developing.
def dm(text, width=70, leftMargin=4, charsPerPrint=4):
    wrappedText = textwrap.fill(text, width)
    print()
    for line in wrappedText.splitlines():
        print(" " * leftMargin, end='')
        for i in range(0, len(line), charsPerPrint):
            chunk = line[i:i + charsPerPrint]
            print(chunk, end='', flush=True)
            time.sleep(0.01)
        print()


def dmSlow(text, width=70, leftMargin=4, charsPerPrint=3):
    wrappedText = textwrap.fill(text, width)
    print()
    for line in wrappedText.splitlines():
        print(" " * leftMargin, end='')
        for i in range(0, len(line), charsPerPrint):
            chunk = line[i:i + charsPerPrint]
            print(chunk, end='', flush=True)
            time.sleep(0.1)
        print()


def dmCompact(text, width=70, leftMargin=4, charsPerPrint=4):
    wrappedText = textwrap.fill(text, width)
    for line in wrappedText.splitlines():
        print(" " * leftMargin, end='')
        for i in range(0, len(line), charsPerPrint):
            chunk = line[i:i + charsPerPrint]
            print(chunk, end='', flush=True)
            time.sleep(0.01)
        print()


# I like the stuff above, but just for now I want to be able to speedrun:
'''
def dm(text, width=70, leftMargin=4, charsPerPrint=4):
    wrappedText = textwrap.fill(text, width)
    print()
    for line in wrappedText.splitlines():
        print(" " * leftMargin, end='')
        print(line)
    time.sleep(0.01)


def dmSlow(text, width=70, leftMargin=4, charsPerPrint=2):
    wrappedText = textwrap.fill(text, width)
    print()
    for line in wrappedText.splitlines():
        print(" " * leftMargin, end='')
        print(line)
    time.sleep(0.1)


def dmCompact(text, width=70, leftMargin=4):
    wrappedText = textwrap.fill(text, width)
    for line in wrappedText.splitlines():
        print(" " * leftMargin, end='')
        print(line)
    time.sleep(0.01)
'''


def makeChoice(choices):
    print()
    for i, choice in enumerate(choices, start=1):
        dmCompact(f'{i}. {choice}')
    print()

    while True:
        try:
            userInput = input(' >> ').lower()

            if userInput.isdigit():
                choice = int(userInput)
                if 1 <= choice <= len(choices):
                    return choice - 1
                else:
                    dmCompact('Invalid choice.')
            else:
                checkIfCommand(userInput)
        except ValueError:
            dmCompact('Invalid input. Enter a number or command.')


def forceChoice(choices):
    print()
    for i, choice in enumerate(choices, start=1):
        dmCompact(f'{i}. {choice}')
    print()

    while True:
        try:
            userInput = input('  > ').lower()
            choice = int(userInput)
            if 1 <= choice <= len(choices):
                return choice - 1
            else:
                dmCompact('Invalid choice.')
        except ValueError:
            dmCompact('Invalid input. Enter a number.')


def processUserInput():
    while True:
        userInput = input('>>> ').lower()
        checkIfCommand(userInput)


def checkIfCommand(text):
    global locations
    command = text.split()

    if any(word in command for word in ['exit']):
        endgame()
    elif any(word in command for word in ['save']):
        saveGame()
    elif any(word in command for word in ['die', 'suicide']):
        suicideMessages()
    elif any(word in command for word in ['inventory',
                                          'pockets',
                                          'got?', 'inventory',
                                          'inventory?', 'e']):
        checkInventory()
    elif any(word in command for word in ['health', 'stats',
                                          'who', 'name',
                                          'kills', 'deaths',
                                          'strength', 'info',
                                          'information', 'c']):
        checkStats()
    elif any(word in command for word in ['eat', 'hungry', 'food']):
        commandEat(command)
    elif any(word in command for word in ['vomit', 'sick']):
        sick()
    elif any(word in command for word in ['drop', 'q']):
        commandDrop(command)
    elif any(word in command for word in ['take', 'get','grab', 'g']):
        take(command)
    elif any(word in command for word in ['look', 'examine', 'f']):
        lookAround(yo.coordinates)
    elif any(word in command for word in ['help', 'hint', 'hints']):
        showInstructions()
    elif any(word in command for word in ['direction', 'bearing', 'compass', 'h']):
        takeBearing()
    elif any(word in command for word in ['scope', 'telescope','t']):
        useTelescope()
    elif any(word in command for word in ['turn', 'face', 'rotate', 'spin', 'r']):
        turn(command)
    elif any(word in command for word in ['left', 'right', 'back', 'behind',
                                          'ahead', 'straight', 'north', 'south',
                                          'east', 'west','down', 'up', 'climb', 'below',
                                          'above', 'w','a','s','d','i','j','k','l','z','x']):
        goDirection(command)
    elif any(word in command for word in ['load', 'restore']):
        loadGame()
    elif any(word in command for word in ['characters', 'npc', 'npcs']):
        whereNPC()
    elif any(word in command for word in ['map','m']):
        generateMap(yo.coordinates)
    elif any(word in command for word in ['fuck','shit','tits','cunt','arse','rape','sex','boobies','boobs','penis','vagina']):
        dm(randomEvent(['Saying bad words? Have some sickness.','Language! You will be punished.','We don\'t allow that kind of language here. Bad health to you.','Don\'t talk of such things. You now have plague.']))
        sick()
    else:
        dmCompact('I don\'t understand that.')


def turnExplicit():
    face = input('Which direction? ').lower()
    turn(face.split())


def lookAround(location):
    place = locations.get(location)

    if place is not None:
        place.describeLong()

    if 'telescope' in yo.inventory:
        ahead = lookFarAhead()
        dmCompact(f'Scope: {ahead}')

def useTelescope():
    initialBearing = yo.bearing

    scopeDirection = input('Use telescope in which direction? ')
    turn(scopeDirection)

    whatYouSee = lookFarAhead()

    if 'telescope' in yo.inventory:
        dmCompact(f'You see: {whatYouSee}')
    else:
        dmCompact("You don't have a telescope.")

    yo.bearing = initialBearing


def showInstructions():
    choice = makeChoice(['How to play the game',
                         'Commands',
                         'Keyboard shortcuts'])

    if choice == 0:
        dm('BASIC COMMANDS: To interact with the world, type simple instructions. For instance "turn around" will turn you around, "go left" will move you left, "take/get apple" will take an apple (if there is an apple present.), "use map" will open the map. "drop all" will drop all of your inventory.')
        dm('If in doubt, type something that seems like it will make sense.')
        input('Press Enter for another tip.')
        dm("DEAD ENDS: You can't see behind you, so if you see no description of any nearby locations, try the command 'turn around.' This will turn you around on the spot.")
        input('Press Enter for another tip.')
        dm('BE SPECIFIC: Keep in mind that the game only checks for keywords in your input, so sometimes it will ask you to specify something. When the game asks you for a specification, such as "What would you like to eat?" make sure reply with the item spelt exactly how it is spelt in your inventory. To view your inventory, type the word "inventory"')
        input('Press Enter for another tip.')
        dm('FINDING YOUR WAY: There are three items that will help you find your way: the compass, the map, and the telescope. If you have a compass, you will be able to check your yo.bearing and explicitly tell the game what direction you want to go in terms of north, south, east, and west. If you have a map, you will be able to use the command "map" to see a map of your surroundings. If you have a map AND a compass, the yo.coordinates of your current location will appear to the bottom right of the description; additionally, the icon showing the player\'s location on the map will appear as an arrow pointing in the direction that you are facing. If you have a telescope, you will be able to use the "telescope" or "scope" command to look at the three tiles beyond adjacent tiles.')
        input('Press Enter for another tip.')
        dm('HINT: The arrows next to where you type tell you whether you have an unresolved choice waiting to be decided. If there is only one arrow, that means you can only input numbers. If there are two arrows, it means there is an unresolved choice, but you may input either numbers or commands. If there are three arrows, you can only input commands.')
    elif choice == 1:
        dm("COMMANDS RECOGNISED: 'exit', | 'save', | 'die', 'suicide', | 'inventory', 'pockets', 'got?', 'inventory', 'inventory?', | 'health', 'stats', 'who', 'name', 'kills', 'deaths', 'strength', 'info', 'information', | 'eat', 'hungry', 'food', | 'vomit', 'sick', | 'drop', | 'look', 'examine', | 'help', 'hint', 'hints',| 'direction', 'bearing', 'compass', | 'left', 'right', 'back', 'behind', 'ahead', 'straight', 'north', 'south', 'east', 'west','down', 'up', 'below', 'above', | 'take', 'get', 'grab', | 'load', 'restore',| 'scope', 'telescope', | 'turn', 'face', 'rotate', 'spin', | 'map'")
    else:
        dm("KEYBOARD SHORTCUTS:")
        dmCompact('w - go straight ahead')
        dmCompact('a - go left')
        dmCompact('s - go right')
        dmCompact('d - step back')
        dmCompact('z - go up')
        dmCompact('x - go down')
        dmCompact('e - check inventory')
        dmCompact('f - look around')
        dmCompact('t - use telescope to see the three tiles beyond a direction.')
        dmCompact('g - take item -- to get everything, when prompted type "all" or just "g" again.')
        dmCompact('q - drop item -- to drop everything, when prompted, type "all" or just "q" again.')
        dmCompact('r - rotate on the spot -- when prompted use direction shortcuts or commands.')

        dm('DIRECTIONS (REQUIRES COMPASS):')
        dmCompact('h - check yo.bearing (tells you what direction you are facing)')
        dmCompact('i - go North')
        dmCompact('k - go South')
        dmCompact('l - go East')
        dmCompact('j - go west')

        dm('MAP (REQUIRES MAP):')
        dmCompact('m - opens the map')


def sick():
    yo.playerHP = 0
    dmCompact('You feel unwell.')


def checkInventory():
    if len(yo.inventory) or len(yo.food) > 0:
        inven = ", ".join(yo.inventory)
        fuud = ", ".join(yo.food)
        dm(f'You have: |{inven}| |{fuud}|')
    else:
        print()
    dmCompact(f'Your coin: {yo.coin}')


def performCombat(enemyName, enemyHP, level):
    while yo.playerHP > 0 and enemyHP > 0:
        dm(f'{yo.playerName}: {yo.playerHP} | {enemyName}: {enemyHP}')
        print()
        print(input('  > '))

        playerRoll = rollDice(yo.strength)
        enemyRoll = rollDice(level)

        if playerRoll >= enemyRoll:
            damage = rollDice(yo.strength ** 2)
            print(f'    You deal {damage} damage!')
            enemyHP -= damage
        else:
            damage = rollDice(level ** 2)
            print(f'    {enemyName} deals {damage} damage!')
            yo.playerHP -= damage

    return yo.playerHP > 0


def suicideMessages():
    messages = ['Why would you do that?',
                'That\'s not a very effective way to win a game!',
                'FOOL!', 'That\'s not very nice.', 'Why?']
    dmCompact('Are you sure you want to die?')
    choice = forceChoice(['Yes, I am weary of living','No, that was a mistake'])
    if choice == 0:
        randomMessage = randomEvent(messages)
        dm(randomMessage)
        die()


def die():
    dropAll()

    time.sleep(3)

    messages = ['You hear the distant tolling of a bell.',
                'Somewhere in the distance, you hear a dog bark.',
                'You feel a falling sensation as everything goes dark',
                'Death comes like a theif in the night.',
                'You knew from the moment you fell into the abyss, that death had overtaken you.',
                'The unpleasant chill of death spreads across your body.',
                'You fall to the ground, the life leaking out of you rapidly like water.',
                'Death took you away, it was almost clinical.',
                'As you slip into the cold waters of death, you feel its cold hands grip you.',
                'Death, as they say, comes to us all, but to some more than others.',
                'You die.', 'You die a horrific and painful death.',
                'You cease to be alive, and are dead.','You shuffle from the mortal coil.',
                'Like an unhappy bubble of anal wind in the mortal bath, you rise to the surface and pop out of life.',
                'Your life force snaps like a rope under great tension, and your body falls to the ground.']
    randomMessage = randomEvent(messages)
    dmSlow(randomMessage)

    yo.deaths += 1
    yo.chapterDeaths += 1
    checkStats()
    yo.tick = 0
    yo.playerHP = yo.strength ** 2
    saveGame()

    time.sleep(1)
    dmSlow(' . . . ')
    print()
    time.sleep(3)
    wander()
    wander()
    wander()

    teleport(yo.lastPlace)


def kill():
    messages = ['You are victorious!']
    randomMessage = randomEvent(messages)
    dmSlow(randomMessage)
    yo.kills += 1
    if yo.strength < 10:
        yo.strength += 1
    checkStats()


def rollDice(sides):
    return random.randint(0, sides)


def randomEvent(events):
    return random.choice(events)


def take(text):
    place = locations.get(yo.coordinates)

    commonSupplies = findCommonWord(text, place.supplies)
    commonLoot = findCommonWord(text, place.loot)

    if commonSupplies:
        place.takeLoot(commonSupplies)
        dmCompact(f'{commonSupplies} taken.')
    elif commonLoot:
        place.takeLoot(commonLoot)
        dmCompact(f'{commonLoot} taken.')
    else:
        takeItem(text)


def takeExplicit():
    global locations
    place = locations.get(yo.coordinates)
    item = input('What would you like to take? ').lower()

    items_to_take = item.split()

    if any(item in place.supplies or item in place.loot for item in items_to_take):
        takeItem(items_to_take)
    elif any(word in ['all', 'everything', 'the lot', 'g'] for word in items_to_take):
        takeItem('all')
    else:
        dmCompact('That isn\'t here.')


def takeItem(item):
    place = locations.get(yo.coordinates)
    if not place.loot and not place.supplies:
        dmCompact('There\'s nothing here to take.')
    else:
        if any(word in item for word in ['all', 'everything', 'the lot']):
            for x in place.loot.copy():
                place.takeLoot(x)
                dmCompact(f'{x} taken.')
            for x in place.supplies.copy():
                place.takeLoot(x)
                dmCompact(f'{x} taken.')
        else:
            if item in place.loot:
                place.takeLoot(item)
                dmCompact(f'{item} added to inventory.')

            elif item in place.supplies:
                place.takeLoot(item)
                dmCompact(f'{item} added to inventory.')
            else:
                takeExplicit()


def commandEat(text):
    common_word = findCommonWord(text, yo.food)
    if common_word:
        eat(common_word)
    else:
        commandEatExplicit()


def findCommonWord(text, wordList):
    for x in wordList:
        if x in text:
            return x
    return None


def commandEatExplicit():
    edible = input('What would you like to eat? ').lower()
    if edible in yo.food:
        eat(edible)
    elif edible in yo.inventory:
        dmCompact("That's not edible!")
    else:
        dmCompact("That's not in your inventory!")


def eat(edible):
    if edible in yo.food:
        if yo.playerHP < yo.strength ** 2:
            yo.food.remove(edible)
            yo.playerHP = yo.strength ** 2
            dmCompact(f'You eat the {edible} and feel satisfied.')
            yo.tick = 0
        else:
            dmCompact("You are at full health and don't feel hungry.")

    elif edible not in yo.food:
        dmCompact("You don't have any yo.food.")


def dropAll():
    global locations
    place = locations.get(yo.coordinates)
    for x in yo.inventory.copy():
        place.dropLoot(x)
        dmCompact(f'{x} dropped.')
    for x in yo.food.copy():
        place.dropLoot(x)
        dmCompact(f'{x} dropped.')
    dm('There\'s nothing left in your inventory')


def commandDrop(text):
    place = locations.get(yo.coordinates)
    if not yo.inventory and not yo.food:
        dmCompact('There\'s nothing in your inventory.')
    else:
        commonFood = findCommonWord(text, yo.food)
        commonInventory = findCommonWord(text, yo.inventory)

        if commonFood:
            place.dropLoot(commonFood)
            dmCompact(f'{commonFood} dropped.')
        elif commonInventory:
            place.dropLoot(commonInventory)
            dmCompact(f'{commonInventory} dropped.')
        elif any(word in text for word in ['all',
                        'everything',
                        'the lot']):
            dropAll()
        else:
            dropExplicit()


def dropExplicit():
    place = locations.get(yo.coordinates)
    drops = input('What would you like to drop? ').lower()
    dropping = drops.split()

    if any(item in yo.inventory or item in yo.food for item in dropping):
        place.dropLoot(dropping)
    elif any(word in dropping for word in ['q', 'all', 'everything', 'the lot']):
        dropAll()
    else:
        dmCompact("That's not in your inventory!")


def wait(seconds):
    time.sleep(seconds)


def lookFarAhead():
    global locations

    #aheadL = (coordinates[0]+(bearing[0]), yo.coordinates[1]+(bearing[1]), yo.coordinates[2]+(bearing[2]))
    furtherL = (yo.coordinates[0]+(2*yo.bearing[0]), yo.coordinates[1]+(2*yo.bearing[1]), yo.coordinates[2]+(2*yo.bearing[2]))
    distantL = (yo.coordinates[0]+(3*yo.bearing[0]), yo.coordinates[1]+(3*yo.bearing[1]), yo.coordinates[2]+(3*yo.bearing[2]))
    yonksAwayL = (yo.coordinates[0]+(4*yo.bearing[0]), yo.coordinates[1]+(4*yo.bearing[1]), yo.coordinates[2]+(4*yo.bearing[2]))

    #ahead = locations.get(aheadL)
    further = locations.get(furtherL)
    distant = locations.get(distantL)
    yonksAway = locations.get(yonksAwayL)

    #inAhead = ahead.inshort if ahead and hasattr(ahead, 'inshort') else None
    inFurther = further.inshort if further and hasattr(further, 'inshort') else None
    inDistance = distant.inshort if distant and hasattr(distant, 'inshort') else None
    yonks = yonksAway.inshort if yonksAway and hasattr(yonksAway, 'inshort') else None

    if 'telescope' in yo.inventory:
        locations_str = ", ".join(location for location in [inFurther, inDistance, yonks] if location is not None)
        return locations_str
    else:
        return None


def generateAdjacentLocations():
    global locations

    placeNorth = locations.get((yo.coordinates[0], yo.coordinates[1] + 1, yo.coordinates[2]))
    placeSouth = locations.get((yo.coordinates[0], yo.coordinates[1] - 1, yo.coordinates[2]))
    placeEast = locations.get((yo.coordinates[0] + 1, yo.coordinates[1], yo.coordinates[2]))
    placeWest = locations.get((yo.coordinates[0] - 1, yo.coordinates[1], yo.coordinates[2]))
    placeAbove = locations.get((yo.coordinates[0], yo.coordinates[1], yo.coordinates[2] + 1))
    placeBelow = locations.get((yo.coordinates[0], yo.coordinates[1], yo.coordinates[2] - 1))

    def get_npc_names(npc_list):
        return [npc.name if npc is not None else None for npc in npc_list]

    inNorth = placeNorth.inshort if placeNorth and hasattr(placeNorth, 'inshort') else None
    inSouth = placeSouth.inshort if placeSouth and hasattr(placeSouth, 'inshort') else None
    inEast = placeEast.inshort if placeEast and hasattr(placeEast, 'inshort') else None
    inWest = placeWest.inshort if placeWest and hasattr(placeWest, 'inshort') else None
    inAbove = placeAbove.inshort if placeAbove and hasattr(placeAbove, 'inshort') else None
    inBelow = placeBelow.inshort if placeBelow and hasattr(placeBelow, 'inshort') else None

    inNorthNPC = get_npc_names(placeNorth.npc) if hasattr(placeNorth, 'npc') else None
    inSouthNPC = get_npc_names(placeSouth.npc) if hasattr(placeSouth, 'npc') else None
    inEastNPC = get_npc_names(placeEast.npc) if hasattr(placeEast, 'npc') else None
    inWestNPC = get_npc_names(placeWest.npc) if hasattr(placeWest, 'npc') else None
    inAboveNPC = get_npc_names(placeAbove.npc) if hasattr(placeAbove, 'npc') else None
    inBelowNPC = get_npc_names(placeBelow.npc) if hasattr(placeBelow, 'npc') else None

    return inNorth, inSouth, inEast, inWest, inAbove, inBelow, inNorthNPC, inSouthNPC, inEastNPC, inWestNPC, inAboveNPC, inBelowNPC


def visitPlace(location):
    place = locations.get(yo.coordinates)
    if place is not None:
        place()
    else:
        goBack()


def visitFlatRock(title):
    dm(f'On the ground, you see a {title}.')
    choices = [f'Open {title}','Ignore']
    choice = forceChoice(choices)

    if choice == 0:
        dmCompact(f'You open the {title}.')
    else:
        goBack()


def describeSurroundings():
    global locations

    inNorth, inSouth, inEast, inWest, inAbove, inBelow, inNorthNPC, inSouthNPC, inEastNPC, inWestNPC, inAboveNPC, inBelowNPC = generateAdjacentLocations()

    # if 'compass' not in yo.inventory:
    direction_mapping = {
        (0, 1, 0): ("Ahead:", inNorth, inNorthNPC,
                    " Left:", inWest, inWestNPC,
                    "Right:", inEast, inEastNPC,
                    "Above:", inAbove, inAboveNPC,
                    "Below:", inBelow, inBelowNPC),
        (0, -1, 0): ("Ahead:", inSouth, inSouthNPC,
                     " Left: ", inEast, inEastNPC,
                     "Right:", inWest, inWestNPC,
                     "Above:", inAbove, inAboveNPC,
                     "Below:", inBelow, inBelowNPC),
        (1, 0, 0): ("Ahead:", inEast, inEastNPC,
                    " Left:", inNorth, inNorthNPC,
                    "Right:", inSouth, inSouthNPC,
                    "Above:", inAbove, inAboveNPC,
                    "Below:", inBelow, inBelowNPC),
        (-1, 0, 0): ("Ahead:", inWest, inWestNPC,
                     " Left:", inSouth, inSouthNPC,
                     "Right:", inNorth, inNorthNPC,
                     "Above:", inAbove, inAboveNPC,
                     "Below:", inBelow, inBelowNPC)
    }
    # else:
    #     compassDirections = ("North:", inNorth, inNorthNPC,
    #                          " West:", inWest, inWestNPC,
    #                          " East:", inEast, inEastNPC,
    #                          "South:", inSouth, inSouthNPC,
    #                          "Above:", inAbove, inAboveNPC,
    #                          "Below:", inBelow, inBelowNPC)
    #     direction_mapping = {
    #         (0, 1, 0): compassDirections,
    #         (0, -1, 0): compassDirections,
    #         (1, 0, 0): compassDirections,
    #         (-1, 0, 0): compassDirections
    #     }

    direction_info = direction_mapping.get(yo.bearing)

    if direction_info and any(info is not None and info[1] is not None for info in direction_info[1::3]): # I'm sure there's simpler logic for this.
        if 'map' and 'compass' in yo.inventory:
            print(f'--------------------------------------------------------------------- {yo.coordinates[0]}|{yo.coordinates[1]}')
        else:
            print('-----------------------------------------------------------------------------')

        for i in range(0, len(direction_info), 3):
            direction, location, npc_info = direction_info[i], direction_info[i + 1], direction_info[i + 2]
            if location is not None:
                dmCompact(f'{direction} {location}')
                if npc_info:
                    print(f'           {", ".join(filter(None, npc_info))}')


def generateMap(center_coordinates):
    global locations
    places = locations
    grid_size = 9
    half_grid = grid_size // 2

    if 'compass' in yo.inventory:
        if yo.bearing == (0,1,0):
            playerIcon = ' ▲ '
        elif yo.bearing == (-1,0,0):
            playerIcon = ' ◄ '
        elif yo.bearing == (0,-1,0):
            playerIcon = ' ▼ '
        elif yo.bearing == (1,0,0):
            playerIcon = ' ► '
        else:
            playerIcon = ' ■ '
    else:
        playerIcon = ' ■ '

    min_x = center_coordinates[0] - half_grid
    max_x = center_coordinates[0] + half_grid
    min_y = center_coordinates[1] - half_grid
    max_y = center_coordinates[1] + half_grid
    center_z = center_coordinates[2]

    grid = [['   ' for _ in range(grid_size)] for _ in range(grid_size)]

    if 'map' in yo.inventory:
        for y in range(max_y, min_y - 1, -1):
            for x in range(min_x, max_x + 1):
                place = places.get((x, y, center_z), None)
                if place:
                    icon = place.icon
                    grid[max_y - y][x - min_x] = icon.center(3)

        center_x = half_grid
        center_y = half_grid
        grid[center_y][center_x] = playerIcon.center(3)

        print('                        ┌───────────────────────────┐')
        for row in grid:
            print('                        │' + ''.join(row) + '│')
        print("                        └───────────────────────────┘")
    else:
        dmCompact('You don\'t have a map.')


def whereNPC():
    for x in characters.copy():
        print(f'{x.name} {x.currentLocation}')


def endgame():
    saveGame()
    print()
    print('Player visited:', yo.visited)
    print()
    print('NPC LOCATIONS:')
    print()
    for coordinates, place in locations.items():
        if hasattr(place, 'npc'):
            NPCs = [npc.name for npc in place.npc if hasattr(npc, 'name')]

            if NPCs:
                print(f'{coordinates} :: {", ".join(NPCs)}')

    wait(10)
    raise SystemExit
