"""
chomp.py

an example of an alpha-beta game search

See 
    * http://en.wikipedia.org/wiki/Chomp 
    * http://en.wikipedia.org/wiki/Alpha-beta_pruning

Tested with python 2.7.5 and graphviz (dot) version 2.30.1

Jim Mahoney | cs.marlboro.edu | MIT License | Jan 2014

Output

    $ python chomp.py

    ---- chomp alpha-beta search ----

    The player who can take no apples 
    and is left with the poison loses.

         0 1 2 3 4
        ----------
     0 | p a a a a
     1 | a a a a a
     2 | a a a a a

     Random player chomps below/right (2, 4).

         0 1 2 3 4
        ----------
     0 | p a a a a
     1 | a a a a a
     2 | a a a a .

     AI player chomps below/right (2, 3).

         0 1 2 3 4
        ----------
     0 | p a a a a
     1 | a a a a a
     2 | a a a . .

     Random player chomps below/right (1, 1).

         0 1 2 3 4
        ----------
     0 | p a a a a
     1 | a . . . .
     2 | a . . . .

     AI player chomps below/right (0, 3).

         0 1 2 3 4
        ----------
     0 | p a a . .
     1 | a . . . .
     2 | a . . . .

     Random player chomps below/right (0, 2).

         0 1 2 3 4
        ----------
     0 | p a . . .
     1 | a . . . .
     2 | a . . . .

     AI player chomps below/right (2, 0).

         0 1 2 3 4
        ----------
     0 | p a . . .
     1 | a . . . .
     2 | . . . . .

     Random player chomps below/right (0, 1).

         0 1 2 3 4
        ----------
     0 | p . . . .
     1 | a . . . .
     2 | . . . . .

     AI player chomps below/right (1, 0).

         0 1 2 3 4
        ----------
     0 | p . . . .
     1 | . . . . .
     2 | . . . . .

    Done. Random player loses.


    $ python chomp.py analyze

    Prints one line for each board position examined in 
    the search tree for the 2 x 3 board, giving 
     [list of moves] alpha beta (pruned moves, if any)
    The order is that of the values returned, depth first.

     [(), (1, 2), (0, 2), (1, 1), (0, 1), (1, 0)] 2 -inf 
     [(), (1, 2), (0, 2), (1, 1), (0, 1)] 2 inf 
     [(), (1, 2), (0, 2), (1, 1), (1, 0), (0, 1)] 2 -inf 
     [(), (1, 2), (0, 2), (1, 1), (1, 0)] 2 2 pruning []
     [(), (1, 2), (0, 2), (1, 1)] 2 -inf 
     [(), (1, 2), (0, 2), (0, 1), (1, 0)] -3 inf 
     [(), (1, 2), (0, 2), (0, 1)] -3 2 pruning []
     [(), (1, 2), (0, 2), (1, 0), (0, 1)] -3 inf 
     [(), (1, 2), (0, 2), (1, 0)] -3 2 pruning []
     [(), (1, 2), (0, 2)] 2 inf 
     [(), (1, 2), (1, 1), (0, 2), (0, 1), (1, 0)] 2 -inf 
     [(), (1, 2), (1, 1), (0, 2), (0, 1)] 2 2 pruning []
     [(), (1, 2), (1, 1), (0, 2), (1, 0), (0, 1)] 2 -inf 
     [(), (1, 2), (1, 1), (0, 2), (1, 0)] 2 2 pruning []
     [(), (1, 2), (1, 1), (0, 2)] 2 -inf 
     [(), (1, 2), (1, 1)] 2 2 pruning [(0, 1), (1, 0)]
     [(), (1, 2), (0, 1), (1, 0)] 4 -inf 
     [(), (1, 2), (0, 1)] 4 2 pruning []
     [(), (1, 2), (1, 0), (0, 2), (0, 1)] -3 2 
     [(), (1, 2), (1, 0), (0, 2)] -3 -inf 
     [(), (1, 2), (1, 0), (0, 1)] 4 -3 
     [(), (1, 2), (1, 0)] 4 2 pruning []
     [(), (1, 2)] 2 -inf 
     [(), (0, 2), (1, 1), (0, 1), (1, 0)] -3 inf 
     [(), (0, 2), (1, 1), (0, 1)] -3 2 pruning []
     [(), (0, 2), (1, 1), (1, 0), (0, 1)] -3 inf 
     [(), (0, 2), (1, 1), (1, 0)] -3 2 pruning []
     [(), (0, 2), (1, 1)] 2 inf 
     [(), (0, 2)] 2 2 pruning [(0, 1), (1, 0)]
     [(), (1, 1), (0, 2), (0, 1), (1, 0)] -3 inf 
     [(), (1, 1), (0, 2), (0, 1)] -3 2 pruning []
     [(), (1, 1), (0, 2), (1, 0), (0, 1)] -3 inf 
     [(), (1, 1), (0, 2), (1, 0)] -3 2 pruning []
     [(), (1, 1), (0, 2)] 2 inf 
     [(), (1, 1)] 2 2 pruning [(0, 1), (1, 0)]
     [(), (0, 1), (1, 0)] -5 inf 
     [(), (0, 1)] -5 2 pruning []
     [(), (1, 0), (0, 2), (0, 1)] 4 2 
     [(), (1, 0), (0, 2)] 4 inf 
     [(), (1, 0), (0, 1)] -5 4 
     [(), (1, 0)] -5 2 pruning []
     [()] 2 inf 
 
    $ python chomp.py graph | dot -Tpng > tree.png

    Generates tree.png image of game search of a 2 x 3 board. 
    The search looks at 42 board positions (listed above),
    shown in the 1923 x 1056 pixel image.

    Similarly, the image tree_big.png shows the full search of 
    a 3 x 3 board : 527 board positions in a 19377 x 1632 pixel image.
  
"""
from copy import deepcopy
import random
import sys
inf = float('inf')  # infinity

