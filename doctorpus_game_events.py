import doctorpus_game_classes_functions as g

#%% AGENDA
'''
AGENDA:

    Create a tower that teleports you back to the starting dungeon.
    Good excuse to test out the wall class.

    From now on, I want to more or less leave the game classes and functions alone, unless I really need some more.
    I want to focus on building the world and the story.

CONVENTION:

    I know this isn't how you're supposed to do it, but I am camelCase for everthing.
    If it starts with a capital letter, it's a class, otherwise it's a function or variable.
    Next big project I'll try to stick to convention more.

'''
#%% World Building shortcuts

def map(x,y,z):
    g.generateMap((x,y,z))

#%%EVENTS

def computerTalk():
    g.dm('As you approach the computer, the screen turns itself on, and these words appear on the screen:')
    g.dmSlow(f'"Welcome, {g.yo.playerName} #{g.yo.deaths}"')
    g.dm('As you stand in front of the computer, the screen blinks off for a few seconds, then another message appears:')
    g.dmSlow('"What is your name?"')
    door = g.locations.get((0,1,9))
    print()
    password = input('Type name: ')
    if password == g.yo.playerName:
        g.dm('The lights flicker brown momentarily, and then you hear a click behind you.')
        g.dmSlow('You hear the red door behind you creak as it swings slightly ajar.')
        door.lock = 0
    else:
        g.goBack()
        g.dm('You hear a hatch open above you, and a giant worm falls down from the roof. With a squelching bark, it shows a line of tiny teeth and throws itself at you.')
        outcome = g.performCombat('Worm',2,1)
        if outcome:
            g.dm('The worm falls to the floor, and in a sort of agonising squirm, it is clear that it is defeated.')
            g.kill()
        else:
            g.dm('The worm wraps itself around your head, and the last thing you feel is the wet slime choking you as it burrows its way into your mouth.')
            g.die()


def visitCrystal():
    g.dmCompact("As you approach the crystal, it begins to hum. It pusles purple light.")
    g.wait(2)
    g.dm("Everything goes dark, and you feel yourelf being put to sleep as if a switch went off in your head and turned you off. Your body flops to the floor.")
    g.wait(2)
    g.dm('You feel as though you are being handled by a writhing swarm of slimy worms, and they put things in your mouth and pull things out of your nose.')
    g.wait(3)
    g.dmSlow('Suddenly, you awake again, as though it was all a strange dream.')


def roomOne():
    g.dm('There is a notebook on the floor, attached to a chain bolted to the floor.')
    choice = g.makeChoice(['Read notebook','Ignore'])

    if choice == 0:
        chapterOne()


def chapterOne():
    g.dm("\"I was awakened sometime in the early morning by a loud crash and a stampeding noise from upstairs.  A voice barked some orders, ‘Team One, upstairs and grab him.  Everyone else, stick to the plan.’  Heavy boots clumped up the stairs with surprising speed and before I was awake enough to realize what had happened, there were bright LED lights shining in my face.  The room suddenly seemed very small, with the shapes of a dozen or so large men surrounding me.  I was grabbed and my head was forced onto a dusty-smelling bag.  Hands were everywhere, holding me, sticking needles into me, and half-walking-half-dragging me out of my bedroom and down the bumpy stairs.  My memory is unclear of what happened next, I assume some kind of sedative was applied and I was bundled into a vehicle and carted off.")
    input('Turn page >')
    g.dm("\"I awoke again, slowly at first.  The ceiling was closer to my face than I had remembered.  Then I remembered my vivid dream of the night before and sat up.  This wasn’t my bedroom and that wasn’t my ceiling.  These white sheets were not mine and the clinical-looking bedside table I had never seen before.  I rubbed my eyes and looked into a stainless-steel mirror on the wall.  ‘Golly, I’ve either gotten to the age where I’m in an old people’s home and can’t remember how I got there, or that wasn’t a dream I had last night. I wonder if this has anything to do with the –’")
    input('Turn page >')
    g.dm("\"As if in answer to my question the door opened abruptly and a pleasant looking man stepped into the room wearing a white lab coat and round glasses.  His hair was slicked back and he had some kind of electronic device cupped over his left ear. He had a red pen tucked behind his other ear and was holding a clipboard underneath his arm.  He took a military step forward and stuck out his hand.  I shook it.  ‘Who …?’\"")
    g.dm("The rest of the pages of the notebook were torn out.")

#%% NPCs

PoohBear = g.Bear((-1, -1, -2), (-1, -1, -2),
                'Pooh Bear', 10, 100, 'male',
                'Ferocious bear, frothing at the mouth with bloodlust',
                40, 'furs', 'This bear has survived many winters in this area, and lives in a cave nearby.')

EdwardBear = g.Bear((-1, 0, -2), (-1, 0, -2),
                  'Edward Bear', 10, 100, 'male',
                  'Ferocious bear, frothing at the mouth with bloodlust',
                  40, 'furs', 'This bear has survived many winters in this area, and lives in a cave nearby.')

