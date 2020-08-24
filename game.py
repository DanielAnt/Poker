import pygame
from player import *
from board import *
from gamenetwork import *


def main_game(nickname, ip, port, client_id):

    def take_a_seat(seat_id):
        game_client.send("SIT")
        game_client.send(seat_id)

    def stand_up(seat):
        if seat:
            game_client.send("STANDUP")

    def start_game():
        game_client.send("START")

    def draw_text(text, font, color, surface, x, y):
        x = int(x)
        y = int(y)
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    def table_view():
        click = False
        play = True
        while play:
            board, player = game_client.update()

            screen.fill(GREEN)
            mx, my = pygame.mouse.get_pos()
            #### BUTTONS #####
            stand_up_button = pygame.Rect(1500, 800, 80, 40)
            if stand_up_button.collidepoint(mx, my) and click:
                stand_up(player.seat)
            pygame.draw.rect(screen, (255, 255, 255), stand_up_button)
            draw_text("Stand Up", font, (0, 0, 0), screen, 1540, 820)

            if board.active_players > 1 and not board.game_status:
                start_game_button = pygame.Rect(1500, 700, 80, 40)
                if start_game_button.collidepoint(mx, my) and click:
                    start_game()
                pygame.draw.rect(screen, (255, 255, 255), start_game_button)
                draw_text("Start Game", font, (0, 0, 0), screen, 1540, 720)

            if board.game_status:
                deal_cards_button = pygame.Rect(1500, 600, 80, 40)
                if deal_cards_button.collidepoint(mx, my) and click:
                    game_client.send("DEALCARDS")
                pygame.draw.rect(screen, (255, 255, 255), deal_cards_button)
                draw_text("deal cards", font, (0, 0, 0), screen, 1540, 620)

            if board.cards:
                card_x, card_y = 600, 388
                for dis, card in enumerate(board.cards):
                    board_card_image = pygame.image.load("PNG/"+card+".png")
                    screen.blit(board_card_image, (card_x + 100 * dis, card_y))

            quit_game_button = pygame.Rect(1500, 100, 80, 40)
            if quit_game_button.collidepoint(mx, my) and click:
                quit()
            pygame.draw.rect(screen, (255, 255, 255), quit_game_button)
            draw_text("QUIT", font, (0, 0, 0), screen, 1540, 120)

            for seat_number, seat in board.seats.items():
                x, y = seat.cords
                seat_image = pygame.image.load("PNG/emptyseat.png")
                dx, dy = seat_image.get_rect().size
                if x > width / 2:
                    deal_dx = -50
                else:
                    deal_dx = 50
                if y > height / 2:
                    deal_dy = -50
                else:
                    deal_dy = 50
                if board.game_status and seat_number == board.dealer_pos:
                    deal_image = pygame.image.load("PNG/dealerchip3.png")
                    screen.blit(deal_image, (x + deal_dx, y + deal_dy))
                if seat.state:
                    if board.game_status:
                        if seat.state == player:
                            for iter, card in enumerate(player.cards):
                                card_image = pygame.image.load("PNG/" + card + ".png")
                                screen.blit(card_image, (x + (deal_dx * 3) * iter, y + (deal_dy * 2)))
                        else:
                            for iter in range(2):
                                card_image = pygame.image.load("PNG/gray_back.png")
                                screen.blit(card_image, (x + (deal_dx) * iter * 2, y + (deal_dy * 2)))
                    screen.blit(seat_image, (x, y))
                    draw_text(seat.state.name, font, (0, 0, 0), screen, x+dx/2, y+dy/2)
                else:
                    screen.blit(seat_image, (x, y))
                    draw_text("Empty", font, (0, 0, 0), screen, x+dx/2, y+dy/2)
                    if not player.seat:
                        if pygame.Rect(x, y, dx, dy).collidepoint(mx, my) and click:
                            take_a_seat(seat.id)

            click = False
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                    game_client.send("bye")
                    game_client.disconnect()
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

    ## COLORS ##
    WHITE = 255, 255, 255
    GREEN = 0, 200, 0

    if ip != "0.0.0.0":
        game_client = GameClient(ip=ip, port=port, client_id=client_id, client_name=nickname)
        player = game_client.login()
        if player:
            pygame.init()
            size = width, height = 1600, 900
            screen = pygame.display.set_mode(size)
            font = pygame.font.SysFont(None, 20)
            table_view()
        else:
            print("Client already connected")
            game_client.disconnect()
    else:
        board = Board(100, "test", 10, 10, 1)
        player = Player(100, "Andy", 100)


if __name__ == '__main__':

    val = input("chose player:")
    if int(val) == 1:
        main_game("BOY", "192.168.1.132", 16001, 10123)
    elif int(val) == 2:
        main_game("JACK", "192.168.1.132", 16001, 10054)
    elif int(val) == 3:
        main_game("TRAY", "192.168.1.132", 16001, 10057)


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
