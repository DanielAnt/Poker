import pygame
from gamenetwork import *


def main_game(nickname, ip, port, client_id):

    def take_a_seat(seat, buy_in_size):
        if not seat.state:
            game_client.send("SIT")
            message = f'{seat.id};{buy_in_size}'
            game_client.send(message)

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
        cen_x = int(width * 0.5)
        cen_y = int(height * 0.45)
        dx = int(cen_x * 0.75)
        dy = int(cen_y * 0.75)
        dx1 = int(dx * 0.65)
        dy1 = int(dy * 0.75)

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

        cards_pos = {}
        dx = int(width / 23)
        dy = int(height / 24)
        dis_x = int(width / 64)
        dis_y = int(height/ 36)
        for pos, seat in seats_pos.items():
            if seat[0] > width / 2:
                if seat[1] > height / 2:
                    cards_pos[pos] =[[seat[0] - dx, seat[1] - dy],
                                     [seat[0] - dx - dis_x, seat[1] - dy - dis_y]]
                else:
                    cards_pos[pos] = [[seat[0] - dx, seat[1] + dy],
                                      [seat[0] - dx - dis_x, seat[1] + dy + dis_y]]
            else:
                if seat[1] > height / 2:
                    cards_pos[pos] = [[seat[0] + dx, seat[1] - dy],
                                      [seat[0] + dx + dis_x, seat[1] - dy + dis_y]]
                else:
                    cards_pos[pos] = [[seat[0] + dx, seat[1] + dy],
                                      [seat[0] + dx + dis_x, seat[1] + dy + dis_y]]

        board_cards_x = cen_x - 200
        board_cards_y = cen_y
        board_cards_pos = {}
        for i in range(5):
            board_cards_pos[i] = board_cards_x + 100 * i, board_cards_y

        slider_pos = {}
        slider_pos['start_x'] = int(width - width * 0.36)
        slider_pos['start_y'] = int(height - height * 0.06)
        slider_pos['width'] = int(width * 0.16)
        slider_pos['height'] = int(height * 0.005)
        slider_pos['end_x'] = slider_pos['start_x'] + slider_pos['width']
        slider_pos['range'] = slider_pos['end_x'] - slider_pos['start_x']
        slider_pos['cen_x'] = int(slider_pos['start_x'] + slider_pos['width'] * 0.5)
        slider_pos['cen_y'] = slider_pos['start_y']

        slider_pos['buyin_cen_x'] = int(cen_x)
        slider_pos['buyin_cen_y'] = int(cen_y)
        slider_pos['buyin_start_x'] = int(slider_pos['buyin_cen_x'] - slider_pos['width'] / 2)
        slider_pos['buyin_end_x'] = int(slider_pos['buyin_cen_x'] + slider_pos['width'] / 2)
        slider_pos['buyin_range'] = int(slider_pos['buyin_end_x'] - slider_pos['buyin_start_x'])

        buttons_pos = {}
        buttons_pos['start_x'] = width - width * 0.07
        buttons_pos['start_y'] = height - height * 0.15
        buttons_pos['start_width'] = width * 0.06
        buttons_pos['start_height'] = height * 0.04
        buttons_pos['stand_height'] = height - height * 0.1

        buttons_pos['bet_rect_x'] = int(width - width * 0.37)
        buttons_pos['bet_rect_y'] = int(height - height * 0.16)
        buttons_pos['bet_rect_width'] = int(width * 0.18)
        buttons_pos['bet_rect_height'] = int(height * 0.15)
        buttons_pos['bet_x'] = int(width - width * 0.35)
        buttons_pos['bet_y'] = int(height - height * 0.14)
        buttons_pos['width'] = int(width / 25)
        buttons_pos['height'] = int(height / 25)
        buttons_pos['check_x'] = int(width - width * 0.30)
        buttons_pos['check_y'] = int(height - height * 0.14)
        buttons_pos['pass_x'] = int(width - width * 0.25)
        buttons_pos['pass_y'] = int(height - height * 0.14)

        buttons_pos["seat_window_x"] = int(cen_x)
        buttons_pos["seat_window_y"] = int(cen_y)
        buttons_pos["seat_window_width"] = int(width / 5)
        buttons_pos["seat_window_height"] = int(height / 5)

        buttons_pos["seat_conf_x"] = int(buttons_pos["seat_window_x"] - (width / 20))
        buttons_pos["seat_conf_y"] = int(buttons_pos["seat_window_y"] + (height / 20))

        buttons_pos["seat_cancel_x"] = int(buttons_pos["seat_window_x"] + (width / 20))
        buttons_pos["seat_cancel_y"] = int(buttons_pos["seat_window_y"] + (height / 20))

        return seats_pos, pot_pos, slider_pos, buttons_pos, cards_pos, board_cards_pos

    def create_button(buttons, text, pos, size, color):
        x, y = pos
        x, y = int(x), int(y)
        w, h = size
        w, h = int(w), int(h)
        buttons[text] = pygame.Rect(x, y, w, h)
        pygame.draw.rect(screen, color, buttons[text])
        draw_text(text, font, (0, 0, 0), screen, int(x + 0.5 * w), int(y + 0.5 * h))
        return buttons

    def create_button_center(buttons, text, pos, size, color):
        x, y = pos
        x, y = int(x), int(y)
        w, h = size
        w, h = int(w), int(h)
        buttons[text] = pygame.Rect(x, y, w, h)
        buttons[text].center = x, y
        pygame.draw.rect(screen, color, buttons[text])
        draw_text(text, font, (0, 0, 0), screen, int(x), int(y))
        return buttons

    def table_view():
        click = False
        show_seat_window = False
        chosen_seat = False
        click_mx = 0
        click_my = 0
        dot_x = int(slider_pos["start_x"])
        dot_y = int(slider_pos["start_y"])
        dot_x2 = int(slider_pos["buyin_start_x"])
        dot_y2 = int(slider_pos["buyin_cen_y"])
        moving_seat_image = pygame.image.load("PNG/emptyseatmove.png")
        moving_seat_image_rect = moving_seat_image.get_rect()
        seat_image = pygame.image.load("PNG/emptyseat.png")
        seat_image_rect = seat_image.get_rect()
        deal_image = pygame.image.load("PNG/dealerchip3.png")
        deal_image_rect = deal_image.get_rect()

        play = True
        while play:
            buttons = {}
            board, player = game_client.update()

            screen.fill(GREEN)
            mx, my = pygame.mouse.get_pos()

            if click:
                click_mx, click_my = mx, my

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
                for i, card in enumerate(board.cards):
                    board_card_image = pygame.image.load("PNG/"+card+"_60.png")
                    board_card_image_rect = board_card_image.get_rect()
                    board_card_image_rect.center = board_cards_pos[i][0], board_cards_pos[i][1]
                    screen.blit(board_card_image, board_card_image_rect)

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
                draw_text(str(bet_size)+" $", font, BLACK, screen, buttons_pos['pass_x'], height - height * 0.03)

                # BET BUTTON
                if player.seat.id in board.players_pots:
                    current_money = board.board_player_money[player.seat.id] - board.players_pots[player.seat.id]
                else:
                    current_money = board.board_player_money[player.seat.id]
                if board.check_size >= current_money:
                    buttons = create_button(buttons, "ALL-IN", (buttons_pos['bet_x'], buttons_pos['bet_y']),
                                            (buttons_pos['width'], buttons_pos['height']), WHITE)
                    if buttons["ALL-IN"].collidepoint(mx, my) and click:
                            game_check()
                else:
                    buttons = create_button(buttons, "BET", (buttons_pos['bet_x'], buttons_pos['bet_y']),
                                            (buttons_pos['width'], buttons_pos['height']), WHITE)
                    if buttons["BET"].collidepoint(mx, my) and click:
                        if bet_size >= board.check_size - board.board_player_money[player.seat.id]:
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
                # SEAT IMAGE
                if seat_id == board.moving_player_seat_id:
                    dx, dy = moving_seat_image.get_rect().size
                    moving_seat_image_rect.center = x, y
                    screen.blit(moving_seat_image, moving_seat_image_rect)
                else:
                    dx, dy = seat_image.get_rect().size
                    seat_image_rect.center = x, y
                    screen.blit(seat_image, seat_image_rect)

                if x > width / 2:
                    deal_dx = 35
                else:
                    deal_dx = -35

                if y > height / 2:
                    deal_dy = -35
                else:
                    deal_dy = 35

                # DEAL CHIP
                if board.game_status and seat_id == board.dealer_pos:
                    deal_image_rect.center = x + deal_dx, y + deal_dy
                    screen.blit(deal_image, deal_image_rect)

                # RENDERING CARDS
                if seat.state:
                    if board.game_status:
                        if seat.state["id"] == player.id:
                            for i, card in enumerate(player.cards):
                                if board.players_status[seat_id]:
                                    card_image = pygame.image.load("PNG/" + card + "_60.png")
                                    card_image_rect = card_image.get_rect()
                                    card_image_rect.center = cards_pos[seat.id][i][0], cards_pos[seat.id][i][1]
                                    screen.blit(card_image, card_image_rect)
                                else:
                                    card_image = pygame.image.load("PNG/gray_back.png")
                                    card_image_rect = card_image.get_rect()
                                    card_image_rect.center = cards_pos[seat.id][i][0], cards_pos[seat.id][i][1]
                                    if card_image_rect.collidepoint(mx, my):
                                        card_image = pygame.image.load("PNG/" + card + "_60.png")
                                    screen.blit(card_image, card_image_rect)
                            if seat.state["id"] in board.players_pots:
                                if board.players_pots[seat.state["id"]] != 0:
                                    draw_text(str(board.players_pots[seat.state["id"]]) + " $", font, BLACK, screen,
                                              pot_pos[seat_id][0], pot_pos[seat_id][1])

                        else:
                            for i in range(2):
                                if board.post_game:
                                    if board.players_status[seat_id]:
                                        card_back_image = pygame.image.load("PNG/" +
                                                                            board.players_post_game_cards[seat_id][i] +
                                                                            "_60.png")
                                        if seat_id in board.prize:
                                            draw_text(f'{round(board.board_player_money[seat_id]-board.prize[seat_id], 1)} $ + {board.prize[seat_id]} $', font, BLACK, screen,
                                                  x, int(y + deal_dy * (-1.5)))
                                else:
                                    card_back_image = pygame.image.load("PNG/gray_back.png")
                                if board.players_status[seat_id]:
                                    card_back_image_rect = card_back_image.get_rect()
                                    card_back_image_rect.center = cards_pos[seat.id][i][0], cards_pos[seat.id][i][1]
                                    screen.blit(card_back_image, card_back_image_rect)
                                if board.players_pots:
                                    if seat.state["id"] in board.players_pots:
                                        if board.players_pots[seat.state["id"]] != 0:
                                            draw_text(f'{board.players_pots[seat.state["id"]]} $', font, BLACK,
                                                      screen, pot_pos[seat_id][0], pot_pos[seat_id][1])
                    if seat == player.seat:
                        draw_text(seat.state["name"], font, RED, screen, x, y)
                    else:
                        if board.players_status[seat_id]:
                            draw_text(seat.state["name"], font, BLACK, screen, x, y)
                        else:
                            draw_text(seat.state["name"], font, GREY, screen, x, y)

                    # PLAYERS MONEY
                    if seat.id not in board.prize:
                        draw_text(f'{board.board_player_money[seat.id]} $', font, BLACK,
                              screen, x, int(y + deal_dy * (-1.5)))
                    else:
                        draw_text(f'{round(board.board_player_money[seat_id] - board.prize[seat_id], 1)}'
                                  f' $ + {board.prize[seat_id]} $',
                                font, BLACK, screen,
                                x, int(y + deal_dy * (-1.5)))

                else:
                    draw_text("Empty", font, GREY, screen, x, y)
                    if not player.seat:
                        if seat_image_rect.collidepoint(mx, my) and click:
                            if not player.seat:
                                show_seat_window = True
                                chosen_seat = seat

            if show_seat_window:
                # BACKGROUND
                seat_window = pygame.Rect(buttons_pos["seat_window_x"], buttons_pos["seat_window_y"],
                                          buttons_pos["seat_window_width"], buttons_pos["seat_window_height"])
                seat_window.center = buttons_pos["seat_window_x"], buttons_pos["seat_window_y"]
                pygame.draw.rect(screen, GREY, seat_window)

                #SLIDER
                buyin_slider_rect = pygame.Rect(0, 0,slider_pos['width'], slider_pos['height'])
                buyin_slider_rect.center = slider_pos['buyin_cen_x'], slider_pos['buyin_cen_y']
                buyin_slider_rect_hitbox = pygame.Rect(slider_pos['buyin_cen_x'], slider_pos['buyin_cen_y'],
                                                 slider_pos['width'] + 25, slider_pos['height'] + 25)
                buyin_slider_rect_hitbox.center = slider_pos['buyin_cen_x'], slider_pos['buyin_cen_y']
                pygame.draw.rect(screen, BLACK, buyin_slider_rect)
                if buyin_slider_rect_hitbox.collidepoint(mx, my) and click:
                    dot_x2 = round(mx, 0)
                    if dot_x2 < slider_pos['buyin_start_x']:
                        dot_x2 = slider_pos['buyin_start_x']
                    if dot_x2 > slider_pos['buyin_end_x']:
                        dot_x2 = slider_pos['buyin_end_x']
                pygame.draw.circle(screen, RED, (dot_x2, dot_y2), 7)
                buy_in_size = float(round(board.min_buy_in + (board.max_buy_in - board.min_buy_in) * ((dot_x2 - slider_pos["buyin_start_x"]) / slider_pos["buyin_range"]), 0))
                draw_text(f'BUY IN: {buy_in_size}$', font, BLACK, screen, slider_pos['buyin_cen_x'], slider_pos['buyin_cen_y'] - 30 )

                # BUTTONS
                buttons = create_button_center(buttons, "ACCEPT",
                                               (buttons_pos["seat_conf_x"], buttons_pos["seat_conf_y"]),
                                               (buttons_pos['width'], buttons_pos['height']), WHITE)

                if buttons["ACCEPT"].collidepoint(mx, my) and click:
                    if chosen_seat:
                        take_a_seat(chosen_seat, buy_in_size)
                        show_seat_window = False

                buttons = create_button_center(buttons, "CANCEL",
                                               (buttons_pos["seat_cancel_x"], buttons_pos["seat_cancel_y"]),
                                               (buttons_pos['width'], buttons_pos['height']), WHITE)

                if buttons["CANCEL"].collidepoint(mx, my) and click:
                    show_seat_window = False
                    chosen_seat = False


            click = False
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                    game_client.send("bye")
                    game_client.disconnect()
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    pass
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
        font_size = int(round(1/80 * width, 0))

        font = pygame.font.SysFont(None, font_size)

        seats_pos, pot_pos, slider_pos, buttons_pos, cards_pos, board_cards_pos = calculate_seat_pos(width, height)
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


