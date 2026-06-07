import pygame
import random

# --- CONFIGURATION & CONSTANTS ---
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500
PLAYER_SPEED = 350
BULLET_SPEED = 600
ENEMY_SPEED = 180
BIG_ENEMY_SPEED =120
#incase of changing values for testing
# SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500
# PLAYER_SPEED = 350
# BULLET_SPEED = 600
# ENEMY_SPEED = 180
# BIG_ENEMY_SPEED =120



class Player(pygame.sprite.Sprite): # 1. Inherit from Sprite
    def __init__(self):
        super().__init__() # Initialize the parent sprite class
        
        # 2. Load the actual image asset (replace with your file name)
        # .convert_alpha() keeps transparency intact
        self.image = pygame.image.load("assets/images/player_ship.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        
        # Scale the image to match your desired size if needed
        self.image = pygame.transform.scale(self.image, (50, 50)) 
        
        # 3. Create the rect and position it
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # Keep your radius for collisions!
        self.radius = 20
        self.health = 3
        
    # Quick helper property to easily grab the position as a Vector2
    @property
    def pos(self):
        return pygame.Vector2(self.rect.center)

    def move(self, dt, keys):
        # Create a temporary Vector2 to handle float precision movement
        new_pos = self.pos
        if keys[pygame.K_w]: new_pos.y -= PLAYER_SPEED * dt
        if keys[pygame.K_s]: new_pos.y += PLAYER_SPEED * dt
        if keys[pygame.K_a]: new_pos.x -= PLAYER_SPEED * dt
        if keys[pygame.K_d]: new_pos.x += PLAYER_SPEED * dt
        
        # Borders
        new_pos.x = max(0, min(SCREEN_WIDTH, new_pos.x))
        new_pos.y = max(0, min(SCREEN_HEIGHT, new_pos.y))
        
        # Apply new coordinates back to the rect
        self.rect.center = (new_pos.x, new_pos.y)

    def draw(self, screen):
        # Sprites are drawn using the image and rect
        screen.blit(self.image, self.rect)

class Bullet:
    def __init__(self, x, y, direction):
        self.pos = pygame.Vector2(x, y)
        self.direction = direction # 1 for Right, -1 for Left
        self.radius = 3

    def update(self, dt):
        self.pos.x += (BULLET_SPEED * self.direction) * dt

    def is_offscreen(self):
        return self.pos.x < 0 or self.pos.x > SCREEN_WIDTH

    def draw(self, screen):
        pygame.draw.circle(screen, 'white', self.pos, self.radius)

class Enemy:
    def __init__(self, player_pos, is_big=False):
        self.is_big = is_big
        self.radius = 15 if is_big else 8
        self.health = 3 if is_big else 1
        self.speed = BIG_ENEMY_SPEED if is_big else ENEMY_SPEED
        self.color = 'blue' if is_big else 'red'
        self.pos = self._get_valid_spawn(player_pos)

    def _get_valid_spawn(self, player_pos):
        # Logic to spawn away from player
        while True:
            pos = pygame.Vector2(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
            if pos.distance_to(player_pos) > 150:
                return pos

    def update(self, player_pos, dt):
        direction = (player_pos - self.pos)
        if direction.length() != 0:
            self.pos += direction.normalize() * self.speed * dt

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)

    

class PickUp:
    def __init__(self):
        self.radius=15
        self.color='green'
        self.posx=random.randint(0,SCREEN_WIDTH)
        self.posy=random.randint(0,SCREEN_HEIGHT)
        self.pos=pygame.Vector2(self.posx, self.posy)
        self.picked_up=False



    def on_player_contact(self,player):
        if self.pos.distance_to(player.pos)<35:
            self.picked_up=True
            player.health+=1
            
    def draw(self,screen):
        if not self.picked_up:
            pygame.draw.circle(screen,self.color,self.pos,self.radius)


        

        

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 25)
        self.game_over_font = pygame.font.Font(None, 74)
    
        # Audio
        song=random.choice(['assets/sound/hellraiser.mp3','assets/sound/war_pigs.mp3'])
        self.bullet_sfx = pygame.mixer.Sound('assets/sound/bullet_sound.mp3')
        self.bullet_sfx.set_volume(0.9)
        

        pygame.mixer.music.load(song)
        if (song=='war_pigs.mp3'):
            pygame.mixer.music.set_volume(0.5)  
            pygame.mixer.music.play(-1,60.0)
        else:
             pygame.mixer.music.set_volume(0.3)  
             pygame.mixer.music.play(-1,45.0)




        # Game Entities
        self.player = Player()
        self.bullets = []
        self.enemies = []
        self.objects=[]
        
        self.score = 0
        self.slayed = 0
        self.running = True
        self.is_game_over = False

        # Timers
        self.ENEMY_SPAWN = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ENEMY_SPAWN, 1800)
        self.BIG_ENEMY_SPAWN = pygame.USEREVENT + 2
        pygame.time.set_timer(self.BIG_ENEMY_SPAWN, 10000)
        self.HEALTH_PACK=pygame.USEREVENT+3
        pygame.time.set_timer(self.HEALTH_PACK,5000)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.is_game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.reset_game()  # Call our clean reset!
            
            if not self.is_game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bullets.append(Bullet(self.player.pos.x + 20, self.player.pos.y, 1))
                        self.bullet_sfx.play() 
                    if event.key == pygame.K_o:
                        self.bullet_sfx.play() 
                        self.bullets.append(Bullet(self.player.pos.x - 20, self.player.pos.y, -1))

            
                
                if event.type == self.ENEMY_SPAWN:
                    num_to_spawn = random.choice([2, 3, 4])
                    for _ in range(num_to_spawn):
                        self.enemies.append(Enemy(self.player.pos))
                
                if event.type == self.BIG_ENEMY_SPAWN:
                    self.enemies.append(Enemy(self.player.pos, is_big=True))

                if event.type==self.HEALTH_PACK:
                    self.objects.append(PickUp())


    def update(self, dt):
        if self.is_game_over: return

        keys = pygame.key.get_pressed()
        self.player.move(dt, keys)

        # Update Bullets
        for b in self.bullets[:]:
            b.update(dt)
            if b.is_offscreen():
                self.bullets.remove(b)

        # Update Enemies & Collisions
        for e in self.enemies[:]:
            e.update(self.player.pos, dt)

            # Player-Enemy Collision
            if self.player.pos.distance_to(e.pos) < (self.player.radius + e.radius):
                if e.is_big:
                    self.is_game_over = True
                else:
                    self.player.health -= 1
                    self.enemies.remove(e)
                    if self.player.health <= 0:
                        self.is_game_over = True

            # Bullet-Enemy Collision
            for b in self.bullets[:]:
                if b.pos.distance_to(e.pos) < (b.radius + e.radius):
                    e.health -= 1
                    if b in self.bullets: 
                        self.bullets.remove(b)
                    if e.health <= 0:
                        if e in self.enemies: self.enemies.remove(e)
                        self.slayed += 1
                        self.score += (5 if e.is_big else 2)

            for p in self.objects[:]:
                p.on_player_contact(self.player)  # Call the contact check
                if p.picked_up:
                    self.objects.remove(p)        # Remove it from the list if collected

    def reset_game(self):
        self.player = Player()      # Creates a fresh player with full health
        self.bullets = []           # Clears active bullets
        self.enemies = []           # Clears existing enemies
        self.score = 0
        self.slayed = 0
        self.is_game_over = False
        
        # Restart the ready-up countdown
        self.ready_timer = 3.0
        self.game_started = False
        
        # Reload and play the music from the beginning (or timestamp)
        #pygame.mixer.music.play(-1, 45.0)

    def draw(self):
        self.screen.fill('black')
        
        if not self.is_game_over:
            self.player.draw(self.screen)
            for b in self.bullets: b.draw(self.screen)
            for e in self.enemies: e.draw(self.screen)
            for p in self.objects: p.draw(self.screen)
        else:
            msg = self.game_over_font.render("GAME OVER!", True, 'RED')
            self.screen.blit(msg, (SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2 - 40))
            restart_txt=self.font.render(f"Restart: Enter key", True, 'white')
            self.screen.blit(restart_txt, (SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2 - 70))

          


        # UI
        score_txt = self.font.render(f"Score: {self.score}", True, 'BLUE')
        slayed_txt = self.font.render(f"SLAYED: {self.slayed}", True, 'white')
        lives_txt=self.font.render(f"Total Lives: {self.player.health}", True, 'white')
        self.screen.blit(score_txt, (10, 10))
        self.screen.blit(slayed_txt, (10, 40))
        self.screen.blit(lives_txt, (10, 70))




        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()

if __name__ == "__main__":
    Game().run()