import pygame
from gamenetwork import *


def main_game(nickname, ip, port, client_id):

    def take_a_seat(seat_id):
        game_client.send("SIT")
        game_client.send(seat_id)

    def stand_up(seat):
        if seat:
            game_client.send("STANDUP")

    def seat_back():
        game_client.send("SEATBACK")

    def game_start():
        game_client.send("START")

    def game_bet(bet_size):
        if bet_size > 0:
            bet_size = round(bet_size, 1)
            game_client.send("BET")
            game_client.send(bet_size)

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
            7: [cen_x - dx1, cen_y + dy1],
            6: [cen_x, cen_y + dy],
            5: [cen_x + dx1, cen_y + dy1],
            4: [cen_x + dx, cen_y],
            3: [cen_x + dx1, cen_y - dy1],
            2: [cen_x, cen_y - dy],
            1: [cen_x - dx1, cen_y - dy1]
        }

        pot_pos = {}
        for pos, seat in seats_pos.items():
            pot_x = seat[0] + 0.4 * (cen_x - seat[0])
            pot_y = seat[1] + 0.4 * (cen_y - seat[1])
            pot_pos[pos] = [pot_x, pot_y]

        slider_pos = {}
        slider_pos['start_x'] = int(width - width * 0.36)
        slider_pos['start_y'] = int(height - height * 0.1)
        slider_pos['width'] = int(width * 0.16)
        slider_pos['height'] = int(height * 0.005)
        slider_pos['end_x'] = slider_pos['start_x'] + slider_pos['width']
        slider_pos['range'] = slider_pos['end_x'] - slider_pos['start_x']
        slider_pos['cen_x'] = int(slider_pos['start_x'] + slider_pos['width'] * 0.5)
        slider_pos['cen_y'] = slider_pos['start_y']

        buttons_pos = {}
        buttons_pos['start_x'] = width - width * 0.07
        buttons_pos['start_y'] = height - height * 0.15
        buttons_pos['start_width'] = width * 0.06
        buttons_pos['start_height'] = height * 0.04
        buttons_pos['stand_height'] = height - height * 0.1

        buttons_pos['bet_rect_x'] = int(width - width * 0.37)
        buttons_pos['bet_rect_y'] = int(height - height * 0.22)
        buttons_pos['bet_rect_width'] = int(width * 0.18)
        buttons_pos['bet_rect_height'] = int(height * 0.2)
        buttons_pos['bet_x'] = width - width * 0.35
        buttons_pos['bet_y'] = height - height * 0.2
        buttons_pos['width'] = width / 25
        buttons_pos['height'] = height / 25
        buttons_pos['check_x'] = width - width * 0.30
        buttons_pos['check_y'] = height - height * 0.2
        buttons_pos['pass_x'] = width - width * 0.25
        buttons_pos['pass_y'] = height - height * 0.2

        return seats_pos, pot_pos, slider_pos, buttons_pos

    def create_button(buttons, text, pos, size, color):
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

            # BUTTONS
            # STAND UP BUTTON
            if player.seat and not player.stand_up_queue:
                buttons = create_button(buttons, "STAND UP", (buttons_pos['start_x'], buttons_pos['stand_height']),
                                        (buttons_pos['start_width'], buttons_pos['start_height']), WHITE)
                if buttons["STAND UP"].collidepoint(mx, my) and click:
                    stand_up(player.seat)

            if player.stand_up_queue:
                buttons = create_button(buttons, "SEATBACK", (buttons_pos['start_x'], buttons_pos['stand_height']),
                                        (buttons_pos['start_width'], buttons_pos['start_height']), WHITE)
                if buttons["SEATBACK"].collidepoint(mx, my) and click:
                    seat_back()
            # START GAME
            if board.seating_players > 1 and not board.game_status:
                buttons = create_button(buttons, "START GAME", (buttons_pos['start_x'], buttons_pos['start_y']),
                                        (buttons_pos['start_width'], buttons_pos['start_height']), WHITE)
                if buttons["START GAME"].collidepoint(mx, my) and click:
                    game_start()

            # BOARD DISPLAYING BOARD CARDS AND POT
            if board.game_status and board.cards:
                card_x, card_y = 600, 388
                draw_text(str(board.pot) + " $", font, BLACK, screen,  width * 0.5, card_y + 160)
                for dis, card in enumerate(board.cards):
                    board_card_image = pygame.image.load("PNG/"+card+"_60.png")
                    screen.blit(board_card_image, (card_x + 100 * dis, card_y))

            # QUIT BUTTON
            quit_game_button = pygame.Rect(1500, 100, 80, 40)
            if quit_game_button.collidepoint(mx, my) and click:
                quit()
            pygame.draw.rect(screen, WHITE, quit_game_button)
            draw_text("QUIT", font, BLACK, screen, 1540, 120)

            if player.stand_up_queue:
                draw_text("You're going to stand up after this hand", font, BLACK, screen, width/2, height/100)
            # PLAYER MONEY
            draw_text(f'{player.name}: {player.money} $', font, BLACK, screen, 45, 20)

            if player.seat:
                # BET RECT
                betting_rect = pygame.Rect(buttons_pos['bet_rect_x'], buttons_pos['bet_rect_y'],
                                           buttons_pos['bet_rect_width'], buttons_pos['bet_rect_height'])
                pygame.draw.rect(screen, GREY, betting_rect)

                # BETTING SILDER
                slider_rect = pygame.Rect(slider_pos['start_x'], slider_pos['start_y'],
                                          slider_pos['width'], slider_pos['height'])
                slider_rect.center = slider_pos['cen_x'], slider_pos['cen_y']
                slider_rect_hitbox = pygame.Rect(slider_pos['start_x'], slider_pos['start_y'],
                                                 slider_pos['width'] + 10, slider_pos['height'] + 25)
                slider_rect_hitbox.center = slider_pos['cen_x'], slider_pos['start_y']
                pygame.draw.rect(screen, BLACK, slider_rect)
                if slider_rect_hitbox.collidepoint(mx, my) and click:
                    dot_x = round(mx, 0)
                    if dot_x < slider_pos['start_x']:
                        dot_x = slider_pos['start_x']
                    if dot_x > slider_pos['end_x']:
                        dot_x = slider_pos['end_x']
                if "dot_x" not in locals() or "dot_y" not in locals():
                    dot_x, dot_y = slider_pos['start_x'], slider_pos['start_y']
                pygame.draw.circle(screen, RED, (dot_x, dot_y), 7)

                # BET SIZE
                if board.check_size >= board.board_player_money[player.seat.id]:
                    bet_size = board.board_player_money[player.seat.id]
                else:
                    if player.id in board.players_pots:
                        bet_size = (board.check_size - board.players_pots[player.id]) + \
                                   round((board.board_player_money[player.seat.id] -
                                          (board.check_size - board.players_pots[player.id])) *
                                         ((dot_x - slider_pos['start_x']) / slider_pos['range']), 1)
                    else:
                        bet_size = board.check_size + round((board.board_player_money[player.seat.id] -
                                                             board.check_size) *
                            ((dot_x - slider_pos['start_x']) / slider_pos['range']), 1)

                if bet_size < 0 or "bet_size" not in locals():
                    bet_size = 0
                bet_size = round(bet_size, 1)
                draw_text(str(bet_size)+" $", font, BLACK, screen, width - width * 0.34, height - height * 0.13)

                # BET BUTTON
                buttons = create_button(buttons, "BET", (buttons_pos['bet_x'], buttons_pos['bet_y']),
                                        (buttons_pos['width'], buttons_pos['height']), WHITE)
                if buttons["BET"].collidepoint(mx, my) and click:
                    game_bet(bet_size)
                # PASS BUTTON
                buttons = create_button(buttons, "CHECK", (buttons_pos['check_x'], buttons_pos['check_y']),
                                        (buttons_pos['width'], buttons_pos['height']), WHITE)
                if buttons["CHECK"].collidepoint(mx, my) and click:
                    game_check()
                # CHECK BUTTON
                buttons = create_button(buttons, "PASS", (buttons_pos['pass_x'], buttons_pos['pass_y']),
                                        (buttons_pos['width'], buttons_pos['height']), WHITE)
                if buttons["PASS"].collidepoint(mx, my) and click:
                    game_pass()

            # DISPLAYING SEATS, PLAYER CARDS, DEALER CHIP
            for seat_id, seat in board.seats.items():
                x, y = seats_pos[seat_id]
                x, y = int(x), int(y)
                if seat_id == board.moving_player_seat_id:
                    seat_image = pygame.image.load("PNG/emptyseatmove.png")
                else:
                    seat_image = pygame.image.load("PNG/emptyseat.png")
                dx, dy = seat_image.get_rect().size
                seat_image_rect = seat_image.get_rect()
                seat_image_rect.center = x, y
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
                if board.game_status and seat_id == board.dealer_pos:
                    deal_image = pygame.image.load("PNG/dealerchip3.png")
                    deal_image_rect = deal_image.get_rect()
                    deal_image_rect.center = x + deal_dx, y + deal_dy
                    screen.blit(deal_image, deal_image_rect)
                if seat.state:
                    if board.game_status:
                        if seat.state["id"] == player.id:
                            for i, card in enumerate(player.cards):
                                if board.players_status[seat_id]:
                                    card_image = pygame.image.load("PNG/" + card + "_60.png")
                                    card_image_rect = card_image.get_rect()
                                    card_image_rect.center = x + card_dx + 25 * i, y + card_dy + 25 * i
                                    if board.players_pots[seat.state["id"]] != 0:
                                        draw_text(str(board.players_pots[seat.state["id"]])+" $", font, BLACK, screen,
                                                  pot_pos[seat_id][0], pot_pos[seat_id][1])
                                    screen.blit(card_image, card_image_rect)
                                else:
                                    card_image = pygame.image.load("PNG/gray_back.png")
                                    card_image_rect = card_image.get_rect()
                                    card_image_rect.center = x + card_dx + 25 * i, y + card_dy + 25 * i
                                    if board.players_pots[seat.state["id"]] != 0:
                                        draw_text(str(board.players_pots[seat.state["id"]]) + " $", font, BLACK, screen,
                                                  pot_pos[seat_id][0], pot_pos[seat_id][1])
                                    if card_image_rect.collidepoint(mx, my):
                                        card_image = pygame.image.load("PNG/" + card + "_60.png")
                                    screen.blit(card_image, card_image_rect)
                        else:
                            for i in range(2):
                                if board.post_game:
                                    if board.players_status[seat_id]:
                                        card_back_image = pygame.image.load("PNG/" +
                                                                            board.players_post_game_cards[seat_id][i] +
                                                                            "_60.png")
                                else:
                                    card_back_image = pygame.image.load("PNG/gray_back.png")
                                if board.players_status[seat_id]:
                                    card_back_image_rect = card_back_image.get_rect()
                                    card_back_image_rect.center = x + card_dx + 25 * i, y + card_dy + 25 * i
                                    screen.blit(card_back_image, card_back_image_rect)
                                if board.players_pots:
                                    if seat.state["id"] in board.players_pots:
                                        if board.players_pots[seat.state["id"]] != 0:
                                            draw_text(str(board.players_pots[seat.state["id"]]) + " $", font, BLACK,
                                                      screen, pot_pos[seat_id][0], pot_pos[seat_id][1])
                    screen.blit(seat_image, seat_image_rect)
                    if seat == player.seat:
                        draw_text(seat.state["name"] + str(seat.id), font, RED, screen, x, y)
                    else:
                        if board.players_status[seat_id]:
                            draw_text(seat.state["name"] + str(seat.id), font, (0, 0, 0), screen, x, y)
                        else:
                            draw_text(seat.state["name"] + str(seat.id), font, (192, 192, 192), screen, x, y)
                    draw_text(str(board.board_player_money[seat.id])+" $", font, (0, 0, 0),
                              screen, x, y + deal_dy * (-1))

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

    # COLORS
    WHITE = 255, 255, 255
    GREEN = 0, 200, 0
    GREY = 192, 192, 192
    BLACK = 0, 0, 0
    RED = 255, 0, 0

    game_client = GameClient(ip=ip, port=port, client_id=client_id, client_name=nickname)
    player = game_client.login()
    if player:
        pygame.init()
        size = width, height = 1600, 900
        screen = pygame.display.set_mode(size)
        font = pygame.font.SysFont(None, 20)
        seats_pos, pot_pos, slider_pos, buttons_pos = calculate_seat_pos(width, height)
        table_view()
    else:
        print("Client already connected")
        game_client.disconnect()



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