Paddington = g.Bear((-1, -1, -1), (-1, -1, -1),
                  'Paddington', 10, 100, 'male',
                  'Ferocious bear, frothing at the mouth with bloodlust',
                  40, 'furs', 'This bear has survived many winters in this area, and lives in a cave nearby.')

Ebenezer = g.Trader((0,0,0), (0,0,0),
                  'Ebenezer', 100, 100, 'male',
                  'An old peddlar, carting about his wares.', 1000,
                  ['compass','map','telescope'], 'He\'s been doing this for as long as he can remember.',
                  ['steamed hams'])

Domenic = g.Trader((4,4,0), (4,4,0),
                  'Domenic', 100, 100, 'male',
                  'An old peddlar, carting about his wares.', 1000,
                  ['compass','map','telescope'], 'He\'s been doing this for as long as he can remember.',
                  ['carbonara','bolognese','panchetta'])

Worm1 = g.Worm((16,2,9), (16,2,9), 'Worm', 2, 4, 'worm', '', 1, 'slime', '')

g.characters = [
    PoohBear,
    EdwardBear,
    Paddington,
    Ebenezer,
    Domenic,
    Worm1,
]

#%% Generic Location attributes
'''
(,,): g.Spot('','Passage', 'You are in a passage.',[],[],[]),
(,,): g.Spot('','Dirt Path', 'You are on a dirt path.',[],[],[]),
(,,): g.Spot('','Cobbled Path', 'You are on a cobbled path.',[],[],[]),
(,,): g.Spot('','Brick Path', 'You are on a brick path.',[],[],[]),
(,,): g.Spot('','Stone Path', 'You are on a stone path.',[],[],[]),
(,,): g.Spot('','Rocky Path', 'You are on a rocky path.',[],[],[]),
(,,): g.Spot('','Dusty Path', 'You are on a dusty path.',[],[],[]),
(,,): g.Spot('','Clay Path', 'You are on a clay path.',[],[],[]),
(,,): g.Spot('','Muddy Path', 'You are on a muddy path.',[],[],[]),
(,,): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
(,,): g.Tree(' ♠ ', 'Apple Tree', 'You are at the foot of an apple tree.',[],[],[], 'apple'),
'''
#%% Locations

