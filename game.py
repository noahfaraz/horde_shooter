import pygame
import random
pygame.init()

screen=pygame.display.set_mode((500,500))
clock=pygame.time.Clock()
running=True
dt=0
player_pos = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)
bullet_speed=600
bullets=[]
enemy=[]
big_enemy=[]
big_enemy_health=3
player_health=3
start_ticks=pygame.time.get_ticks()
slayed=0
score=0
not_contact=True

enemy_speed=180
big_enemy_speed=120

font = pygame.font.SysFont(None, 25)
game_over_font=pygame.font.Font(None,74)


def get_time():
        return (pygame.time.get_ticks() - start_ticks) // 1000


def spawn_enemy(enemy_list,player_pos, min_distance=40, max_attempts=50):
    for _ in range(max_attempts):
        pos = pygame.Vector2(
            random.randint(0, screen.get_width()),
            random.randint(0, screen.get_height())
        )

        valid = True
        for e in enemy_list:
            if pos.distance_to(e) < min_distance :
                valid = False
                break
            if pos.distance_to(player_pos)<60:
                 valid=False
                 break

        if valid:
            enemy_list.append(pos)
            return  # success

   

def spawn_big_enemy(big_enemy,player_pos, min_distance=40, max_attempts=50):
    for _ in range(max_attempts):
        pos = pygame.Vector2(
            random.randint(0, screen.get_width()),
            random.randint(0, screen.get_height())
        )

        valid = True
        for e,h in big_enemy:
            if pos.distance_to(e) < min_distance :
                valid = False
                break
            if pos.distance_to(player_pos)<60:
                 valid=False
                 break

        if valid:
            big_enemy.append([pos,big_enemy_health])
            return  # success


enemy_gen=random.randint(2,4)
enemy_counter=0
while enemy_counter<enemy_gen:
        enemy_pos=pygame.Vector2( random.randint(0,screen.get_width()) ,random.randint(0,screen.get_height()))
        if enemy_pos.distance_to(player_pos)>200:
            enemy.append(enemy_pos)
            #pygame.draw.circle(screen,'red',enemy_pos,30)
            enemy_counter+=1
        else:
            continue


enemy_spawn=pygame.USEREVENT
pygame.time.set_timer(enemy_spawn,1800)#10 seconds 1 enemy spawns

big_enemy_event=pygame.USEREVENT+1
pygame.time.set_timer(big_enemy_event,10000)
  



