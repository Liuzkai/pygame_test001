import pygame
import random

# 初始化Pygame
pygame.init()

# 游戏窗口设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("卡牌游戏")

# 颜色定义
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


# 卡牌类
class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.width = 60
        self.height = 90
        self.face_up = False
        self.x = 0
        self.y = 0
        self.dragging = False
        self.drag_offset = (0, 0)

    def draw(self, surface):
        # 创建卡牌表面
        card_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        if self.face_up:
            card_surface.fill(WHITE)
            # 绘制花色和数值
            font = pygame.font.Font(None, 24)
            text_color = RED if self.suit in ["♥", "♦"] else BLACK
            text = font.render(f"{self.value}{self.suit}", True, text_color)
            card_surface.blit(text, (5, 5))
            # 绘制卡牌边框
            pygame.draw.rect(card_surface, BLACK, (0, 0, self.width, self.height), 2)
        else:
            # 卡牌背面
            pygame.draw.rect(card_surface, GREEN, (0, 0, self.width, self.height))
            pygame.draw.rect(card_surface, BLACK, (0, 0, self.width, self.height), 2)

        surface.blit(card_surface, (self.x, self.y))

    def is_clicked(self, pos):
        # 检查是否点击了卡牌
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return rect.collidepoint(pos)


# 游戏主类
class CardGame:
    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.deck = []
        self.hand = []
        self.dealing = False
        self.deal_speed = 5
        self.create_deck()

    def create_deck(self):
        # 创建一副标准扑克牌
        suits = ["♠", "♣", "♥", "♦"]
        values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        for suit in suits:
            for value in values:
                card = Card(suit, value)
                card.x = SCREEN_WIDTH // 2 - card.width // 2
                card.y = SCREEN_HEIGHT // 2 - card.height // 2
                self.deck.append(card)
        random.shuffle(self.deck)

    def deal_cards(self):
        # 发牌动画
        if not self.dealing:
            self.dealing = True
            target_x = 100
            for i in range(5):
                if self.deck:
                    card = self.deck.pop()
                    card.face_up = True
                    card.target_pos = (target_x, 300)
                    target_x += 80
                    self.hand.append(card)

    def update(self):
        # 处理发牌动画
        if self.dealing:
            dealing_done = True
            for card in self.hand:
                dx = card.target_pos[0] - card.x
                dy = card.target_pos[1] - card.y
                if abs(dx) > 1:
                    card.x += dx * 0.1
                    dealing_done = False
                if abs(dy) > 1:
                    card.y += dy * 0.1
                    dealing_done = False
            if dealing_done:
                self.dealing = False

    def draw(self):
        screen.fill(GREEN)
        # 绘制手牌
        for card in self.hand:
            card.draw(screen)
        # 绘制牌堆
        if self.deck:
            deck_card = self.deck[-1]
            deck_card.x = 50
            deck_card.y = 50
            deck_card.draw(screen)
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # 检查是否点击了牌堆
                if self.deck and pygame.Rect(50, 50, 60, 90).collidepoint(pos):
                    self.deal_cards()
                # 检查是否点击了手牌
                for card in reversed(self.hand):  # 从最上面的卡牌开始检查
                    if card.is_clicked(pos):
                        card.dragging = True
                        card.drag_offset = (pos[0] - card.x, pos[1] - card.y)
                        # 将被拖动的卡牌移到最上层
                        self.hand.remove(card)
                        self.hand.append(card)
                        break

            elif event.type == pygame.MOUSEBUTTONUP:
                for card in self.hand:
                    card.dragging = False

            elif event.type == pygame.MOUSEMOTION:
                for card in self.hand:
                    if card.dragging:
                        pos = pygame.mouse.get_pos()
                        card.x = pos[0] - card.drag_offset[0]
                        card.y = pos[1] - card.drag_offset[1]

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()


# 运行游戏
if __name__ == "__main__":
    game = CardGame()
    game.run()