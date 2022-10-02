class BattleSnake:
    '''
    This class represents the snakes in a game of BattleSnake.
    Every board object contains multiple snakes.
    Snakes only contain getters and setters, as well as an update method.
    '''
    def __init__(self, board, id=""):
        '''
        This constructor assigns the snake's ID as well as the snake's attributes.
        Assigning the attributes is messy because the snakes are in a list.
        '''
        if id == "":
            id = board.get_self_id()
            
        self.id = id
        
        # Ugly workaround, snakes are in list in data
        for snake in board.board["snakes"]: 
            if snake["id"] == self.id:
                self.head = snake["head"]
                self.body = snake["body"]
                self.length = snake["length"]
                self.health = snake["health"]
    
    def get_id(self):
        return self.id
    
    def get_head(self):
        return self.head
    
    def get_body(self):
        return self.body
    
    def get_length(self):
        return self.length
    
    def get_health(self):
        return self.health
    
    def update(self, board):
        '''
        When a board is updated, this function is called for each snake.
        '''
        self.head, self.body = board.get_position(self.id)
        self.length = board.get_length(self.id)
        self.health = board.get_health(self.id)
        
        return self