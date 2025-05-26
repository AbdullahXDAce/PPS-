import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 640
BOARD_SIZE = 8
SQUARE_SIZE = WIDTH // BOARD_SIZE
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
HIGHLIGHT = (247, 247, 105, 150)
CAPTURE_HIGHLIGHT = (255, 50, 50, 150)
MOVE_HIGHLIGHT = (106, 168, 79, 150)

# Piece colors
WHITE_PIECE = (230, 230, 230)
BLACK_PIECE = (50, 50, 50)
PIECE_OUTLINE = (70, 70, 70)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Chess with Unique Pieces")
clock = pygame.time.Clock()

class Piece:
    def __init__(self, type, color, x, y):
        self.type = type
        self.color = color
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.is_moving = False
        self.captured = False
        self.capture_particles = []
        self.piece_color = WHITE_PIECE if color == WHITE else BLACK_PIECE
    
    def draw(self, surface):
        # Draw capture particles if any
        for particle in self.capture_particles[:]:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 1
            
            if particle[2] <= 0:
                self.capture_particles.remove(particle)
            else:
                pygame.draw.circle(surface, 
                                 (random.randint(200, 255), random.randint(100, 200), random.randint(0, 100)), 
                                 (int(particle[0][0]), int(particle[0][1])), 
                                 int(particle[2] / 2))
        
        if self.captured:
            return
            
        # Smooth movement
        if self.is_moving:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist < 0.5:
                self.x = self.target_x
                self.y = self.target_y
                self.is_moving = False
            else:
                self.x += dx * 0.2
                self.y += dy * 0.2
        
        # Draw the piece
        center_x = self.x * SQUARE_SIZE + SQUARE_SIZE // 2
        center_y = self.y * SQUARE_SIZE + SQUARE_SIZE // 2
        radius = SQUARE_SIZE // 3
        small_radius = radius // 2
        
        # Draw different shapes for each piece type
        if self.type == 'pawn':
            # Pawn - Cone shape with base
            pygame.draw.circle(surface, self.piece_color, (center_x, center_y + radius//3), radius)
            pygame.draw.polygon(surface, self.piece_color, [
                (center_x, center_y - radius),
                (center_x - radius//1.5, center_y + radius//3),
                (center_x + radius//1.5, center_y + radius//3)
            ])
            
        elif self.type == 'rook':
            # Rook - Castle shape with battlements
            pygame.draw.rect(surface, self.piece_color, 
                           (center_x - radius, center_y - radius//2, radius*2, radius*1.5))
            # Battlements
            for i in range(3):
                x_pos = center_x - radius + i * radius
                pygame.draw.rect(surface, self.piece_color, 
                               (x_pos, center_y - radius, radius//2, radius//2))
            
        elif self.type == 'knight':
            # Knight - Horse head shape
            pygame.draw.ellipse(surface, self.piece_color, 
                              (center_x - radius, center_y - radius//2, radius*2, radius*1.5))
            pygame.draw.polygon(surface, self.piece_color, [
                (center_x - radius//2, center_y - radius),
                (center_x, center_y - radius*1.3),
                (center_x + radius//2, center_y - radius)
            ])
            # Ear
            pygame.draw.circle(surface, self.piece_color, 
                             (center_x - radius//3, center_y - radius*1.1), radius//4)
            
        elif self.type == 'bishop':
            # Bishop - Mitre hat shape
            pygame.draw.ellipse(surface, self.piece_color, 
                              (center_x - radius//1.5, center_y, radius*1.5, radius))
            pygame.draw.polygon(surface, self.piece_color, [
                (center_x, center_y - radius*1.2),
                (center_x - radius, center_y),
                (center_x + radius, center_y)
            ])
            # Cross on mitre
            pygame.draw.line(surface, PIECE_OUTLINE, 
                           (center_x, center_y - radius*1.2), 
                           (center_x, center_y - radius//2), 2)
            pygame.draw.line(surface, PIECE_OUTLINE, 
                           (center_x - radius//3, center_y - radius//1.5), 
                           (center_x + radius//3, center_y - radius//1.5), 2)
            
        elif self.type == 'queen':
            # Queen - Crown shape with jewel
            pygame.draw.circle(surface, self.piece_color, (center_x, center_y - radius//3), small_radius)
            pygame.draw.polygon(surface, self.piece_color, [
                (center_x, center_y - radius*1.3),
                (center_x - radius, center_y),
                (center_x + radius, center_y)
            ])
            # Crown points
            for i in range(3):
                x_pos = center_x - radius + i * radius
                pygame.draw.polygon(surface, self.piece_color, [
                    (x_pos, center_y - radius//2),
                    (x_pos + radius//2, center_y),
                    (x_pos - radius//2, center_y)
                ])
            # Jewel
            pygame.draw.circle(surface, (255, 215, 0) if self.color == WHITE else (200, 0, 0), 
                             (center_x, center_y - radius//3), small_radius//2)
            
        elif self.type == 'king':
            # King - Crown with cross
            pygame.draw.circle(surface, self.piece_color, (center_x, center_y - radius//3), small_radius)
            pygame.draw.polygon(surface, self.piece_color, [
                (center_x, center_y - radius*1.3),
                (center_x - radius, center_y),
                (center_x + radius, center_y)
            ])
            # Cross
            pygame.draw.rect(surface, self.piece_color, 
                           (center_x - radius//6, center_y - radius*1.5, radius//3, radius*1.2))
            pygame.draw.rect(surface, self.piece_color, 
                           (center_x - radius//2, center_y - radius, radius, radius//3))
        
        # Outline for all pieces
        pygame.draw.circle(surface, PIECE_OUTLINE, (center_x, center_y), radius, 2)
    
    def move_to(self, x, y):
        self.target_x = x
        self.target_y = y
        self.is_moving = True
    
    def capture(self):
        self.captured = True
        # Create particles for capture effect
        center_x = self.x * SQUARE_SIZE + SQUARE_SIZE // 2
        center_y = self.y * SQUARE_SIZE + SQUARE_SIZE // 2
        
        for _ in range(20):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(1, 5)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            lifetime = random.randint(20, 40)
            self.capture_particles.append([[center_x, center_y], [dx, dy], lifetime])

def draw_board(surface):
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            color = LIGHT_SQUARE if (x + y) % 2 == 0 else DARK_SQUARE
            pygame.draw.rect(surface, color, (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_highlights(surface, moves, selected_piece):
    if selected_piece:
        # Highlight selected piece
        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        s.fill(HIGHLIGHT)
        surface.blit(s, (selected_piece.x * SQUARE_SIZE, selected_piece.y * SQUARE_SIZE))
        
        # Highlight possible moves
        for move in moves:
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            
            # Check if move is a capture
            target_piece = None
            for piece in pieces:
                if piece.x == move[0] and piece.y == move[1] and not piece.captured:
                    target_piece = piece
                    break
            
            if target_piece:
                s.fill(CAPTURE_HIGHLIGHT)
            else:
                s.fill(MOVE_HIGHLIGHT)
            
            surface.blit(s, (move[0] * SQUARE_SIZE, move[1] * SQUARE_SIZE))

def get_possible_moves(piece, pieces):
    moves = []
    
    # Pawn moves
    if piece.type == 'pawn':
        direction = -1 if piece.color == WHITE else 1
        
        # Forward move
        if 0 <= piece.y + direction < BOARD_SIZE:
            square_empty = True
            for p in pieces:
                if p.x == piece.x and p.y == piece.y + direction and not p.captured:
                    square_empty = False
                    break
            
            if square_empty:
                moves.append((piece.x, piece.y + direction))
                
                # Double move from starting position
                if ((piece.color == WHITE and piece.y == 6) or 
                    (piece.color == BLACK and piece.y == 1)):
                    square_empty = True
                    for p in pieces:
                        if p.x == piece.x and p.y == piece.y + 2*direction and not p.captured:
                            square_empty = False
                            break
                    if square_empty:
                        moves.append((piece.x, piece.y + 2*direction))
        
        # Capture moves
        for dx in [-1, 1]:
            new_x, new_y = piece.x + dx, piece.y + direction
            if 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE:
                for p in pieces:
                    if p.x == new_x and p.y == new_y and not p.captured and p.color != piece.color:
                        moves.append((new_x, new_y))
    
    # Rook moves
    elif piece.type == 'rook':
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            for i in range(1, BOARD_SIZE):
                new_x, new_y = piece.x + i*dx, piece.y + i*dy
                if 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE:
                    occupied = False
                    for p in pieces:
                        if p.x == new_x and p.y == new_y and not p.captured:
                            occupied = True
                            if p.color != piece.color:
                                moves.append((new_x, new_y))
                            break
                    if not occupied:
                        moves.append((new_x, new_y))
                    else:
                        break
    
    # Knight moves
    elif piece.type == 'knight':
        for dx, dy in [(2, 1), (1, 2), (-1, 2), (-2, 1), 
                      (-2, -1), (-1, -2), (1, -2), (2, -1)]:
            new_x, new_y = piece.x + dx, piece.y + dy
            if 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE:
                friendly_piece = False
                for p in pieces:
                    if p.x == new_x and p.y == new_y and not p.captured and p.color == piece.color:
                        friendly_piece = True
                        break
                if not friendly_piece:
                    moves.append((new_x, new_y))
    
    # Bishop moves
    elif piece.type == 'bishop':
        for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            for i in range(1, BOARD_SIZE):
                new_x, new_y = piece.x + i*dx, piece.y + i*dy
                if 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE:
                    occupied = False
                    for p in pieces:
                        if p.x == new_x and p.y == new_y and not p.captured:
                            occupied = True
                            if p.color != piece.color:
                                moves.append((new_x, new_y))
                            break
                    if not occupied:
                        moves.append((new_x, new_y))
                    else:
                        break
    
    # Queen moves (rook + bishop)
    elif piece.type == 'queen':
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            for i in range(1, BOARD_SIZE):
                new_x, new_y = piece.x + i*dx, piece.y + i*dy
                if 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE:
                    occupied = False
                    for p in pieces:
                        if p.x == new_x and p.y == new_y and not p.captured:
                            occupied = True
                            if p.color != piece.color:
                                moves.append((new_x, new_y))
                            break
                    if not occupied:
                        moves.append((new_x, new_y))
                    else:
                        break
        
        for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            for i in range(1, BOARD_SIZE):
                new_x, new_y = piece.x + i*dx, piece.y + i*dy
                if 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE:
                    occupied = False
                    for p in pieces:
                        if p.x == new_x and p.y == new_y and not p.captured:
                            occupied = True
                            if p.color != piece.color:
                                moves.append((new_x, new_y))
                            break
                    if not occupied:
                        moves.append((new_x, new_y))
                    else:
                        break
    
    # King moves
    elif piece.type == 'king':
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                new_x, new_y = piece.x + dx, piece.y + dy
                if 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE:
                    friendly_piece = False
                    for p in pieces:
                        if p.x == new_x and p.y == new_y and not p.captured and p.color == piece.color:
                            friendly_piece = True
                            break
                    if not friendly_piece:
                        moves.append((new_x, new_y))
    
    return moves

# Initialize board
def initialize_board():
    pieces = []
    # Add pawns
    for x in range(BOARD_SIZE):
        pieces.append(Piece('pawn', WHITE, x, 6))
        pieces.append(Piece('pawn', BLACK, x, 1))
    # Add rooks
    pieces.append(Piece('rook', WHITE, 0, 7))
    pieces.append(Piece('rook', WHITE, 7, 7))
    pieces.append(Piece('rook', BLACK, 0, 0))
    pieces.append(Piece('rook', BLACK, 7, 0))
    # Add knights
    pieces.append(Piece('knight', WHITE, 1, 7))
    pieces.append(Piece('knight', WHITE, 6, 7))
    pieces.append(Piece('knight', BLACK, 1, 0))
    pieces.append(Piece('knight', BLACK, 6, 0))
    # Add bishops
    pieces.append(Piece('bishop', WHITE, 2, 7))
    pieces.append(Piece('bishop', WHITE, 5, 7))
    pieces.append(Piece('bishop', BLACK, 2, 0))
    pieces.append(Piece('bishop', BLACK, 5, 0))
    # Add queens
    pieces.append(Piece('queen', WHITE, 3, 7))
    pieces.append(Piece('queen', BLACK, 3, 0))
    # Add kings
    pieces.append(Piece('king', WHITE, 4, 7))
    pieces.append(Piece('king', BLACK, 4, 0))
    return pieces

# Main game variables
pieces = initialize_board()
selected_piece = None
possible_moves = []
current_turn = WHITE
game_over = False

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = pygame.mouse.get_pos()
            board_x, board_y = x // SQUARE_SIZE, y // SQUARE_SIZE
            
            if selected_piece:
                if (board_x, board_y) in possible_moves:
                    target_piece = None
                    for piece in pieces:
                        if piece.x == board_x and piece.y == board_y and not piece.captured and piece != selected_piece:
                            target_piece = piece
                            break
                    
                    if target_piece and target_piece.color != selected_piece.color:
                        target_piece.capture()
                    
                    selected_piece.move_to(board_x, board_y)
                    current_turn = BLACK if current_turn == WHITE else WHITE
                
                selected_piece = None
                possible_moves = []
            else:
                for piece in pieces:
                    if (piece.x == board_x and piece.y == board_y and 
                        not piece.captured and piece.color == current_turn):
                        selected_piece = piece
                        possible_moves = get_possible_moves(piece, pieces)
                        break
    
    # Draw everything
    draw_board(screen)
    draw_highlights(screen, possible_moves, selected_piece)
    
    # Draw pieces
    for piece in sorted(pieces, key=lambda p: p.captured):
        piece.draw(screen)
    
    # Draw turn indicator
    font = pygame.font.SysFont('Arial', 24)
    turn_text = font.render(f"Turn: {'White' if current_turn == WHITE else 'Black'}", True, BLACK)
    screen.blit(turn_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(FPS)