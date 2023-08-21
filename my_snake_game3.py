from designer import *
from random import randint

#SNAKE GAME

MY_PATH = ""
SNAKE_SPEED = 5
PADDING_FRUIT = 85


#Dictionary TurningPoint
TurningPoint = {
        'x' : int,
        'y' : int,
        'direction': str
        }

#Dictionary World
World = {'snake head': DesignerObject,
         'snake body': [DesignerObject],
         'snake head direction': str,
         'snake body direction': [str],
         'turning points': [TurningPoint],
         'background': DesignerObject,
         'jake the snake message': DesignerObject,
         'fruit': DesignerObject,
         'score': int,
         'counter': DesignerObject
         }


def create_world() -> World:
    """creat_world returns a dictionary containing the world at the beginning of the game"""
    return {'snake head': create_snake_head(),
            'snake body': [],
            'snake head direction': 'right',
            'snake body direction': [],
            'turning points': [],
            'background': create_background(),
            'jake the snake message': create_jake_the_snake_message(),
            'fruit': create_fruit(),
            'score': 0,
            'counter': text('red', 'Score: ', 30, get_width() / 2, 50, font_name = 'Impact')
            }


#BACKGROUND MANAGEMENT ---------------------------------------------------

def create_background() -> DesignerObject:
    """create_background returns a DesignerObject containing the image of the background"""
    background = background_image(MY_PATH + 'snake_game_background_5.jpg')
    return background

def create_jake_the_snake_message() -> DesignerObject:
    """create_jake_the_snake_message returns a DesignerObject containing the image of the jake the snake message"""
    jake_the_snake_message = image(MY_PATH + 'snake_game_jake_the_snake_message.png')
    jake_the_snake_message['scale'] = 1.0
    jake_the_snake_message['y'] = get_height() - PADDING_FRUIT
    return jake_the_snake_message

def update_counter(world: World):
    """update_counter updates the text displayed on screen with the up-to-date score.
    Parameters:
        world: a dictionary of type World"""
    world['counter']['text'] = str(world['score'])

def print_score(world: World):
    """print_score print the score in the console.
    Parameters:
        world: a dictionary of type World"""
    print('Your score was', world['score'])
    
def flash_game_over(world: World):
    """flash_game_over updates the text displayed on screen with the game-over message.
    Parameters:
        world: a dictionary of type World"""
    world['counter']['text'] = 'GAME OVER!'
    create_snake_dizzy(world)


#SNAKE HEAD MANAGEMENT ------------------------------------

def create_snake_head() -> DesignerObject:
    """create_snake_head returns a DesignerObject containing the image of the snake head"""
    snake_head = image(MY_PATH + 'snake_game_snake_head_4.png')
    snake_head['scale'] = 0.2
    snake_head['anchor'] = 'center'
    return snake_head

def move_snake_head(world: World):
    """move_snake_head changes the coordinates of the snake head depending on its direction.
    Parameter:
        world: a dictionary of type World"""
    if (world['snake head direction'] == 'left'):
        world['snake head']['x'] -= SNAKE_SPEED
    elif (world['snake head direction'] == 'right'):
        world['snake head']['x'] += SNAKE_SPEED
    elif (world['snake head direction'] == 'up'):
        world['snake head']['y'] -= SNAKE_SPEED
    elif (world['snake head direction'] == 'down'):
        world['snake head']['y'] += SNAKE_SPEED

def head_left(world: World):
    """head_left modifies the attributes of the snake head to set it left.
    Parameter:
        world: a dictionary of type World"""
    world['snake head']['flip_x'] = True
    world['snake head direction'] = 'left'
    world['snake head']['angle'] = 0
    
def head_right(world: World):
    """head_right modifies the attributes of the snake head to set it right.
    Parameter:
        world: a dictionary of type World"""
    world['snake head']['flip_x'] = False
    world['snake head direction'] = 'right'
    world['snake head']['angle'] = 0
    
def head_up(world: World):
    """head_up modifies the attributes of the snake head to set it up.
    Parameter:
        world: a dictionary of type World"""
    world['snake head']['flip_x'] = False
    world['snake head direction'] = 'up'
    world['snake head']['angle'] = 90
    
def head_down(world: World):
    """head_down modifies the attributes of the snake head to set it down.
    Parameter:
        world: a dictionary of type World"""
    world['snake head']['flip_x'] = False
    world['snake head direction'] = 'down'
    world['snake head']['angle'] = -90