while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
             running=False
        if not_contact:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # ← spawn bullet ONCE per keypress #right bullet
                        bullet_pos=pygame.Vector2(player_pos.x+20, player_pos.y)
                        bullets.append([bullet_pos,1])
                
                if event.key == pygame.K_o: # ← spawn bullet ONCE per keypress
                        left_bullet=True
                        right_bullet=False
                        bullet_pos=pygame.Vector2(player_pos.x-20, player_pos.y)
                        bullets.append((bullet_pos,-1))

       

      
        if not_contact:
            if event.type==enemy_spawn:
                enemy_roll=random.random()
                if enemy_roll<0.5:
                    spawn_enemy(enemy,player_pos)
                    spawn_enemy(enemy,player_pos)


                elif random.random()<0.8:
                     spawn_enemy(enemy,player_pos)
                     spawn_enemy(enemy,player_pos)
                     spawn_enemy(enemy,player_pos)

                     
                    
                else:
                     spawn_enemy(enemy,player_pos)
                     spawn_enemy(enemy,player_pos)
                     spawn_enemy(enemy,player_pos)
                     spawn_enemy(enemy,player_pos)

            
            if event.type==big_enemy_event:
                spawn_big_enemy(big_enemy,player_pos)
                     

                     

    



    screen.fill('black')
    pygame.draw.circle(screen,'yellow',player_pos,20)
 
    for enemy_pos in enemy:
        pygame.draw.circle(screen, 'red', enemy_pos, 8)

    
    for big_enemy_pos,h in big_enemy:
        pygame.draw.circle(screen, 'blue', big_enemy_pos,15)
   
   
    
    if  not_contact:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos.y -= 350 * dt
        if keys[pygame.K_s]:
            player_pos.y += 350 * dt
        if keys[pygame.K_a]:
            
            player_pos.x -= 350 * dt
        if keys[pygame.K_d]:

        
            player_pos.x += 350 * dt
        

    if not_contact:
        for e in enemy[:]:

            direction = (player_pos - e)
            
            if direction.length() != 0:
            
                direction = direction.normalize()
            
            e += direction * enemy_speed * dt

        
        for e,h in big_enemy[:]:
             direction = (player_pos - e)
            
             if direction.length() != 0:
            
                direction = direction.normalize()
            
             e += direction * big_enemy_speed * dt
             
        
    
    bullet_pos=(player_pos.x,player_pos.y)

    for bullet in bullets[:]:
            if bullet[1]==1:
                bullet[0][0] += bullet_speed * dt
            elif bullet[1]==-1:
                 bullet[0][0]-=bullet_speed*dt
     

            if bullet[0][0] > screen.get_width() and bullet[0][0] < screen.get_width():
                bullets.remove(bullet)
                continue
            if not_contact:
                pygame.draw.circle(screen,(255,255,255), bullet[0], 3)

   

            for e in enemy[:]:
                 if bullet[0].distance_to(e) < 20:
                    enemy.remove(e)
                    bullets.remove(bullet)
                    slayed += 1
                    score+=2
                    # score_roll=random.random()
                    # if score_roll<.4:
                    #     score+=5
                    # if score_roll<.6:
                    #      score+=7
                    # else:
                    #      score+=3
                         
                    # break

            

            for item in big_enemy[:]:
                e, h = item[0], item[1]
                if bullet[0].distance_to(e) < 20:
                     item[1] -= 1          # ← modifies the actual list item
                     bullets.remove(bullet)
                if item[1] == 0:
                     big_enemy.remove(item)  # ← removes the full [pos, health] pair
                     slayed += 1
                     score+=5
                    #  score_roll = random.random()
                    #  if score_roll < .4:
                    #     score += 5
                    #  elif score_roll < .6:
                    #     score += 7
                    #  else:
                    #     score += 3
                    #  break
       




    for e in enemy[:]:
         if player_pos.distance_to(e)<20:
            # player_pos[0]=-30
            # player_pos[1]=-30
            # #only for testing
            player_health-=1
            if player_health <= 0:
                not_contact=False



    for e,h in big_enemy[:]:
          if player_pos.distance_to(e)<20:
            # player_pos[0]=-30
            # player_pos[1]=-30
            # #only for testing
           
             not_contact=False
         

 #borders
    current_time = get_time()

   
    if player_pos[0] < 0:
            player_pos[0] = 0
    if player_pos[0] > screen.get_width():
            player_pos[0] = screen.get_width()

    if player_pos[1] < 0:
            player_pos[1] = 0
    if player_pos[1] > screen.get_height():
            player_pos[1] = screen.get_height()

    slayed_text = font.render(f"SLAYED: {slayed}", True, 'white')
    score_text = font.render(f"Score: {score}", True, 'BLUE')
    game_over=game_over_font.render(f"GAME OVER!",True,'RED')

    # if not_contact!=1:
    # screen.blit(score_text, (screen.get_width()/4, screen.get_height()/4)) # top left c
    # screen.blit(num_text, (screen.get_width()/4, screen.get_height()/4+30))  # top left c
    screen.blit(score_text, (0,0) )# top left c
    screen.blit(slayed_text, (0,30)) # top left c
    
    if not_contact!=1:
         screen.blit(game_over, (screen.get_width()/6, 0))
 
    pygame.display.flip()#display stuff on screen which is drawn

    dt=clock.tick(60)/1000
    if running==False:
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                running=True
                not_contact=True
pygame.quit()