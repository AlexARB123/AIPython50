import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # For this condition to be met, the count has to be equal to the number of cells in the set
        # If so, we return all cells
        if len(self.cells) == self.count:
            return self.cells

        return set()
        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # For this condition to be met, the count has to be equal to 0
        # If so, return all cells
        if self.count == 0:
            return self.cells

        return set()
        raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # We need to check if the cell is in the sentence
        if cell in self.cells:
            # Since we know it as a mine, we can remove it and reduce the sentence count
            self.cells.remove(cell)
            self.count -= 1
        
        return None
        raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # We need to check if the cell is in the sentence
        if cell in self.cells:
            # Since we know it safe, we remove it from the sentence without increasing or decreasing the count
            self.cells.remove(cell)
        
        return None
        raise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        empty = Sentence(set(), 0)
        # 1) Mark the cell as a move made
        self.moves_made.add(cell)

        # 2) Mark the cell as safe
        self.safes.add(cell)

        # 3) Create a new sentence with the cell and all of it's neighboring cells
        # Make sure sentence checks for all cells AND discards cells which status is already known
        min_i = max(cell[0] - 1, 0)
        max_i = min(cell[0] + 2, self.height)
        min_j = max(cell[1] - 1, 0)
        max_j = min(cell[1] + 2, self.width)
        
        print(min_i, max_i, min_j, max_j)
        newCells = set()
        currMines = count
        for i in range(min_i, max_i):
            for j in range(min_j, max_j):
                print(i,j)
                if (i,j) in self.safes:
                    continue
                if (i,j) in self.moves_made:
                    continue
                if (i,j) in self.mines:
                    currMines = currMines -1
                    continue
                if (i,j) == cell:
                    continue
                
                newCells.add((i,j))

        newSentence = Sentence(newCells, currMines)
        
        if newSentence != empty:
            print("Check: ", newSentence)
            if newSentence not in self.knowledge:
                self.knowledge.append(newSentence)

        # 4) Mark any additional cells as safe or as mines
        for sentence in self.knowledge:
            if sentence.known_mines().copy():
                for cells in sentence.known_mines().copy():
                    self.mark_mine(cells)
            if sentence.known_safes().copy():
                for cells in sentence.known_safes().copy():
                    self.mark_safe(cells)
        # 5) Add any new sentences that can be inferred from exisiting knowledge
        for sentence in self.knowledge:
            print(sentence)
        for sentence in self.knowledge:
            if newSentence.cells.issubset(sentence.cells) and sentence.count > 0 and newSentence.count > 0 and newSentence != sentence:
                createSentence = Sentence(list(sentence.cells.difference(newSentence.cells)), sentence.count - newSentence.count)
                if createSentence != empty:
                    self.knowledge.append(createSentence)
                    print("Sentence created")
        
        # 6) Add any new knowledge to the know mines
        for sentence in self.knowledge:
            if sentence.known_mines().copy():
                for cells in sentence.known_mines().copy():
                    self.mark_mine(cells)
            if sentence.known_safes().copy():
                for cells in sentence.known_safes().copy():
                    self.mark_safe(cells)

        return None
        raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        moves = self.safes - self.moves_made
        if moves:
            newMove = random.choice(tuple(moves))
            return newMove
        
        return None
        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Check if move can be made
        moves = []
        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.moves_made and (i,j) not in self.mines:
                    moves.append((i,j))
        if len(moves) == 0:
            return None
        else:
            return random.choice(moves)
        raise NotImplementedError