class Chomp(object):
    """ A game 2D rectangular take away last-move-loses game.

        >>> print Chomp(rows=3, columns=5).do((1,3))
             0 1 2 3 4
            ----------
         0 | p a a a a
         1 | a a a . .
         2 | a a a . .
        <BLANKLINE>

    """

    # The game board looks like this initially.
    #
    #       p a a a a a a
    #       a a a a a a a
    #       a a a a a a a   rows        top left is 'p'oison
    #       a a a a a a a                 others are  'a'pples
    #       a a a a a a a
    #
    #                width
    #
    # On each turn, a player 'chomps' a rectangle below and to the right
    # of a (row, col) move, where 0 <= col < width and 0 <= row < rows.
    #
    # The game is stored both as a list of (row, col) moves 
    # (starting with None for the starting board) and the corresponding
    # board position (letters stored in a matrix) after that move.
    # Letters that are "chomped" are replaced by periods.
    #
    # If the only move remaining is the p (poison apple), 
    # the player whose move it is loses.
    
    def __init__(self, rows=3, columns=5):
        self.rows = rows
        self.columns = columns
        self.search_depth = rows * columns   # i.e. search the whole move tree
        self.moves = [()]
        self.boards = [self.initial_board()]
        self.debug_output = False
    
    def initial_board(self):
        """ Return starting grid :'p' top left, 'a' everywhere else """ 
        grid = [None] * self.rows
        grid[0] = ['p'] + ['a'] * (self.columns - 1) # e.g. ['p', 'a', 'a' , 'a']
        for i in range(1, self.rows):
            grid[i] = ['a'] * self.columns           # e.g. ['a', 'a', 'a' , 'a']
        return grid

    def board(self):
        """ Return grid of p's and a's for the current board position. """
        return self.boards[-1]

    def __str__(self):
        """ Return string representation of board """
        grid = self.board()
        result =  ' '*5 + ' '.join(map(lambda x: str(x), 
                                       range(self.columns))) + '\n'
        result += ' '*4 + '--' * self.columns + '\n'
        i = 0
        for row in grid:
            result += ' {} | '.format(i) + ' '.join(row) + '\n'
            i += 1
        return result

    def label(self, head='', foot=''):
        """ board as html graphviz label"""
        grid = self.board()
        result = '<table>'
        if head: 
            result += '<tr><td>' + head + '</td></tr>'
        result += '<tr><td>'
        for row in grid:
            result += ' '.join(row) + "<br/>"
        result = result[:-5] + '</td></tr>'
        if foot:
            result += '<tr><td>' + foot + '</td></tr>'
        return result + '</table>'
    
    def get_random_move(self):
        """ Return a random legal move """
        return random.choice(self.possible_moves())

    def do(self, move):
        """ Applying a move to the game state. Return self. """
        self.moves.append(move)
        grid = deepcopy(self.board())
        for col in xrange(move[1], self.columns):
            for row in xrange(move[0], self.rows):
                grid[row][col] = '.'
        self.boards.append(grid)
        return self

    def undo(self, move):
        """ Remove that last move from the game state. Return self. """
        self.moves.pop()
        self.boards.pop()
        return self

    def possible_moves(self):
        """ Return the list of legal moves. 
            >>> Chomp(2,2).possible_moves()
            [(1, 1), (0, 1), (1, 0)]
        """
        grid = self.board()
        possible = []
        for col in xrange(self.columns):
            for row in xrange(self.rows):
                if grid[row][col] == 'a':
                    possible.append((row,col))
        possible.reverse()   # maybe this order is better for search pruning?
        return possible

    def finished(self):
        """ Return True if game is done. """
        # The game is done if there are no 'a' characters on the board.
        grid = self.board()
        for col in xrange(self.columns):
            for row in xrange(self.rows):
                if grid[row][col] == 'a':
                    return False
        return True

    def evaluate(self):
        """ Return value of game position from the point of view the
            player whose turn it is to move.
             value > 0 means winning,
             value < 0 means losing, and
             larger (smaller) is better (worse). """
        # win_value is a positive number which is larger earlier in the game,
        # so that the algorithm chooses earlier wins over later wins.
        win_value = 2 + self.columns * self.rows - len(self.moves)
        if self.finished():       # If game is over, then current player
            return - win_value    # (whose turn it is to move) has lost.
        else:
            return 0              # The game isn't over; return 'I dunno'

    def analyze(self):
        """ print move search tree """
        #  This one has some pruning and is manageable size : 
        #  Chomp(3,3).do((1,1)).analyze()
        self.get_alphabeta_move(save_nodes=True)
        # print " nodes = {}".format(len(self.nodes))
        # return
        # self.nodes.sort(key=lambda x: (x['depth'], x['node']))
        for n in self.nodes:
            print " {} {} {} {}".format(
                n['node'], n['alpha'], n['beta'], n['prune'])

    def graphviz_analyze(self):
        """ print graphvize version of search tree """
        self.get_alphabeta_move(save_nodes=True)
        # print " nodes = {}".format(len(self.nodes))        
        # return
        # self.nodes.sort(key=lambda x: (x['depth'], x['node']))
        ranks = [''] * self.search_depth
        print "digraph chomp {"
        print ' graph [fontname="Anonymous Pro"]';
        for n in self.nodes:
            print '{} [label=<{}> shape=none];'.format(hash(n['node']), n['label'])
            if ranks[n['depth']] == '':
                ranks[n['depth']] = '{rank=same'
            ranks[n['depth']] += ' ' + str(hash(n['node']))
        for r in ranks:
            if r != '':
                print r + '};'
        for n in self.nodes:
            if n['depth'] != 0:
                print "{} -> {};".format(hash(n['parent']), hash(n['node']))
        print "}"
            
    def init_search_analysis(self, save_nodes):
        """ Initialize search tree node storage """
        self.save_nodes = save_nodes
        if save_nodes:
            self.nodes = []
        
    def search_analysis(self, depth, alpha, beta, prune=''):
        """ If enabled, store this node of the search tree """
        if self.save_nodes:
            if depth % 2 == 1:
                # Make the sign of alpha & beta consistent
                # with 1st player's point of view.
                (alpha, beta) = (-alpha, -beta)
            self.nodes.append({'node': str(self.moves), 
                               'label' : self.label(
                                   "{},{}".format(alpha,beta), prune),
                               'parent': str(self.moves[:-1]),
                               'alpha':alpha, 'beta':beta, 
                               'depth': depth, 'prune':prune})

    def get_alphabeta_move(self, save_nodes=False):
        """ Return the best move found by searching the move tree. """
        # Call this to start the recursive alphabeta search.
        # Optionally remember the nodes of the search tree.
        self.init_search_analysis(save_nodes)
        beta = inf
        alpha = -inf
        alpha_move = None             # best move found for current player
        for move in self.possible_moves():
            self.do(move)
            value = - self.alphabeta(1, -beta, -alpha)
            self.undo(move)
            if value > alpha:
                (alpha, alpha_move) = (value, move)
        self.search_analysis(0, alpha, beta)
        return alpha_move

    def alphabeta(self, depth, alpha, beta):
        """ Return game value via a recursive alpha-beta game search. """
        # search depth increases downward, with 0 at the root of the tree.
        if depth >= self.search_depth or self.finished():
            value = self.evaluate()
            self.search_analysis(depth, value, beta)
            return value
        possible = self.possible_moves()
        for i in xrange(len(possible)):
            self.do(possible[i])
            value = - self.alphabeta(depth + 1, -beta, -alpha)
            self.undo(possible[i])
            if value >= beta:     # abandon branch; other player can do better
                self.search_analysis(depth, value, beta, 
                                     'pruning ' + str(possible[i+1:]))
                return value
            if value > alpha:     # new best value for current player
                alpha = value
        self.search_analysis(depth, alpha, beta)
        return alpha

def play():
    print "---- chomp alpha-beta search ----\n"
    print "The player who can take no apples "
    print "and is left with the poison loses.\n"
    game = Chomp()
    player = 'Random'
    while not game.finished():
        print game
        move = {'Random'   : game.get_random_move, 
                'AI' : game.get_alphabeta_move}[player]()
        print " {} player chomps below/right {}.\n".format(player, move)
        game.do(move)
        player = {'AI' : 'Random', 
                  'Random' : 'AI'}[player]
    print game
    print "Done. {} player loses.\n".format(player)


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'graph':
            Chomp(2,3).graphviz_analyze()
        else:
            Chomp(2,3).analyze()
    else:
        play()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    main()
    