g.locations = {
    #starting dungeon
    (0,-1,9): g.Setting(' · ',(0,0,9), 'Computer Monitor', 0, computerTalk),
    (0,0,9): g.Spot('[_]','Starting Room', 'You are in a damp, dimly-lit room.', ['key'], [],[]),
    (0,1,9): g.Door(' ╫ ','Red Door', 1),
    (0,2,9): g.Spot(' ○ ','Passage', 'You are in a passage.',[],[],[]),
    (0,2,8): g.Spot('═≡ ','Manhole', 'It\'s very dark in here.', [],[],[]),
    (-1,2,8): g.FlatRock('π══','Flat Rock', '', ['gown', 'key', 'map'],['apple'],[]),
    (0,3,9): g.Door(' ╫ ','Door 0', 1),
    (0,4,9): g.Spot('═╦═','T-Shape','This is the entrance to the passage you came from originally.',[],[],[]),
    (-1,4,9): g.Portal(' ← ',(16,4,9),'Passage'),
    (1,4,9): g.Door('═══','Passage', 0),
    (2,4,9): g.Spot('═╦═','Door 1','You are standing in a passage at the entrance to a doorway.',[],[],[]),
    (2,3,9): g.Scene('[1]', 'Room 1', 'You are standing in a mostly empty room, similar to the one you came from. Instead of a computer monitor on the opposite wall this time, there is a strange apparatus consisting of a tangle of wires attached to a dimly glowing crystal. There is a notebook on the floor.', [], [], [], 0, roomOne),
    (2,2,9): g.Portal(' ↓ ',(0,0,0),'Apparatus'),
    (3,4,9): g.Door('═══','Passage', 0),
    (4,4,9): g.Spot('═╦═','Door 2','You are standing in a passage at the entrance to a doorway.',[],[],[]),
    (5,4,9): g.Door('═══','Passage', 0),
    (6,4,9): g.Spot('═╦═','Door 3','You are standing in a passage at the entrance to a doorway.',[],[],[]),
    (7,4,9): g.Door('═══','Passage', 0),
    (8,4,9): g.Spot('═╦═','Door 4','You are standing in a passage at the entrance to a doorway.',[],[],[]),
    (9,4,9): g.Door('═══','Passage', 0),
    (10,4,9): g.Spot('═╦═','Door 5','You are standing in a passage at the entrance to a doorway.',[],[],[]),
    (11,4,9): g.Door('═══','Passage', 0),
    (12,4,9): g.Spot('═╦═','Door 6','You are standing in a passage at the entrance to a doorway.',[],[],[]),
    (13,4,9): g.Door('═══','Passage', 0),
    (14,4,9): g.Spot('═╦═','Door 7','You are standing in a passage at the entrance to a doorway.',[],[],[]),
    (15,4,9): g.Door('═══','Passage', 0),
    (16,4,9): g.Spot('═╦═','Door 8','You are standing in a passage at the entrance to a doorway.',[],[],[]),
    (16,3,9): g.Spot(' ║ ','Passage', 'You are in a passage.',[],[],[]),
    (16,2,9): g.Spot('[!]','Fight Room', 'You are in a room with so many giant worms that you can\'t even see the floor.',[],[],[]),
    (17,4,9): g.Portal(' → ',(0,4,9),'Passage'),
    # Open world Row
    (-4, 4, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (-4, 3, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (-4, 2, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (-4, 1, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (-4, 0, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (-4, -1, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (-4, -2, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (-4, -3, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (-4, -4, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    # Open World Row
    (-3, 4, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (-3, 3, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (-3, 2, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (-3, 1, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (-3, 0, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (-3, -1, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (-3, -2, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (-3, -3, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (-3, -4, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    # Open World Row
    (-2, 4, 0): g.Spot(' Θ ','Beehive', 'You see beehive hanging from a bush, with bees buzzing around it going about their business.', [], ['honeycomb'], []),
    (-2, 3, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (-2, 2, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (-2, 1, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (-2, 0, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (-2, -1, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (-2, -2, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (-2, -3, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (-2, -4, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    # Open World Row
    (-1, 4, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (-1, 3, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (-1, 2, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (-1, 1, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (-1, 0, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (-1, -1, 0): g.Spot(' ☼ ','Cave Entrance', 'You stumble upon a hidden cave.', [], [], []),
    (-1, -2, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (-1, -3, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (-1, -4, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    # Cave System
    (-1, -1, -1): g.Spot(' O ','Cave', 'It is very dark in here.', ['bones'], [], []),
    (-1, -1, -2): g.Spot(' O ','Dark Pit', 'You are in a dark pit, there isn\'t much you can see.', [], [], []),
    (-1, 0, -2): g.FlatRock(' ⌂ ','Treasure Chest', 'There is a slight glow from all around you. It seems like the glow is coming from all directions at once. As you look around the cave, you can tell that someone, or something, has been camping here recently. On the ground, you see an old chest.', ['compass'], ['gristle'], []),
    # Open World Row
    (0, 4, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (0, 3, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (0, 2, 0): g.Spot(' ┌─','Dirt Path', 'You are on a dirt path.',[],[],[]),
    (0, 1, 0): g.Spot(' │ ', 'Dirt Path', 'You are on a dirt path.',[],[],[]),
    (0, 0, 0): g.Spot('w∩w','Grassy Knoll', 'You are standing on top of a grassy knoll.', [], [], []),
    (0, -1, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (0, -2, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (0, -3, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (0, -4, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    # Open World Row
    (1, 4, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (1, 3, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (1, 2, 0): g.Spot('───','Dirt Path', 'You are on a dirt path.',[],[],[]),
    (1, 1, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (1, 0, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (1, -1, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (1, -2, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (1, -3, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (1, -4, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    # Open World Row
    (2, 4, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (2, 3, 0): g.Spot('█▀█','Dark Tower', 'You step inside the tower door and see a ladder going up.', [], [], []),
    (2, 2, 0): g.Spot('─┘ ','Dirt Path', 'You are on a dirt path.',[],[],[]),
    (2, 1, 0): g.Tree(' ♠ ', 'Apple Tree', 'You are at the foot of an apple tree.',[],[],[], 'apple'),
    (2, 0, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (2, -1, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (2, -2, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (2, -3, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (2, -4, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    # Dark Tower
    (2, 3, 1): g.Portal(' ≡ ',(2,3,2),'Ladder'),
    (2, 3, 2): g.Spot('[ ]','Tower Room', 'The ladder leads to a stone room, and there is another ladder above.',[],[],[]),
    (2, 3, 3): g.Portal(' ≡ ',(2,3,4),'Ladder'),
    (2, 3, 4): g.Spot('[ ]','Tower Room', 'The ladder leads to a stone room, and there is another ladder above.',[],[],[]),
    (2, 3, 5): g.Portal(' ≡ ',(2,3,6),'Ladder'),
    (2, 3, 6): g.Spot('[ ]','Tower Top', 'You reach the top of the tower, and there is a glowing crystal above you, with some steps leading up to it.',[],[],[]),
    (2, 3, 7): g.Setting('{ }', (0,0,9), 'Crystal', 0, visitCrystal),
    # Open World Row
    (3, 4, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (3, 3, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (3, 2, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (3, 1, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (3, 0, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (3, -1, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (3, -2, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (3, -3, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (3, -4, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    # Open World Row
    (4, 4, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (4, 3, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (4, 2, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (4, 1, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (4, 0, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (4, -1, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (4, -2, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (4, -3, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
    (4, -4, 0): g.Spot('wWw','Grass', 'You are in a grassy meadow.',[],[],[]),
}
