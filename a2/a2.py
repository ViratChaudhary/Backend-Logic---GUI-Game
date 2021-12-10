"""
CSSE1001 Assignment 2
Semester 2, 2020
"""
from a2_support import *

# Fill these in with your details

__author__ = "{{Virat Chaudhary}} ({{s4641144}})"
__email__ = "v.chaudhary@uqconnect.edu.au"
__date__ = "28 September 2020"

# Write your code here

class Entity:
    '''create a general entity.'''

    def __init__(self):
        '''Constructor: Entity()'''

        self._collision_state = True
        self._id = 'Entity'

    def get_id(self):
        '''
        gets the ID of the entity.

        Returns:
            id (str): The ID of the entity.
        '''

        return self._id

    def set_collide(self, collidable):
        '''
        sets the collision state of the entity.

        Parameters:
            collidable (bool): the collision state.
        '''

        if collidable != self._collision_state:
            self._collision_state = collidable
        
    def can_collide(self):
        '''
        gets the collision state of the entity.

        Returns:
            _collision_state (bool): the collision state.
        '''

        return self._collision_state

    def __str__(self):
        '''
        gets the formal identification of the entity including the entity ID. 

        Returns:
            (str): entity formal identification.
        '''

        return "Entity('{}')".format(self._id)

    def __repr__(self):
        '''
        gets the formal identification of the entity including the entity ID. 

        Returns:
            (str): entity formal identification.
        '''

        return self.__str__()

class Wall(Entity):
    '''create a wall entity inherited by the general entity.'''

    def __init__(self):
        '''Constructor: Wall()'''

        self._collision_state = False
        self._id = WALL

    def __str__(self):
        '''
        gets the formal identification of the wall entity including the wall entity ID. 

        Returns:
            (str): wall entity formal identification.
        '''

        return "Wall('{}')".format(self._id)

class Item(Entity):
    '''create an item entity inherited by the general entity.'''

    def __str__(self):
        '''
        gets the formal identification of the item entity including the item entity ID. 

        Returns:
            (str): item entity formal identification.
        '''

        return "Item('{}')".format(self._id)

    def on_hit(self, game):
        '''
        raises a NotImplementedError for items that do not have specified on_hit.  

        Parameters:
            game (GameLogic()): the game logic instance.

        Returns:
            error -> NotImplementedError()
        '''

        raise NotImplementedError()

class Key(Item):
    '''create a key entity inherited by the item entity.'''

    def __init__(self):
        '''Constructor: Key()'''

        self._id = KEY
        self._collision_state = True

    def on_hit(self, game):
        '''
        handles the collection of the key, adding it to the player inventory 
        and removing the key entity from game when player hits key. 

        Parameters:
            game (GameLogic()): the game logic instance.
        '''

        player_position = game._player.get_position()
        game._player.add_item(self)
        game.get_game_information().pop(player_position)

    def __str__(self):
        '''
        gets the formal identification of the key entity including the key entity ID. 

        Returns:
            (str): key entity formal identification.
        '''

        return "Key('{}')".format(self._id)

class MoveIncrease(Item):
    '''create a move increase entity inherited by the item entity.'''

    def __init__(self, moves=5):
        '''
        Constructor: MoveIncrease(int)

        Parameters:
            moves (int): number of moves added to the maximum moves allowed by the player.
        '''

        self._moves = moves
        self._collision_state = True
        self._id = MOVE_INCREASE

    def __str__(self):
        '''
        gets the formal identification of the move increase entity including the move increase entity ID. 

        Returns:
            (str): move increase entity formal identification.
        '''

        return "MoveIncrease('{}')".format(self._id)

    def on_hit(self, game):
        '''
        handles changing the move count of the player and removing the move increase entity when player hits move increase. 

        Parameters:
            game (GameLogic()): the game logic instance.
        '''

        player_position = game._player.get_position()
        game._player.change_move_count(self._moves)
        game.get_game_information().pop(player_position)

