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
    door = g.locations.get((0,2,9))
    print()
    breakpoint()
    password = input('Type name: ')
    if password == g.yo.playerName:
        g.dm('The lights flicker brown momentarily, and then you hear a click behind you. You hear the red door behind you creak as it swings slightly ajar.')
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

#%%CHAPTER 1

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
(,,): g.Spot('Passage', 'You are in a passage.',[],[],[])
(,,): g.Spot('Dirt Path', 'You are on a dirt path.',[],[],[])
(,,): g.Spot('Cobbled Path', 'You are on a cobbled path.',[],[],[])
(,,): g.Spot('Brick Path', 'You are on a brick path.',[],[],[])
(,,): g.Spot('Stone Path', 'You are on a stone path.',[],[],[])
(,,): g.Spot('Rocky Path', 'You are on a rocky path.',[],[],[])
(,,): g.Spot('Dusty Path', 'You are on a dusty path.',[],[],[])
(,,): g.Spot('Clay Path', 'You are on a clay path.',[],[],[])
(,,): g.Spot('Muddy Path', 'You are on a muddy path.',[],[],[])
(,,): g.Tree(' ♠ ', 'Apple Tree', 'You are at the foot of an apple tree.',[],[],[], 'apple')
'''
#%% Locations

g.locations = {
    #starting dungeon
    (0,0,9): g.Setting(' · ',(0,1,9), 'Computer Monitor', 0, computerTalk),
    (0,1,9): g.Spot('[_]','Starting Room', 'You are in a damp, dimly-lit room.', ['key'], [],[]),
    (0,2,9): g.Door(' ╫ ','Red Door', 1),

    (0,3,9): g.Spot(' ○ ','Passage', 'You are in a passage.',[],[],[]),
    (0,3,8): g.Spot('═♂ ','Manhole', 'It\'s very dark in here.', [],[],[]),
    (-1,3,8): g.FlatRock('π══','Flat Rock', '', ['gown', 'key', 'map'],['apple'],[]),
    (0,4,9): g.Spot('═╦═','T-Shape','This is the entrance to the passage you came from originally.',[],[],[]),
    (-1,4,9): g.Portal(' ← ',(16,4,9),'Passage'),
    (1,4,9): g.Door('═══','Passage', 0),
    (2,4,9): g.Spot('═╦═','Door 1','You are standing in a passage at the entrance to a doorway.',[],[],[]),
    (2,3,9): g.Portal(' ↓ ',(0,0,0),'Room 1'),
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
    (-4, 4, 0): g.Spot(' · ','Meadow', 'You find yourself in a peaceful meadow with colorful flowers.', ['butterfly'], [], []),
    (-4, 3, 0): g.Spot(' · ','Clearing', 'A small clearing surrounded by tall trees.', ['birdsong'], [], []),
    (-4, 2, 0): g.Spot(' · ','Forest Edge', 'The edge of a dense forest, sunlight filtering through the leaves.', ['acorn'], [], []),
    (-4, 1, 0): g.Spot(' · ','Riverbank', 'You stand by the serene riverbank, the water gently flowing.', ['pebble'], [], []),
    (-4, 0, 0): g.Spot(' · ','Open Field', 'An expansive open field with a clear view of the sky.', [], [], []),
    (-4, -1, 0): g.Spot(' · ','Grassy Path', 'A winding path through tall grass, leading to unknown places.', [], [], []),
    (-4, -2, 0): g.Spot(' · ','Wildflower Patch', 'A colorful patch of wildflowers swaying in the breeze.', ['wildflower'], [], []),
    (-4, -3, 0): g.Spot(' · ','Old Tree', 'An ancient tree with twisted branches, providing shade.', ['leaf'], [], []),
    (-4, -4, 0): g.Spot(' · ','Rocky Outcrop', 'A rocky outcrop with a view of the surrounding landscape.', ['rock'], [], []),
    # Open World Row
    (-3, 4, 0): g.Spot(' · ','Hilltop', 'You climb to the top of a hill, overlooking the land below.', ['view'], [], []),
    (-3, 3, 0): g.Spot(' · ','Sunlit Glade', 'A peaceful glade bathed in sunlight, surrounded by tall trees.', [], [], []),
    (-3, 2, 0): g.Spot(' · ','Winding Path', 'A path winding through the woods, the sound of rustling leaves.', ['twig'], [], []),
    (-3, 1, 0): g.Spot(' · ','Abandoned Campsite', 'Remnants of an old campsite, a faint scent of burnt wood lingers.', ['charcoal'], [], []),
    (-3, 0, 0): g.Spot(' · ','Old Bridge', 'A sturdy old bridge crossing a narrow stream.', ['rusty nail'], [], []),
    (-3, -1, 0): g.Spot(' · ','Thicket', 'A thicket of thorny bushes making progress difficult.', ['thorn'], [], []),
    (-3, -2, 0): g.Spot(' · ','Shaded Pond', 'A small pond surrounded by shade, frogs croaking in the distance.', ['frog'], [], []),
    (-3, -3, 0): g.Spot(' · ','Mossy Boulder', 'A large boulder covered in moss, a cool place to rest.', ['moss'], [], []),
    (-3, -4, 0): g.Spot(' · ','Hidden Well', 'A well hidden among the trees, water dripping from the bucket.', [], [], []),
    # Open World Row
    (-2, 4, 0): g.Spot(' · ','Beehive', 'A buzzing beehive hanging from a tree branch.', ['honeycomb'], [], []),
    (-2, 3, 0): g.Spot(' · ','Dense Thicket', 'A dense thicket with a variety of plant life.', ['flower'], [], []),
    (-2, 2, 0): g.Spot(' · ','Broken Cart', 'The remnants of a broken cart, abandoned long ago.', ['wheel'], [], []),
    (-2, 1, 0): g.Spot(' · ','Sunflower Field', 'A field of bright sunflowers swaying in the breeze.', ['seed'], [], []),
    (-2, 0, 0): g.Spot(' · ','Grazing Deer', 'A group of deer grazing peacefully in the grass.', ['antler'], [], []),
    (-2, -1, 0): g.Spot(' · ','Overgrown Path', 'An overgrown path leading to an unknown destination.', ['vine'], [], []),
    (-2, -2, 0): g.Spot(' · ','Sturdy Oak', 'A sturdy oak tree with a hollow in its trunk.', ['oak acorn'], [], []),
    (-2, -3, 0): g.Spot(' · ','Rustling Leaves', 'A gentle breeze rustles the leaves of the surrounding trees.', ['leaf'], [], []),
    (-2, -4, 0): g.Spot(' · ','Echoing Cave', 'A cave entrance with echoes of mysterious sounds coming from within.', ['echo'], [], []),
    # Open World Row
    (-1, 4, 0): g.Spot(' · ','Pond', 'A tranquil pond with lily pads floating on the surface.', ['lily'], [], []),
    (-1, 3, 0): g.Spot(' · ','Fern Grove', 'A grove filled with lush ferns, creating a magical atmosphere.', ['fern'], [], []),
    (-1, 2, 0): g.Spot(' · ','Mushroom Ring', 'A ring of mushrooms arranged in a mysterious pattern.', ['mushroom'], [], []),
    (-1, 1, 0): g.Spot(' · ','Waterfall', 'A breathtaking waterfall cascading down from a cliff.', [], [], []),
    (-1, 0, 0): g.Spot(' · ','Grassy Knoll', 'You are standing on top of a grassy knoll.', [], [], []),
    (-1, -1, 0): g.Spot(' ☼ ','Cave Entrance', 'You stumble upon a hidden cave.', [], [], []),
    (-1, -2, 0): g.Spot(' · ','Boulder Field', 'A field of large boulders with peculiar markings.', [], [], []),
    (-1, -3, 0): g.Spot(' · ','Whispering Woods', 'The wind whispers through the tall trees in an eerie manner.', [], [], []),
    (-1, -4, 0): g.Spot(' · ','Enchanted Garden', 'A garden with enchanting flowers that glow softly in the dark.', ['flower'], [], []),
    # Cave System
    (-1, -1, -1): g.Spot(' · ','Cave', 'It is very dark in here.', ['bones'], [], []),
    (-1, -1, -2): g.Spot(' · ','Dark Pit', 'You are in a dark pit, there isn\'t much you can see.', [], [], []),
    (-1, 0, -2): g.FlatRock(' ⌂ ','Treasure Chest', 'There is a slight glow from all around you. It seems like the glow is coming from all directions at once. As you look around the cave, you can tell that someone, or something, has been camping here recently. On the ground, you see an old chest.', ['compass'], ['gristle'], []),
    # Open World Row
    (0, 4, 0): g.Spot(' · ','Ancient Ruins', 'Ruins of an ancient civilization, mysterious symbols etched into the stones.', ['relic'], [], []),
    (0, 3, 0): g.Spot(' · ','Sunny Meadow', 'A sunny meadow with butterflies fluttering about.', ['butterfly'], [], []),
    (0, 2, 0): g.Spot(' · ','Whistling Wind', 'The wind whistles through the tall grass, creating a soothing melody.', [], [], []),
    (0, 1, 0): g.Spot(' · ','Giant Oak', 'A giant oak tree with branches reaching for the sky.', ['acorn'], [], []),
    (0, 0, 0): g.Spot(' · ','Grassy Knoll', 'You are standing on top of a grassy knoll.', [], [], []),
    (0, -1, 0): g.Spot(' · ','Tranquil Lake', 'A tranquil lake with crystal-clear water reflecting the surrounding landscape.', ['pebble'], [], []),
    (0, -2, 0): g.Spot(' · ','Willow Tree', 'A majestic willow tree with long, sweeping branches.', ['willow leaf'], [], []),
    (0, -3, 0): g.Spot(' · ','Butterfly Grove', 'A grove filled with colorful butterflies dancing in the air.', ['butterflywing'], [], []),
    (0, -4, 0): g.Spot(' · ','Mystical Pond', 'A pond with mystical properties, the water glows softly.', ['mystical water'], [], []),
    # Open World Row
    (1, 4, 0): g.Spot(' · ','Dragon\'s Lair', 'A cave entrance with carvings resembling dragon scales.', ['dragonscale'], [], []),
    (1, 3, 0): g.Spot(' · ','Eagle\'s Nest', 'A high cliff with an eagle\'s nest perched at the top.', ['feather'], [], []),
    (1, 2, 0): g.Spot(' · ','Glowing Mushrooms', 'A cluster of mushrooms emitting a soft glow in the dark.', ['mushroom'], [], []),
    (1, 1, 0): g.Spot(' · ','Waterfall Cave', 'A hidden cave behind a waterfall, the sound of water echoing inside.', ['echo'], [], []),
    (1, 0, 0): g.Spot(' · ','Bamboo Grove', 'A serene grove with tall bamboo shoots swaying in the breeze.', ['shoot'], [], []),
    (1, -1, 0): g.Spot(' · ','Crystal Clear Creek', 'A creek with crystal-clear water flowing over smooth stones.', ['water'], [], []),
    (1, -2, 0): g.Spot(' · ','Cherry Blossom Tree', 'A cherry blossom tree with delicate pink petals falling like snow.', ['blossom'], [], []),
    (1, -3, 0): g.Spot(' · ','Hidden Garden', 'A hidden garden with rare and exotic plants.', ['rare flower'], [], []),
    (1, -4, 0): g.Spot(' · ','Stone Circle', 'A mysterious circle of standing stones with ancient carvings.', ['stone'], [], []),
    # Open World Row
    (2, 4, 0): g.Spot(' · ','Moss-Covered Bridge', 'A moss-covered bridge spanning a narrow river.', ['moss'], [], []),
    (2, 3, 0): g.Spot(' · ','Firefly Grove', 'A grove filled with fireflies, creating a magical display of lights.', ['firefly'], [], []),
    (2, 2, 0): g.Spot(' · ','Sunset Cliff', 'A cliff with a breathtaking view of the sunset over the horizon.', [], [], []),
    (2, 1, 0): g.Tree(' ♠ ', 'Apple Tree', 'You are at the foot of an apple tree.',[],[],[], 'apple'),
    (2, 0, 0): g.Spot(' · ','Enchanted Forest', 'A forest with trees that seem to whisper secrets to those who listen closely.', [], [], []),
    (2, -1, 0): g.Spot(' · ','Giant\'s Footprint', 'A mysterious giant footprint imprinted in the ground.', ['footprint'], [], []),
    (2, -2, 0): g.Spot(' · ','Gentle Breeze', 'A place where a gentle breeze always seems to blow.', ['breeze'], [], []),
    (2, -3, 0): g.Spot(' · ','Golden Fields', 'Fields of golden wheat swaying in the wind.', ['golden wheat'], [], []),
    (2, -4, 0): g.Spot(' · ','Starlit Sky', 'An open area with a perfect view of the starlit sky at night.', ['starlight'], [], []),
    # Open World Row
    (3, 4, 0): g.Spot(' · ','Rainbow Falls', 'A waterfall with water reflecting the colors of a rainbow.', ['rainbow'], [], []),
    (3, 3, 0): g.Spot(' · ','Singing Birds', 'A grove filled with birds singing harmonious melodies.', ['birdsong'], [], []),
    (3, 2, 0): g.Spot(' · ','Floating Islands', 'Mysterious floating islands with unique flora and fauna.', ['feather'], [], []),
    (3, 1, 0): g.Spot(' · ','Magnetic Rock', 'A rock with magnetic properties, affecting nearby npc.', ['magnet'], [], []),
    (3, 0, 0): g.Spot(' · ','Celestial Pool', 'A pool of water with a celestial glow, reflecting the stars above.', [], [], []),
    (3, -1, 0): g.Spot(' · ','Thunderstorm Valley', 'A valley where thunderstorms are a common occurrence.', ['essence'], [], []),
    (3, -2, 0): g.Spot(' · ','Glowing Caves', 'Caves filled with bioluminescent fungi, creating an otherworldly glow.', ['fungus'], [], []),
    (3, -3, 0): g.Spot(' · ','Lunar Oasis', 'An oasis with water that shimmers in the moonlight.', [], [], []),
    (3, -4, 0): g.Spot(' · ','Aurora Plains', 'Plains where the aurora borealis dances across the night sky.', [], [], []),
    # Open World Row
    (4, 4, 0): g.Spot(' · ','Eternal Flame', 'A flame that never extinguishes, surrounded by a protective barrier.', [], [], []),
    (4, 3, 0): g.Spot(' · ','Giant\'s Rest', 'A massive stone where giants are said to rest during their journeys.', [], [], []),
    (4, 2, 0): g.Spot(' · ','Fairy Ring', 'A magical ring of mushrooms where fairies are said to gather.', [' dust'], [], []),
    (4, 1, 0): g.Spot(' · ','Astral Observatory', 'An observatory where celestial events can be observed.', ['telescope'], [], []),
    (4, 0, 0): g.Spot(' · ','Mystic Arch', 'A mystical arch with symbols representing different realms.', ['symbol'], [], []),
    (4, -1, 0): g.Spot(' · ','Timeless Well', 'A well with water that seems to transcend the boundaries of time.', [], [], []),
    (4, -2, 0): g.Spot(' · ','Dreamer\'s Haven', 'A tranquil haven where dreams are said to take form.', [], [], []),
    (4, -3, 0): g.Spot(' · ','Galactic Garden', 'A garden with plants from distant galaxies, each with unique properties.', ['flower'], [], []),
    (4, -4, 0): g.Spot(' · ','Infinity Pool', 'A pool with water that extends infinitely into the unknown.', [], [], []),
}
