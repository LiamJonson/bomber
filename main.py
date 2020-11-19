# process player input
def get_keyboard_input():
    return input()


player_inputs = {'w': "up", 'a': "left",
                 's': 'down', 'd': 'right',
                 ' ': 'bomb'
                 }


def process_player_input(player_input):
    x, y = dict(game_objects)[('player',)]['position']
    if player_input == 'up':
        x = x - 1
    elif player_input == 'down':
        x = x + 1
    elif player_input == 'right':
        y = y + 1
    elif player_input == 'left':
        y = y - 1
    elif player_input == 'bomb':
        new_objects.append(create_object('bomb', (x, y)))
    movements.append((("player",), (x, y)))


# GLOBALS
game_state = "in_progress"
game_objects = {}
new_objects = []
movements = []
interactions = []
old_objects = []


# GAME OBJECTS LOGIC


def idle_logic(_):
    pass


#def bomb_logic(bomb_object):
#    raise NotImplementedError///////////////////////////////////////////////
#def bomb_logic(bomb_object):
#    for game_object in game_objects:
#        if game_object[0] == 'bomb':
#            if game_objects[game_object]['life_time'] != 0:
#                game_objects[game_object]['life_time'] -= 1
#            else:
#                old_objects.append(game_object)
#                n = game_objects[game_object]['position']
#                new_objects.append(('heatwave', {'passable': True, 'interactable': True, },(n[0],n[1]-1)))
#                new_objects.append(('heatwave', {'passable': True, 'interactable': True, }, (n[0]-1, n[1])))
#                new_objects.append(('heatwave', {'passable': True, 'interactable': True, }, (n[0], n[1])))
#                new_objects.append(('heatwave', {'passable': True, 'interactable': True, }, (n[0], n[1] + 1)))
#                new_objects.append(('heatwave', {'passable': True, 'interactable': True, }, (n[0]+1 , n[1])))
def bomb_logic(bomb_object):
    print(game_objects[bomb_object]['life_time'])
    if game_objects[bomb_object]['life_time'] > 0:
        game_objects[bomb_object]['life_time'] -= 1
    else:
        koords = (game_objects[bomb_object]['position'][0], game_objects[bomb_object]['position'][1])
        old_objects.append(bomb_object)
        for i in [-1, 0, 1]:
            new_objects.append(create_object('heatwave', (koords[0] + i, koords[1])))
        for j in [-1, 1]:
            new_objects.append(create_object('heatwave', (koords[0], koords[1] + j)))
#def heatwave_logic(heatwave):
#    raise NotImplementedError/////////////////////////////////////////////////////////////////
def heatwave_logic(heatwave):
    for game_object in game_objects:
        if game_object[0] == 'heatwave':
            old_objects.append(game_object)
#def heatwave_logic(heatwave):
#    old_objects.append(heatwave)



object_logics = {
    'bomb': bomb_logic,
    'heatwave': heatwave_logic
}


def process_objects_logic():
    for game_object in game_objects:
        object_logics.get(game_object[0], idle_logic)(game_object)


# UTILITIES
# def get_objects_by_coords(position):
#    raise NotImplementedError

def get_objects_by_coords(position):
    n = []
    for i, j in dict(game_objects).items():
        if j['position'] == position:
            n.append(i)
    return n


objects_ids_counter = 0


def get_next_counter_value():
    global objects_ids_counter
    result = objects_ids_counter
    objects_ids_counter += 1
    return result


# OBJECT CREATION

def add_new_objects():
    for obj_type, obj_props, obj_coords in new_objects:
        others = get_objects_by_coords(obj_coords)
        if all(game_objects[o]['interactable'] for o in others):
            obj_props['position'] = obj_coords
            obj_key = (obj_type,) if obj_type == 'player' else (obj_type, get_next_counter_value())
            game_objects[obj_key] = obj_props

#def add_new_objects():         ///defect func-change str.101
#    for i in new_objects:
#        n = get_next_counter_value()
#        k = i[1]
#        k.update({'position': i[2]})
#        if get_objects_by_coords(i[2]):
#            k = game_objects[get_objects_by_coords(i[2])[0]]
#            if k['interactable'] == True:
#                game_objects.update({(i[0], n): k})
#            elif k['interactable'] == False:
#                continue
#            else:
#                game_objects.update({(i[0], n): k})
#

obj_types_to_char = {
    'player': "@", "wall": '#', 'soft_wall': '%', 'heatwave': '+', "bomb": '*', "coin": '$'
}


