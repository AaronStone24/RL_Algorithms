from DRL_in_Action import GridBoard

class GridWorld:
    def __init__(self, size=4, mode='static'):
        if size>=4:
            self.board = GridBoard(size=size)
        else:
            print("Minimum board size is 4")
            self.board = GridBoard(size=4)
        
        #Add pieces, positions will be updated later
        self.board.addPiece('Player','P',(0,0))
        self.board.addPiece('Goal','+',(1,0))
        self.board.addPiece('Pit','-',(2,0))
        self.board.addPiece('Wall','W',(3,0))

        if mode == 'static':
            self.initGridStatic()
        elif mode == 'player':
            self.initGridPlayer()
        else:
            self.initGridRand()

    #Initialize stationary Grid, all items are placed deterministically
    def initGridStatic(self):
        #Setup static pieces
        self.board.components['Player'].pos = (0,3)
        self.board.components['Goal'].pos = (0,0)
        self.board.components['Pit'].pos = (0,1)
        self.board.components['Wall'].pos = (1,1)

    def validateBoard(self):
        valid = True

        player = self.board.components['Player']
        goal = self.board.components['Goal']
        wall = self.board.components['Wall']
        pit = self.board.components['Pit']

        all_pieces = [piece for name,piece in self.board.components.items()]
        all_positions = [player.pos, goal.pos, wall.pos, pit.pos]
        if len(all_pieces) > len(set(all_pieces)):
            return False

        corners = [(0,0), (0,self.board.size), (self.board.size,0), (self.board.size,self.board.size)]
        
        if player.pos in corners or goal.pos in corners:
            val_move_pl = [self.validateMove('Player', addpos) for addpos in [(0,1),(1,0),(-1,0),(0,-1)]]
            val_move_go = [self.validateMove('Goal', addpos) for addpos in [(0,1),(1,0),(-1,0),(0,-1)]]
            if 0 not in val_move_pl or 0 not in val_move_go:
                valid = False
        
        return valid

    def initGridPlayer(self):
        self.initGridStatic()
        self.board.components['Player'].pos = GridBoard.randPair(0,self.board.size)

        if not self.validateBoard():
            self.initGridPlayer()
    
    def initGridRand(self):
        self.board.components['Player'].pos = GridBoard.randPair(0,self.board.size)
        self.board.components['Goal'].pos = GridBoard.randPair(0,self.board.size)
        self.board.components['Pit'].pos = GridBoard.randPair(0,self.board.size)
        self.board.components['Wall'].pos = GridBoard.randPair(0,self.board.size)

        if not self.validateBoard():
            self.initGridRand()

    def validateMove(self, piece, addpos=(0,0)):
        outcome = 0     #0 for valid, 1 invalid, 2 lost game
        pit = self.board.components['Pit'].pos
        wall = self.board.components['Wall'].pos
        new_pos = GridBoard.addTuple(self.board.components[piece].pos, addpos)
        
        if new_pos == wall:
            outcome = 1
        elif max(new_pos) > (self.board.size-1):
            outcome = 1
        elif min(new_pos) < 0:
            outcome = 1
        elif new_pos == pit:
            outcome = 2

        return outcome

    def makeMove(self, action):
        def checkMove(addpos):
            if self.validateMove('Player', addpos) in [0,2]:
                new_pos = GridBoard.addTuple(self.board.components['Player'].pos, addpos)
                self.board.movePiece('Player', new_pos)
        
        if action == 'u':
            checkMove((-1,0))
        elif action == 'd':
            checkMove((1,0))
        elif action == 'l':
            checkMove((0,-1))
        elif action == 'r':
            checkMove((0,1))
        else:
            pass

    def reward(self):
        if self.board.components['Player'].pos == self.board.components['Pit'].pos:
            return -10
        elif self.board.components['Player'].pos == self.board.components['Goal'].pos:
            return 10
        else:
            return -1
    
    def display(self):
        return self.board.render()