def add_turning_point(world: World):
    """add_turning_point adds a turning point to the list of active turning points
    Parameter:
        world: a dictionary of type World"""
    world['turning points'].append({'x': world['snake head']['x'], \
                                    'y': world['snake head']['y'], \
                                    'direction': world['snake head direction']})
    
def check_at_turning_point(reference_object:DesignerObject, world: World)-> str:
    """check_at_turning_point checks if a reference object is at a turning point
    and returns the new direction if yes, an empty string if no.
    Parameter:
        reference_object: a DesignerObject which we want to test
        world: a dictionary of type World"""
    found = ""
    for turning_point in world['turning points']:
        if (turning_point['x'] == reference_object['x']) and (turning_point['y'] == reference_object['y']):
            found = turning_point['direction']
            return(found)
    return(found)
    
def remove_turning_point(reference_object:DesignerObject, world: World):
    """removes a turning point from the list if the reference object is a match
    Parameter:
        reference_object: a DesignerObject which we want to test
        world: a dictionary of type World"""
    new_list = []
    for turning_point in world['turning points']:
        if (turning_point['x'] == reference_object['x']) and (turning_point['y'] == reference_object['y']):
            print("removing turning point")
        else:
            new_list.append(turning_point)
    world['turning points'] = new_list
            
def flip_snake_head(world: World, key: str):
    """flip_snake_head changes the direction the snake head moves, based on a key stroke
    Parameters:
        world: a dictionary of type World
        key: a str containing the keystroke"""
    if key == 'left':
        head_left(world)
        add_turning_point(world)
    elif key == 'right':
        head_right(world)
        add_turning_point(world)
    elif key == 'up':
        head_up(world)
        add_turning_point(world)
    elif key == 'down':
        head_down(world)
        add_turning_point(world)

def hit_border(world: World) -> bool:
    """hit_border returns a boolean indicating if the snake head has hit the screen border
    Parameters:
        world: a dictionary of type World"""
    if world['snake head']['x'] > get_width():
        return True
    elif world['snake head']['x'] < 0:
        return True
    elif world['snake head']['y'] > get_height():
        return True
    elif world['snake head']['y'] < 0:
        return True
    else:
        return False
    
def is_head_on_snake(world: World) -> bool:
    """is_head_on_snake returns a boolean checking if the heead and the snake 
    body are colliding.
    Parameters:
        world: a dictionary of type World"""
    i = 0
    for body in world['snake body']:
        #we only check is body is not next to the head
        if colliding(world['snake head'], body) and (i>2):
            return True
        i = i + 1
    return False

def create_snake_dizzy(world:World):
    """create_snake_dizzy changes the image for the snake head.
    Parameters:
        world: a dictionary of type World"""
    new_head = image(MY_PATH + 'snake_game_snake_head_dizzy.png')
    new_head['scale'] = 0.2
    new_head['anchor'] = 'center'
    new_head['x'] = world['snake head']['x']
    new_head['y'] = world['snake head']['y']
    new_head['flip_x'] = world['snake head']['flip_x']
    new_head['angle'] = world['snake head']['angle']
    world['snake head'] = new_head
    

# SNAKE BODY MANAGEMENT ---------------------------------

def create_snake_body() -> [DesignerObject]:
    """create_snake_body returns a DesignerObject containing a segment of the snake"""
    snake_body = image(MY_PATH + 'snake_game_snake_body_2.png')
    snake_body['scale'] = 0.2
    snake_body['anchor'] = 'center'
    return snake_body

def set_position_body(reference_element: DesignerObject, direction: str, offset_pixel:int):
    """set_position_body returns the coordinates x and y of an image to be positioned according
    to the direction and position of a reference object.
    Parameters:
        reference_element: a DesignerObject
        direction: the direction of the reference_element
        offset_pixel: the offset of pixels used to position the new body"""
    x = 0
    y = 0
    if (direction == 'left'):
        x = reference_element['x'] + offset_pixel
        y = reference_element['y']
    elif (direction == 'right'):
        x = reference_element['x'] - offset_pixel
        y = reference_element['y']           
    elif (direction == 'up'):
        x = reference_element['x']
        y = reference_element['y'] + offset_pixel
    elif (direction == 'down'):
        x = reference_element['x']
        y = reference_element['y'] - offset_pixel
    return x, y