def create_object(type, position, **kwargs):
    desc = {'position': position,
            'passable': type not in ['wall', 'soft_wall'],
            'interactable': type not in ['wall'],
            'char': obj_types_to_char[type]
            }
    if type == 'player':
        desc['coins'] = 0
    if type == 'bomb':
        desc['power'] = 3
        desc['life_time'] = 3
    desc.update(kwargs)
    return type, desc, position


# OBJECT MOVEMENT
# def move_objects():
#    raise NotImplementedError
#def move_objects():
#    for i in movements:
#        p = get_objects_by_coords(i[1])
#        if p:
#            if game_objects[p[0]]['passable'] == True:
#                if game_objects[p[0]]['interactable'] == True:
#                    #if i[0] not in interactions:
#                    #    interactions.append(((i[0]), (*p)))
#                    print(interactions,'****',i[0],'*****',*p)
#
#                    interactions.append((i[0],*(p)))
#                    game_objects[i[0]].update({'position': i[1]})
#                else:
#                    game_objects[i[0]].update({'position': i[1]})
#        elif not p:
#            game_objects[i[0]].update({'position': i[1]})
#    movements.clear()
def move_objects():
    interactions.clear()
    for move in movements:
        obj1, coord = move
        inter = get_objects_by_coords(coord)
        if not inter:
            game_objects[obj1]['position'] = coord
        else:
            if all(game_objects[i]['passable'] != False for i in inter):
                game_objects[obj1]['position'] = coord
                for obj2 in inter:
                    interactions.append((obj1, obj2))
    movements.clear()
# OBJECT REMOVAL
# def remove_objects():
#    raise NotImplementedError


def remove_objects():
    for i in old_objects:
        if game_objects.get(i):
            del game_objects[i]
    old_objects.clear()


# OBJECT INTERACTIONS
def idle_interaction(o1, o2):
    pass


#def player_interaction(player, object):
#    raise NotImplementedError
def player_interaction(player, obj):
    if 'coin' in obj:
        old_objects.append(obj)

#def wave_interaction(wave, object):
#    raise NotImplementedError
def wave_interaction(wave, obj):
    if 'soft_wall' in obj or 'player' in obj:
        old_objects.append(obj)




interaction_funs = {
    'player': player_interaction,
    'heatwave': wave_interaction,
}


def process_interactions():
    print((interactions))
    for obj1, obj2 in interactions:
        interaction_funs.get(obj1[0], idle_interaction)(obj1, obj2)
        interaction_funs.get(obj2[0], idle_interaction)(obj2, obj1)
    interactions.clear()


# def check_game_state():
#    raise NotImplementedError

def check_game_state():
    k = [i[0] for i in game_objects.keys()]
    if 'player' not in k:
        return "lose"
    elif 'coin' not in k:
        return "win"
    else:
        return "in_progress"


# GRAPHIC
def draw_screen(screen):
    for line in screen:
        print(''.join(line))


def render_screen():
    screen = [["." for _ in range(10)] for __ in range(10)]
    for obj, desc in dict(game_objects).items():
        x, y = desc['position']
        screen[x][y] = desc['char']
    return screen


# GAME LOAD

level_example = """
##########
#@  %    #
#   %    #
#  %%%   #
# %%$%%  #
#  %%%   #
#   %    #
#   %    #
#   %    #
##########
"""


#def load_level(level):
#    raise NotImplementedError
def load_level(level):
    char_to_type = dict(map(reversed, obj_types_to_char.items()))
    game_objects.clear()

    new_objects[:] = [
        create_object(char_to_type[char], (i, j))
        for i, row in enumerate(level.strip().splitlines())
        for j, char in enumerate(row)
        if char in char_to_type]

    add_new_objects()

#def load_level(level):
#    game_objects.clear()
#    n = [i for i in level.strip().split('\n')]
#    m = {j: i for i, j in obj_types_to_char.items()}
#    for i, j in enumerate(n):
#        for k, l in enumerate(j):
#            if l == ' ':
#                continue
#            else:
#                new_objects.append((create_object(m[l], (i, k))))
#    add_new_objects()
#
# GAME


load_level(level_example)
screen = render_screen()
draw_screen(screen)

while game_state == 'in_progress':

    kb_inp = get_keyboard_input()
    if kb_inp == "ESC":
        game_state = "finished"
        break

    if kb_inp in player_inputs:
        process_player_input(player_inputs[kb_inp])

    process_objects_logic()
    add_new_objects()
    move_objects()
    process_interactions()
    remove_objects()

    screen = render_screen()
    draw_screen(screen)

    game_state = check_game_state()

if game_state == 'win':
    print("You win")
elif game_state == 'lose':
    print("You lost")
else:
    print("Bye Bye!")
