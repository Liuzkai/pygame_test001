import pygame
import random

# 初始化Pygame
pygame.init()

# 游戏窗口设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("21点游戏")

# 颜色定义
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# 卡牌类（添加点数计算）
class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.width = 60
        self.height = 90
        self.face_up = True
        self.x = 0
        self.y = 0

        # 设置卡牌点数
        if value in ["J", "Q", "K"]:
            self.point = 10
        elif value == "A":
            self.point = 11  # 初始按11计算，后续会调整
        else:
            self.point = int(value)

    def draw(self, surface):
        card_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA) # 创建一个带alpha通道的表面
        if self.face_up:
            card_surface.fill(WHITE)
            font = pygame.font.Font(pygame.font.match_font('arial'), 24)
            text_color = RED if self.suit in ["♥", "♦"] else BLACK
            text = font.render(f"{self.value}{self.suit}", True, text_color)
            card_surface.blit(text, (5, 5))
            pygame.draw.rect(card_surface, BLACK, (0, 0, self.width, self.height), 2)
        else:
            pygame.draw.rect(card_surface, GREEN, (0, 0, self.width, self.height))
            pygame.draw.rect(card_surface, BLACK, (0, 0, self.width, self.height), 2)
        surface.blit(card_surface, (self.x, self.y))


# 游戏主类（添加21点规则）
class BlackjackGame:
    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.deck = []
        self.player_hand = []
        self.dealer_hand = []
        self.game_state = "betting"  # 游戏状态：betting, player_turn, dealer_turn, game_over
        self.create_deck()
        self.create_buttons()

    def create_buttons(self):
        # 创建操作按钮
        self.buttons = {
            "hit": pygame.Rect(600, 400, 80, 40),
            "stand": pygame.Rect(600, 450, 80, 40),
            "new_game": pygame.Rect(600, 500, 120, 40)
        }

    def create_deck(self):
        suits = ["♠", "♣", "♥", "♦"]
        values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        self.deck = [Card(suit, value) for suit in suits for value in values]
        random.shuffle(self.deck)

    def calculate_hand_value(self, hand):
        # 计算手牌点数（处理A的特殊情况）
        total = sum(card.point for card in hand)
        aces = sum(1 for card in hand if card.value == "A")

        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        return total

    def initial_deal(self):
        # 初始发牌：玩家和庄家各两张牌
        self.player_hand = [self.deck.pop() for _ in range(2)]
        self.dealer_hand = [self.deck.pop() for _ in range(2)]

        # 庄家第一张牌隐藏
        self.dealer_hand[0].face_up = True
        self.dealer_hand[1].face_up = False  # 第二张牌开始时隐藏

        # 设置初始位置
        self.arrange_cards(self.player_hand, 100, 400)
        self.arrange_cards(self.dealer_hand, 100, 100)

        self.game_state = "player_turn"

    def arrange_cards(self, hand, start_x, y):
        # 排列卡牌位置
        spacing = 30
        for i, card in enumerate(hand):
            card.x = start_x + i * spacing
            card.y = y

    def player_hit(self):
        # 玩家要牌
        if self.game_state == "player_turn":
            new_card = self.deck.pop()
            new_card.face_up = True
            self.player_hand.append(new_card)
            self.arrange_cards(self.player_hand, 100, 400)

            # 检查是否爆牌
            if self.calculate_hand_value(self.player_hand) > 21:
                self.game_state = "game_over"

    def dealer_turn(self):
        # 庄家回合
        self.game_state = "dealer_turn"
        self.dealer_hand[1].face_up = True  # 显示隐藏的牌

        # 庄家要牌直到点数>=17
        while self.calculate_hand_value(self.dealer_hand) < 17:
            new_card = self.deck.pop()
            new_card.face_up = True
            self.dealer_hand.append(new_card)
            self.arrange_cards(self.dealer_hand, 100, 100)

        self.game_state = "game_over"

    def check_winner(self):
        # 判断胜负
        player_value = self.calculate_hand_value(self.player_hand)
        dealer_value = self.calculate_hand_value(self.dealer_hand)

        if player_value > 21:
            return f"Dealer Win! Player Bust"
        if dealer_value > 21:
            return f"Player Win! Dealer Bust"
        if player_value > dealer_value:
            return f"Player Win! "
        if dealer_value > player_value:
            return f"Dealer Win!"
        return f"Push!"

    def draw_info(self):
        # 绘制游戏信息
        font = pygame.font.Font(pygame.font.match_font('arial'), 36)

        # 显示玩家点数
        player_value = self.calculate_hand_value(self.player_hand)
        text = font.render(f"Player: {player_value}", True, BLACK)
        screen.blit(text, (600, 200))

        # 显示庄家点数（游戏结束时显示全部）
        dealer_value = self.calculate_hand_value(self.dealer_hand)
        if self.game_state == "game_over":
            text = font.render(f"Dealer:{dealer_value}", True, BLACK)
        else:
            text = font.render(f"Dealer:?", True, BLACK)
        screen.blit(text, (600, 250))

        # 绘制操作按钮
        self.draw_button("Hit", self.buttons["hit"], BLUE)
        self.draw_button("Stand", self.buttons["stand"], BLUE)
        self.draw_button("New Game", self.buttons["new_game"], GREEN)

        # 显示游戏结果
        if self.game_state == "game_over":
            result = self.check_winner()
            text = font.render(result, True, RED)
            screen.blit(text, (250, 300))

    def draw_button(self, text, rect, color):
        pygame.draw.rect(screen, color, rect)
        font = pygame.font.Font(pygame.font.match_font('arial'), 24)
        text_surf = font.render(text, True, WHITE)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

    def handle_events(self): # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # 处理按钮点击
                if self.buttons["hit"].collidepoint(pos) and self.game_state == "player_turn":
                    self.player_hit()
                elif self.buttons["stand"].collidepoint(pos) and self.game_state == "player_turn":
                    self.dealer_turn()
                elif self.buttons["new_game"].collidepoint(pos):
                    self.__init__()  # 重置游戏
                    self.initial_deal()

    def draw(self):
        screen.fill(GREEN)

        # 绘制庄家手牌
        for card in self.dealer_hand:
            card.draw(screen)

        # 绘制玩家手牌
        for card in self.player_hand:
            card.draw(screen)

        self.draw_info()
        pygame.display.flip()

    def run(self):
        self.initial_deal()  # 开始游戏时自动发牌
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)
        pygame.quit()


# 运行游戏
if __name__ == "__main__":
    game = BlackjackGame()
    game.run()