class BattleSnake:
    
    def __init__(self, board, id=""):
        if id == "":
            id = board.get_self_id()
            
        self.id = (id)
        self.head, self.body = board.get_position(self.id)
        self.length = board.get_length(self.id)
        self.health = board.get_health(self.id)
    
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
        self.head, self.body = board.get_position(self.id)
        self.length = board.get_length(self.id)
        self.health = board.get_health(self.id)