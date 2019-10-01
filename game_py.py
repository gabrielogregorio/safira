'''
************************************ JOGO DA COBRA ************************************
Criando um SNAKE do ZERO com PYGAME em 5 MINUTOS (ou mais)
LINK: https://www.youtube.com/watch?v=H4TXHI9BRCQ

********************************** CRÉDITOS DO AUDIO **********************************
"Chewing, Breadstick, Single, G.wav" by InspectorJ (www.jshaw.co.uk) of Freesound.org
LINK: https://freesound.org/people/InspectorJ/sounds/429596/
AUDIO EDITADO NO SITE: https://audiotrimmer.com/pt/

************************************ ALTERAÇÕES ***************************************
Gabriel Gregório da Silva
'''
from random import randint
from pygame import mixer , display , Surface , time , event , init , quit
from pygame.locals import QUIT , KEYDOWN , K_UP , K_DOWN , K_LEFT , K_RIGHT

UP    = 0
RIGHT = 1
DOWN  = 2
LEFT  = 3

init()

# OBTER VALORES DENTRO DA GRID
def on_grid_random():
    x = randint(0,590)
    y = randint(0,590)
    return (x//10*10,y//10 * 10)

# DETECTA COLISÃO
def colision(c1,c2):
    colidiu =  (c1[0] == c2[0] and (c1[1] == c2[1]))

    # TOCAR UM SOM
    if colidiu:
        mixer.music.load('comendo.mp3')
        mixer.music.play(1)

    return colidiu

screen = display.set_mode((600,600))    # TELA
display.set_caption('Snake')            # TITULO

snake_skin = Surface((10,10))           # TAMANHO DA COBRA
snake_skin.fill((255,255,255))          # COR DA COBRA
snake = [(200,200),(210,200),(220,200)] # PARTES E POSIÇÕES DA COBRA
my_direction = LEFT                     # INICIA ANDANDO PARA A ESQUERDA

apple = Surface((10,10))                # TAMANHO DA MAÇA
apple.fill((255,0,0))                   # COR DA MAÇA
apple_pos = on_grid_random()            # POSIÇÂO DA MAÇA

clock = time.Clock()                    # CONTROLE DO FPS - VELOCIDADE
sair_do_jogo = False                    # SAIR DO GAME - EVITAR ERROS

while True:
    clock.tick(20)                      # DEFINE O CLOCK
    for evento in event.get():          # CAPTURAR EVENTOS
        if evento.type == QUIT:         # EVENTO DE SAIR
            quit()
            sair_do_jogo = True
            
        elif evento.type == KEYDOWN:    # TECLA PRESSIONADA
            if evento.key == K_UP:
                my_direction = UP 

            elif evento.key == K_DOWN:
                my_direction = DOWN

            elif evento.key == K_LEFT:
                my_direction = LEFT

            elif evento.key == K_RIGHT:
                my_direction = RIGHT 

    if sair_do_jogo:
        break

    if colision(snake[0],apple_pos):    # COLISÃO!
        apple_pos = on_grid_random()    # NOVA POSIÇÃO PARA A MAÇA
        snake.append((0,0))             # ADICIONA MAIS UM BLOCO NA COBRA

    # ATUALIZANDO BLOCOS DA COBRA 
    for i in range(len(snake) - 1, 0, -1):
        snake[i] = (snake[i-1][0],snake[i-1][1])

    # DIREÇÃO DA COBRA
    if my_direction == UP:
        snake[0] = (snake[0][0],snake[0][1] -10)
    elif my_direction == DOWN:
        snake[0] = (snake[0][0],snake[0][1] +10)
    elif my_direction == RIGHT:
        snake[0] = (snake[0][0] + 10,snake[0][1])
    elif my_direction == LEFT:
        snake[0] = (snake[0][0] - 10, snake[0][1])


    # LIMPANDO A TELA
    screen.fill((0,0,0))
    screen.blit(apple,apple_pos)

    # PARA CADA POSIÇÃO DA COBRA
    for pos in snake:
        screen.blit(snake_skin,pos)

    display.update()