class Door(Entity):
    '''create a door entity inherited by the general entity.'''

    def __init__(self):
        '''Constructor: Door()'''

        self._id = DOOR
        self._collision_state = True

    def on_hit(self, game):
        '''
        handles checking if player has key, and setting the game win condition when player reaches the door.

        Parameters:
            game (GameLogic()): the game logic instance .
        '''

        player_inventory = game._player.get_inventory()
        for i in player_inventory:
            if i.get_id() == KEY:
                game.set_win(True)

        if game.won() == False:
            print("You don't have the key!")

    def __str__(self):
        '''
        gets the formal identification of the door entity including the door entity ID. 

        Returns:
            (str): door entity formal identification.
        '''

        return "Door('{}')".format(self._id)

class Player(Entity):
    '''create a player entity inherited by the general entity.'''

    def __init__(self, move_count):
        '''
        Constructor: Player(int)

        Parameters:
            move_count (int): number of moves the player can take.
        '''

        self._id = PLAYER
        self._collision_state = True
        self._player_position = None
        self._move_count = move_count
        self._inventory = []

    def set_position(self, position):
        '''
        sets the position of the player within the game using a tuple containing a row and column coordinate.

        Parameters:
            position (tuple<int, int>): the position coordinates of the player.
        '''

        if position != self._player_position:
            self._player_position = position

    def get_position(self):
        '''
        gets the position coordinates of the player.

        Returns:
            _player_position (tuple<int, int>): the position coordinates of the player.
        '''

        return self._player_position

    def change_move_count(self, number):
        '''
        changes the move count of the player to allow for more or less moves remaining.

        Parameters:
            number (int): number of moves to be added (positive int) or subtracted (negative int).
        '''

        self._move_count += number

    def moves_remaining(self):
        '''
        returns the move count for the player indicating how many moves the player has remaining before losing.  

        Returns:
            _move_count (int): move count for the player.
        '''

        return self._move_count

    def add_item(self, item):
        '''
        adds an entity item to the player inventory list. This is to be used by the key on_hit method. 

        Parameters:
            item (Entity): the item to be added to the player inventory.
        '''

        self._inventory.append(item)

    def get_inventory(self):
        '''
        returns a list of all the items in the player inventory. This can be empty or have items within it. 

        Returns:
            _inventory (list<Entity>): the inventory of the player. 
        '''

        return self._inventory

    def __str__(self):
        '''
        gets the formal identification of the player entity including the player entity ID. 

        Returns:
            (str): player entity formal identification.
        '''

        return "Player('{}')".format(self._id)

