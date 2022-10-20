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
        
        self.name = ''
        self.health = ''
        self.body = ''
        self.head = ''
        self.length = ''
        self.shout = ''
        self.squad = ''
        self.customizations = ''
        
        # Ugly workaround, snakes are in list in data
        for snake in board.board["snakes"]: 
            if snake["id"] == self.id:
                if 'name' in snake:
                    self.name = snake["name"]
                if 'health' in snake:
                    self.health = snake["health"]
                if 'body' in snake:  
                    self.body = snake["body"]
                if 'head' in snake:
                    self.head = snake["head"]
                if 'length' in snake:
                    self.length = snake["length"]
                if 'shout' in snake:
                    self.shout = snake["shout"]
                if 'squad' in snake:
                    self.squad = snake["squad"]
                if 'customizations' in snake:
                    self.customizations = snake["customizations"]  
    
    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def get_health(self):
        return self.health
    
    def get_body(self):
        return self.body
    
    def get_head(self):
        return self.head
    
    def get_length(self):
        return self.length
    
    def get_shout(self):
        return self.shout
    
    def get_squad(self):
        return self.squad
    
    def get_customizations(self):
        return self.customizations
    
    def get_info(self):
        return {
            'id': self.get_id(),
            'name': self.get_name(),
            'health': self.get_health(),
            'body': self.get_body(),
            'head': self.get_head(),
            'length': self.get_id(),
            'shout': self.get_shout(),
            'squad': self.get_squad(),
            'customizations': self.get_customizations(),
                }
    
    
    def update(self, board):
        '''
        When a board is updated, this function is called for each snake.
        '''
        self.body = board.get_position(self.id)
        self.head = self.body[0]
        self.length = board.get_length(self.id)
        self.health = board.get_health(self.id)
        
        return self