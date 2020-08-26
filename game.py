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

    def game_start():
        game_client.send("START")

    def game_bet():
        game_client.send("BET")

    def game_check():
        game_client.send("CHECK")

    def game_pass():
        game_client.send("PASS")

    def draw_text(text, font, color, surface, x, y):
        x = int(x)
        y = int(y)
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    def calculate_seat_pos(width, height):
        cen_x = width * 0.5
        cen_y = height * 0.45
        dx = cen_x * 0.75
        dy = cen_y * 0.75
        dx1 = dx * 0.65
        dy1 = dy * 0.75

        seats_pos = {
            0: [cen_x - dx, cen_y],
            1: [cen_x - dx1, cen_y + dy1],
            2: [cen_x, cen_y + dy],
            3: [cen_x + dx1, cen_y + dy1],
            4: [cen_x + dx, cen_y],
            5: [cen_x + dx1, cen_y - dy1],
            6: [cen_x, cen_y - dy],
            7: [cen_x - dx1, cen_y - dy1]
        }

        pot_pos = {}
        for seat in seat_pos:
            pot_x = x + ((((x - 800) ** 2 + (y - 405) ** 2) ** 0.5) * 0.4 / (
                (x - 800) ** 2 + (y - 405) ** 2) ** 0.5) * (800 - x)
            pot_y = y + ((((x - 800) ** 2 + (y - 405) ** 2) ** 0.5) * 0.4 / (
                (x - 800) ** 2 + (y - 405) ** 2) ** 0.5) * (405 - y)
            pot_pos[seat] = [pot_x, pot_y]

        return seats_pos, pot_pos

    def create_button(buttons,text, pos, size, color):
        x, y = pos
        x, y = int(x), int(y)
        w, h = size
        w, h = int(w), int(h)
        buttons[text] = pygame.Rect(x, y, w, h)
        pygame.draw.rect(screen, color, buttons[text])
        draw_text(text, font, (0, 0, 0), screen, int(x + 0.5 * w), int(y + 0.5 * h))
        return buttons


    def table_view():
        click = False
        play = True
        while play:
            buttons = {}
            board, player = game_client.update()

            screen.fill(GREEN)
            mx, my = pygame.mouse.get_pos()
            #### BUTTONS #####

            ## STAND UP BUTTON
            buttons = create_button(buttons, "STAND UP", (width - width * 0.07, height - height * 0.1),
                                    (width * 0.06, height * 0.04), WHITE)
            if buttons["STAND UP"].collidepoint(mx, my) and click:
                stand_up(player.seat)
            ## START GAME
            if board.active_players > 1 and not board.game_status:
                buttons = create_button(buttons, "START GAME", (width - width * 0.07, height - height * 0.15),
                                        (width * 0.06, height * 0.04), WHITE)
                if buttons["START GAME"].collidepoint(mx, my) and click:
                    game_start()

            ## TEST DEAL CARDS
            if board.game_status:
                buttons = create_button(buttons, "DEALCARDS", (width - width * 0.07, height - height * 0.2),
                                        (width * 0.06, height * 0.04), WHITE)
                if buttons["DEALCARDS"].collidepoint(mx, my) and click:
                    game_client.send("DEALCARDS")

            ## BOARD DISPLAYING BOARD CARDS AND POT
            if board.game_status and board.cards:
                card_x, card_y = 600, 388
                draw_text(str(board.pot) + " $", font, BLACK, screen,  card_x, card_y + 120)
                for dis, card in enumerate(board.cards):
                    board_card_image = pygame.image.load("PNG/"+card+"_60.png")
                    screen.blit(board_card_image, (card_x + 100 * dis, card_y))

            ## QUIT BUTTON
            quit_game_button = pygame.Rect(1500, 100, 80, 40)
            if quit_game_button.collidepoint(mx, my) and click:
                quit()
            pygame.draw.rect(screen, WHITE, quit_game_button)
            draw_text("QUIT", font, BLACK, screen, 1540, 120)

            ## BET RECT
            betting_rect = pygame.Rect(int(width - width * 0.37), int(height - height * 0.22),
                                       int(width * 0.18), int(height * 0.2))
            pygame.draw.rect(screen, GREY, betting_rect)




            ## BETTING SILDER
            slider_start_x = int(width - width * 0.36)
            slider_start_y = int(height - height * 0.1)
            slider_width = int(width * 0.16)
            slider_height = int(height * 0.005)
            slider_end_x = slider_start_x + slider_width
            slider_range = slider_end_x - slider_start_x
            slider_rect = pygame.Rect(slider_start_x, slider_start_y,
                                      slider_width, slider_height)
            slider_rect.center = int(slider_start_x + slider_width * 0.5), slider_start_y
            slider_rect_hitbox = pygame.Rect(slider_start_x,slider_start_y,
                                             slider_width+10, slider_height + 25)
            slider_rect_hitbox.center = int(slider_start_x + slider_width * 0.5), slider_start_y
            pygame.draw.rect(screen, BLACK, slider_rect)
            if slider_rect_hitbox.collidepoint(mx, my) and click:
                dot_x = round(mx,0)
                if dot_x < slider_start_x:
                    dot_x = slider_start_x
                if dot_x > slider_end_x:
                    dot_x = slider_end_x
                bet_size = round(player.money * ((dot_x - slider_start_x) / slider_range), 1)

            if "dot_x" not in locals() or "dot_y" not in locals():
                dot_x, dot_y = int(slider_start_x), int(slider_start_y)
            pygame.draw.circle(screen, RED, (dot_x, dot_y), 7)
            ## BET SIZE
            bet_size = round(player.money * ((dot_x - slider_start_x) / slider_range), 1)
            if bet_size < 0 or "bet_size" not in locals():
                bet_size = 0
            draw_text(str(bet_size)+" $", font, BLACK, screen, width - width * 0.34, height - height * 0.13)



            ## BET BUTTON
            buttons = create_button(buttons, "BET",(width - width * 0.35, height - height * 0.2),
                                    (width / 25, height / 25), WHITE)
            if buttons["BET"].collidepoint(mx, my) and click:
                game_bet()
            ## PASS BUTTON
            buttons = create_button(buttons, "CHECK", (width - width * 0.30, height - height * 0.2),
                                    (width / 25, height / 25), WHITE)
            if buttons["CHECK"].collidepoint(mx, my) and click:
                game_check()
            ## CHECK BUTTON
            buttons = create_button(buttons, "PASS", (width - width * 0.25, height - height * 0.2),
                                    (width / 25, height / 25), WHITE)
            if buttons["PASS"].collidepoint(mx, my) and click:
                game_pass()




            ## DISPLAYING SEATS, PLAYER CARDS, DEALER CHIP
            for seat_number, seat in board.seats.items():
                x, y = seats_pos[seat_number]
                x, y = int(x), int(y)
                seat_image = pygame.image.load("PNG/emptyseat.png")
                dx, dy = seat_image.get_rect().size
                seat_image_rect = seat_image.get_rect()
                seat_image_rect.center = x, y
                card_dy = -10
                if x > width / 2:
                    deal_dx = 35
                    card_dx = -65
                else:
                    deal_dx = -35
                    card_dx = 65

                if y > height / 2:
                    deal_dy = -35
                    card_dy = -50
                else:
                    deal_dy = 35
                    card_dy = 50
                if board.game_status and seat_number == board.dealer_pos:
                    deal_image = pygame.image.load("PNG/dealerchip3.png")
                    deal_image_rect = deal_image.get_rect()
                    deal_image_rect.center = x + deal_dx, y + deal_dy
                    screen.blit(deal_image, deal_image_rect)
                if seat.state:
                    if board.game_status:
                        if seat.state["id"] == player.id:
                            for iter, card in enumerate(player.cards):
                                card_image = pygame.image.load("PNG/" + card + "_60.png")
                                card_image_rect = card_image.get_rect()
                                card_image_rect.center = x + card_dx + 25 * iter, y + card_dy + 25 * iter
                                if board.players_pots[seat.state["id"]] != 0:
                                    draw_text(str(board.players_pots[seat.state["id"]])+" $", font, BLACK, screen,
                                              pot_pos[seat_number][0], pot_pos[seat_number][1])
                                screen.blit(card_image, card_image_rect)
                        else:
                            for iter in range(2):
                                card_back_image = pygame.image.load("PNG/gray_back.png")
                                card_back_image_rect = card_back_image.get_rect()
                                card_back_image_rect.center = x + card_dx + 25 * iter, y + card_dy + 25 * iter
                                screen.blit(card_back_image, card_back_image_rect)
                                if board.players_pots[seat.state["id"]] != 0:
                                    draw_text(str(board.players_pots[seat.state["id"]]) + " $", font, BLACK, screen,
                                              pot_pos[seat_number][0], pot_pos[seat_number][1])
                    screen.blit(seat_image, seat_image_rect)
                    draw_text(seat.state["name"], font, (0, 0, 0), screen, x, y)
                    draw_text(str(seat.state["money"])+" $", font, (0, 0, 0), screen, x, y + deal_dy * (-1))

                else:
                    screen.blit(seat_image, seat_image_rect)
                    draw_text("Empty", font, (0, 0, 0), screen, x, y)
                    if not player.seat:
                        if seat_image_rect.collidepoint(mx, my) and click:
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
    GREY = 192, 192, 192
    BLACK = 0, 0, 0
    RED = 255, 0 , 0

    if ip != "0.0.0.0":
        game_client = GameClient(ip=ip, port=port, client_id=client_id, client_name=nickname)
        player = game_client.login()
        if player:
            pygame.init()
            size = width, height = 1600, 900
            screen = pygame.display.set_mode(size)
            font = pygame.font.SysFont(None, 20)
            seats_pos, pot_pos = calculate_seat_pos(width, height)
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
