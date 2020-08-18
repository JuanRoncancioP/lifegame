import pygame
import numpy as np
import time

def main():
    
    pygame.init()

    width, heigth = 720, 480
    screen = pygame.display.set_mode((width, heigth))
    bg = (25, 25, 25)
    screen.fill(bg)
    
    nxC, nyC = (70, 50) 
    
    dimCW = width / nxC
    dimCH = heigth / nyC

    

    gameState = np.zeros((nxC, nyC))

    #automata palo
    gameState[5, 3] = 1
    gameState[5, 4] = 1
    gameState[5, 5] = 1

    #Automata movil
    gameState[21, 21] = 1
    gameState[22, 22] = 1
    gameState[22, 23] = 1
    gameState[21, 23] = 1
    gameState[20, 23] = 1

    pauseExec = False
    
    salida = True

    while salida: 
        time.sleep(0.1)
        newGameState = np.copy(gameState)
        
        ev = pygame.event.get()
        
        for event in ev:
            if event.type == pygame.KEYDOWN:
                pauseExec = not pauseExec
            if event.type == pygame.QUIT:
                salida = False

        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0: 
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = 1
            # not mouseClick[2]

        
        screen.fill(bg)
        for x in range(0, nxC):
            for y in range(0, nyC):
                if not pauseExec:
                    
                    n_neigh = \
                    gameState[(x - 1)%nxC, (y - 1)%nyC] + \
                    gameState[(x - 1)%nxC, (y + 1)%nyC] + \
                    gameState[(x - 1)%nxC, (y    )%nyC] + \
                    gameState[(x + 1)%nxC, (y   )%nyC] + \
                    gameState[(x + 1)%nxC, (y - 1)%nyC] + \
                    gameState[(x + 1)%nxC, (y + 1)%nyC] + \
                    gameState[(x    )%nxC, (y + 1)%nyC] + \
                    gameState[(x    )%nxC, (y - 1)%nyC] 

                    #Si tienes una casilla muerta pero tiene 3 vivas al rededor revive
                    if gameState[x, y] == 0 and n_neigh == 3:
                        newGameState[x, y] = 1
                    
                    #Muere por sobrepoblacion o soledad
                    if gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                        newGameState[x, y] = 0    
                
                poly = \
                [((x   ) * dimCW, y       * dimCH),
                ((x + 1) * dimCW, y       * dimCH),
                ((x + 1) * dimCW, (y + 1) * dimCH),
                ((x    ) * dimCW, (y + 1) * dimCH)
                ]
                
                if newGameState[x, y] == 0:
                    pygame.draw.polygon(screen, (128, 128, 128), poly, 1 )
                else:
                    pygame.draw.polygon(screen, (255, 255, 255), poly, 0 )
                
        gameState = np.copy(newGameState)
        pygame.display.flip()

if __name__ == '__main__':
    main()