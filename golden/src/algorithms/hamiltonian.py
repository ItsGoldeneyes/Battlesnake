class Hamiltonian:
    '''
    This class contains a very rudimentary implementation of a Hamiltonian cycle.
    It is meant for a solo game on a rectangular map and has no collision detection.
    '''
    def generate_linear_hamiltonian(self, board):
        height = board.get_height()
        width = board.get_width()
        
        left_dir = [{"x": i, "y" : 0} for i in range(1,width)]
        
        top_right = [{"x": i, "y" : height-1} for i in range(0, width, 2)]
        lower_right = [{"x": i, "y" : 1} for i in range(1, width-2, 2)]
        top_right.extend(lower_right)
        right_dir = top_right
        
        up_dir = [{"x":x, "y":y} for x in range(0, width-1, 2) for y in range(1, height-1)]
        up_dir.append({"x":0,"y":0})
        
        down_dir = [{"x":x, "y":y} for x in range(1, width-2, 2) for y in range(2, height)]

        if width % 2 == 0:
            # print("even width")
            down_final = [{"x":width-1, "y":y} for y in range(1, height)]
            
            
            down_dir.extend(down_final) # Up as well?
            # print("down", down_dir)
        else:
            # print("odd width")
            down_final_left = [{"x":width-2, "y":y} for y in range(3, height, 2)]
            down_final_right = [{"x":width-1, "y":y} for y in range(2, height, 2)]
            down_final_right.append({"x":width-1, "y":height})
            down_final_right.append({"x":width-1, "y":1})
            down_final_left.extend(down_final_right)
            down_final = down_final_left
            
            left_final = [{"x":width-1, "y":y} for y in range(3, height, 2)]
            right_final = [{"x":width-2, "y":y} for y in range(2, height, 2)]
            
            down_dir.append({"x":width-3, "y":1})
            down_dir.append({"x":width-1, "y":1})
            down_dir.remove({"x":width-4, "y":2})
            
            
            up_dir.remove({"x":width-3, "y":1})
            up_dir.append({"x":width-2, "y":0})
            
            left_dir.remove({"x":width-2, "y":0})
            left_dir.append({"x":width-2, "y":1})
            
            right_dir.remove({"x":width-4, "y":1})
            right_dir.append({"x":width-4, "y":2})
            
            down_dir.extend(down_final)
            left_dir.extend(left_final)
            right_dir.extend(right_final)
            
            # print("down", down_final)
            # print("left", left_final)
            # print("right", right_final)
            
        
        return up_dir, down_dir, left_dir, right_dir
    
    def get_hamiltonian_move(self, pos, board):
        
        up, down, left, right = self.generate_linear_hamiltonian(board)
        
        if pos in up:
            return "up"
        
        if pos in down:
            return "down"
        
        if pos in left:
            return "left"
        
        if pos in right:
            return "right"
        
        return ""
        