class GameLogic:
    '''create a game.'''

    def __init__(self, dungeon_name="game1.txt"):
        '''
        Constructor: GameLogic(str)

        Parameters:
            dungeon_name (str): The name of the level.
        '''

        self._dungeon = load_game(dungeon_name)
        self._dungeon_size = len(self._dungeon)

        #you need to implement the Player class first.
        self._player = Player(GAME_LEVELS[dungeon_name])
        
        #you need to implement the init_game_information() method for this.
        self._game_information = self.init_game_information()
    
        self._win = False

    def get_positions(self, entity):
        """ Returns a list of tuples containing all positions of a given Entity
             type.

        Parameters:
            entity (str): the id of an entity.

        Returns:
            )list<tuple<int, int>>): Returns a list of tuples representing the 
            positions of a given entity id.
        """

        positions = []
        for row, line in enumerate(self._dungeon):
            for col, char in enumerate(line):
                if char == entity:
                    positions.append((row,col))
        return positions

    def get_dungeon_size(self):
        '''
        returns a integer representing the size of the dungeon (width). 

        Returns:
            _dungeon_size (int): size of the dungeon
        '''

        return self._dungeon_size

    def init_game_information(self):
        '''
        returns a dictionary of key, value pairs where the key represents the coordinates or position
        and the value is the entity that occupies the position. 

        Returns:
            locations (dict<tuple<int, int>, Entity>): the dictionary with positions and its corresponding entities. 
        '''

        locations = {}
        
        key_pos = self.get_positions(KEY)
        door_pos = self.get_positions(DOOR)
        wall_pos = self.get_positions(WALL)
        move_inc_pos = self.get_positions(MOVE_INCREASE)
        player_pos = self.get_positions(PLAYER)

        self._player.set_position(player_pos[0])
        
        for pos in key_pos:
            locations[pos] = Key()

        for pos in door_pos:
            locations[pos] = Door()

        if len(move_inc_pos) != 0:
            for pos in move_inc_pos:
                locations[pos] = MoveIncrease()        

        for pos in wall_pos:
            locations[pos] = Wall()

        return locations
        
    def get_game_information(self):
        '''
        returns the dictionary of postion tuples and its corresponding entities defined from
        init_game_information. 

        Returns:
            (dict<tuple<int, int>, Entity>): the dictionary with positions and its corresponding entities. 
        '''

        return self._game_information

    def get_player(self):
        '''
        returns the player entity that was instantiated in the GameLogic constructor. 

        Returns:
            _player (Entity): the player entity.
        '''

        return self._player

    def get_entity(self, position):
        '''
        returns the entity that occupies the position in the game using the get_game_information method. 

        Parameters:
            position (tuple<int, int>): the position coordinates of the entity.

        Returns:
            (Entity): the entity that is present at the position given. 
        '''

        positions = self.get_game_information()
        return positions.get(position)

    def get_entity_in_direction(self, direction):
        '''
        returns the entity that occupies the position in the given direction from player using the get_entity method.

        Parameters:
            direction (str): the direction that is used to identify the entity. 

        Returns:
            (Entity): the entity that is present in the specified direction from player. 
        '''

        directed_position = self.new_position(direction)
        return self.get_entity(directed_position)

    def collision_check(self, direction):
        '''
        checks if a player can move in a specified direction and returns a bool of false if the player can o
        therwise true, usign the get_entity_in_direction method.

        Parameters:
            direction (str): the direction that is used to identify the entity. 

        Returns:
            (bool): true or false depending on if the player collides with the entity in the given direction.
        '''

        entity_in_direction = self.get_entity_in_direction(direction)
        if entity_in_direction == None:
            return False 

        if entity_in_direction.can_collide() == True:
            return False
        
        return True

    def new_position(self, direction):
        '''
        returns a tuple of the new position of the player given a direction the player is moving. 

        Parameters:
            direction (str): the direction that is used for player movement.

        Returns:
            (tuple<int, int>): the new position coordinates of the player for the specified direction. 
        '''

        player_x, player_y = self._player.get_position()
        possible_directions = ['W', 'A', 'S', 'D']

        if direction in possible_directions:
            player_x += DIRECTIONS.get(direction)[0]
            player_y += DIRECTIONS.get(direction)[1]

        return (player_x, player_y)

    def move_player(self, direction):
        '''
        moves the player in the given direction, updating the player position  using the new_position method.

        Parameters:
            direction (str): the direction that is used for player movement.   
        '''

        self._player.set_position(self.new_position(direction))

    def check_game_over(self):
        '''
        uses the player moves_remaining method to check if the player can make more moves and returns 
        false if it can make more moves, otherwise returns true. 

        Returns:
            (bool): true or false dependant on how many remaining moves the player has. 
        '''

        if self._player.moves_remaining() == 0:
            return True
        return False
        
    def set_win(self, win):
        '''
        uses a bool to set the game win condition to true or false. This is by dafault false. 

        Parameters:
            win (bool): true if the game has been won and false otherwise
        '''

        if win != self._win:
            self._win = win

    def won(self):
        '''
        returns the game win condition defined in set_win method. 

        Returns:
            _win (bool): true if the game has been won and false otherwise.
        '''
        
        return self._win