def make_snake_body(world: World):
    """make_snake_body adds a new segment to the list of body segments
    Parameters:
        world: a dictionary of type World"""
    if (world['snake body'] == []):
        #first body element
        snake_head = world['snake head']
        snake_body_first = create_snake_body()
        offset_pixel = 50
        snake_body_first['x'], snake_body_first['y'] = \
                               set_position_body(snake_head, world['snake head direction'], offset_pixel)
        world['snake body'].append(snake_body_first)
        world['snake body direction'].append(world['snake head direction'])
    else:
        #other body elements
        snake_body_last = world['snake body'][-1]
        snake_body_other = create_snake_body()
        last_body_direction = world['snake body direction'][-1]
        offset_pixel = 25
        snake_body_other['x'], snake_body_other['y'] = \
                               set_position_body(snake_body_last, last_body_direction, offset_pixel)
        world['snake body'].append(snake_body_other)
        world['snake body direction'].append(last_body_direction)

def move_snake_body(world: World):
    """move_snake_body moves each body segment of the snake.
    Parameters:
        world: a dictionary of type World"""
    n = len(world['snake body'])
    for i in range(len(world['snake body'])):
        body_segment = world['snake body'][i]
        #check if body_segment is at a turning point
        #if yes, change its direction
        found_new_direction = check_at_turning_point(body_segment, world)
        if (found_new_direction!=""):
            world['snake body direction'][i] = found_new_direction
        
        #if last body, remove the turning point
        if (i==n-1):
            remove_turning_point(body_segment, world)
        
        body_segment_direction = world['snake body direction'][i]
        if (body_segment_direction == 'left'):
            body_segment['x'] -= SNAKE_SPEED
        elif (body_segment_direction == 'right'):
            body_segment['x'] += SNAKE_SPEED
        elif (body_segment_direction == 'up'):
            body_segment['y'] -= SNAKE_SPEED
        elif (body_segment_direction == 'down'):
            body_segment['y'] += SNAKE_SPEED
        

#FRUIT MANAGEMENT --------------------------------------
            
def is_fruit_on_snake(world: World) -> bool:
    """is_fruit_on_snake returns a boolean checking if the fruit and the snake 
    are colliding.
    Parameters:
        world: a dictionary of type World"""
    if colliding(world['fruit'], world['snake head']):
        return True
    else:
        for body in world['snake body']:
            if colliding(world['fruit'], body):
                return True
    return False
    
def is_fruit_close_to_center(x: int, y: int) -> bool:
    """is_fruit_close_to_center returns a boolean that checks if the fruit is close to the center
    of the screen.
    Parameters:
        x: the x coordinate of the fruit
        y: the y coordinate of the fruit"""
    x_center = get_width() / 2
    y_center = get_height() / 2
    dist_squared = (x_center - x) ** 2 + (y_center - y) ** 2
    if (dist_squared < PADDING_FRUIT ** 2):
        return True
    else:
        return False

def create_fruit() -> DesignerObject:
    """create_fruit returns a Designer object containing the image of the fruit"""
    fruit = image(MY_PATH + 'snake_game_fruit_3.png')
    fruit['scale_x'] = .12
    fruit['scale_y'] = .12
    fruit['x'] = randint(PADDING_FRUIT, get_width() - PADDING_FRUIT)
    fruit['y'] = randint(PADDING_FRUIT, get_height() - PADDING_FRUIT)
    while is_fruit_close_to_center(fruit['x'], fruit['y']):
        fruit['x'] = randint(PADDING_FRUIT, get_width() - PADDING_FRUIT)
        fruit['y'] = randint(PADDING_FRUIT, get_height() - PADDING_FRUIT)
    return fruit

def move_fruit(world: World):
    """move_fruit changes randomly the position of the fruit.
    Parameters:
        world: a dictionary of type World"""
    fruit = world['fruit']
    fruit['x'] = randint(PADDING_FRUIT, get_width() - PADDING_FRUIT)
    fruit['y'] = randint(PADDING_FRUIT, get_height() - PADDING_FRUIT)
    while is_fruit_on_snake(world):
        fruit['x'] = randint(PADDING_FRUIT, get_width() - PADDING_FRUIT)
        fruit['y'] = randint(PADDING_FRUIT, get_height() - PADDING_FRUIT)

def eat_fruit(world: World):
    """eat_fruit manages the situation when the snake eats the fruit.
    Parameters:
        world: a dictionary of type World"""
    if is_fruit_on_snake(world):
        world['score'] += 1
        move_fruit(world)
        make_snake_body(world)


#EVENTS MANAGEMENT -------------------------------

when('starting', create_world)
when('updating', move_snake_head)
when('typing', flip_snake_head)
when('updating', move_snake_body)
when('updating', update_counter)
when('updating', eat_fruit)
when(hit_border, print_score, flash_game_over, pause)
when(is_head_on_snake, print_score, flash_game_over, pause)

start()