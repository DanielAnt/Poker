import sys, pygame
from player import *
from board import *
from cards import *

board = Board(100, "test", 10, 10, 1)
player = Player()


## COLORS ##
WHITE = 255, 255, 255
GREEN = 0, 200, 0

pygame.init()
size = width, height = 1600, 900
screen = pygame.display.set_mode(size)
click = False

font = pygame.font.SysFont(None, 20)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)




def game():
    while True:

        screen.fill(GREEN)
        mx, my = pygame.mouse.get_pos()
        #### BUTTONS #####
        stand_up_button = pygame.Rect(1500, 800, 80, 40)
        if stand_up_button.collidepoint((mx,my)) and click:
            player.stand_up()
        pygame.draw.rect(screen, (255,255,255), stand_up_button)
        draw_text("Stand Up", font, (0, 0, 0), screen, 1540, 820)



        for seat_number, seat in board.seats.items():
            x,y = seat.cords
            seat_image = pygame.image.load("PNG/emptyseat.png")
            dx, dy = seat_image.get_rect().size
            if seat.state:
                screen.blit(seat_image, (x, y))
                draw_text(seat.state.name, font, (0, 0, 0), screen, x+dx/2, y+dy/2)
            else:
                screen.blit(seat_image,(x,y))
                draw_text("Empty", font, (0, 0, 0), screen, x+dx/2, y+dy/2)
                if not player.seat:
                    if pygame.Rect(x, y, dx, dy).collidepoint((mx, my)) and click:
                        seat.sit_down(player)
                        player.sit_down(seat)






        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True



        pygame.display.flip()

game()

"""
playerOne = Player(name = "Bob")
playerTwo = Player(name = "George")
playerThree = Player(name = "Kek")
playerFour = Player(name = "Dan")

board = Board()
board.player_sit(0,playerOne)
board.player_sit(1,playerTwo)
board.player_sit(2,playerThree)
board.player_sit(3,playerFour)

deck = Cards()
deck.schuffle()

for _ in range(2):
    for slot,player in board.slots.items():
        if player != None:
            player.get_card(deck.deal_card())




size = width, height = 1600, 900
speed = [2, 2]
green = 0, 128, 0


screen = pygame.display.set_mode(size)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(green)

    for slot, cords in board.slotsCords.items():
        x, y = cords
        for i, card in enumerate(board.slots[slot].cards):
            card = pygame.image.load("PNG/"+card+".png")
            screen.blit(card,(x+(i*135),y))


    pygame.display.flip()


"""