class GameApp:
    '''create a gameapp which handles user interactions, game logic and displaying of the game.'''

    def __init__(self):

        '''Constructor: GameApp()'''

        self._game = GameLogic()
        self._display = Display(self._game._game_information, self._game._dungeon_size)
    
    def play(self):

        '''
        handles the player interactions during the game for changing positions of player,
        entering help and quit commands and indicating invalid inputs
        '''

        # This while loop uses the check_game_over method to evalaute the moves remaining for the player. If True then player loses. 
        while self._game.check_game_over() == False:

            self.draw()
            action = input('Please input an action: ')

            # This ifstatement checks if the user input one of ['Q', 'H', 'W', 'S', 'D', 'A'] excluding Investigate from valid commands. 
            if action in VALID_ACTIONS[-6:]:

                if action == HELP:
                    print(HELP_MESSAGE)

                if action == QUIT:
                    quit_choice = input('Are you sure you want to quit? (y/n): ')
                    if quit_choice == 'y':
                        return
                    elif quit_choice == 'n':
                        continue
                    else:
                        print(INVALID)

                # This if statement checks if the user input is in ['W', 'S', 'D', 'A'], which are inputs for player movement.
                if action in VALID_ACTIONS[-4:]:

                    '''
                    This if statement checks whether the player collides with the entity in the direction.
                    If the player can move in the direction, then a new appropriate position is set for the player.  
                    '''
                    if self._game.collision_check(action) == False:
                        self._game.move_player(action)

                        player_position = self._game.get_player().get_position()
                        key_position = self._game.get_positions(KEY)[0]
                        door_position = self._game.get_positions(DOOR)[0]
                        moveinc_position_list = self._game.get_positions(MOVE_INCREASE)

                        '''
                        This if statement runs the on_hit method for key when the player arrives at the key.
                        The key gets added to the player inventory and removed from the game as it can no longer be collected. 
                        '''
                        if player_position == key_position:
                            self._game.get_entity(key_position).on_hit(self._game)


                        '''
                        This if statement checks whether the move increase list defined above contains a position at all.
                        If it does then the game has a move increase entity. If the player reaches it, then the on_hit method 
                        for move increase adds moves to the player move count and removes move increase from the game. 
                        '''
                        if len(moveinc_position_list) != 0:
                            if player_position == moveinc_position_list[0]:
                                self._game.get_entity(moveinc_position_list[0]).on_hit(self._game)

                        '''
                        This if statement runs the on_hit method for door if the player arrives at the door.
                        This is where it checks whether the player has the key and sets the game win state appropriately.
                        '''
                        if player_position == door_position:
                            hit_on_door = self._game.get_entity(door_position).on_hit(self._game)
                            if self._game.won():
                                break
                    else:
                        print(INVALID)
                    
                    self._game.get_player().change_move_count(-1)

            else:

                '''
                This if statement checks for the investigate command that was excluded above. 
                it prints a string explaining the entity in the direction that was to be investigated and reduces the move count.
                '''
                if action == 'I A' or action == 'I S' or action == 'I D' or action == 'I W':
                    ent_in_dir = self._game.get_entity_in_direction(action[-1])
                    print('{} is on the {} side.'.format(ent_in_dir, action[-1]))
                    self._game.get_player().change_move_count(-1)
                else:
                    print(INVALID)

        # This if statement checks for the state of the game, and whether it has been won or not and prints result appropriately. 
        if self._game.won() == True:
            print(WIN_TEXT)
        else:
            print(LOSE_TEST)
            
    def draw(self):
        '''
        handles the displaying of the game and the indication of moves remaining for the player.
        This method is to be used with play() for user inputs after the game and moves remaining are displayed.
        '''
        self._display.display_game(self._game.get_player().get_position())
        self._display.display_moves(self._game.get_player().moves_remaining())       

def main():
    a = GameLogic()
    print(a.get_game_information())
    
if __name__ == "__main__":
    main()
