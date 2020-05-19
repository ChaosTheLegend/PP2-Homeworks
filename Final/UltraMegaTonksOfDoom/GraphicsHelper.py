import colorsys
import pygame


#healthbars
def DrawHealthbar(x,y,w,h,value,maxval,direction,fillbg,screen,customcol=None):
    
    if(fillbg):
        pygame.draw.rect(screen, (180,180,180), (x-1,y-1,w+2,h+2), 0)

    if(value <= 0):
        return
    col = ''
    if(customcol == None):
        col = createcol((value/maxval)*128) 
    else:
        col = customcol
        
    #Right
    if(direction == 0):
        pygame.draw.rect(screen, col, (x,y,int(w*(value/maxval)),h), 0)
    #Down
    if(direction == 1):
        pygame.draw.rect(screen, col, (x,y,w,int(h*(value/maxval))), 0)
    #Left
    if(direction == 2):
        pygame.draw.rect(screen, col, (x+(w-int(w*(value/maxval))),y,int(w*(value/maxval)),h), 0)
    #Up
    if(direction == 3):
        pygame.draw.rect(screen, col, (x,y+(h-int(h*(value/maxval))),w,int(h*(value/maxval))), 0)

#Textbox
def DrawTextbox(x,y,w,h,font,bodercol,bgcol,selectedcol,textcol,selected,text,screen,events):
    mspos = pygame.mouse.get_pos() 
    output = {'selected':selected,'text':text}
    pygame.draw.rect(screen, bgcol, (x,y,w,h))
    if(selected):
        pygame.draw.rect(screen, selectedcol, (x,y,w,h), 2)
    else:
        pygame.draw.rect(screen, bodercol, (x,y,w,h), 2)

    if(x <= mspos[0] <= x+w and y <= mspos[1] <= y+h):
        if(pygame.mouse.get_pressed()[0] == 1):
            output['selected'] = True
    elif(pygame.mouse.get_pressed()[0] == 1):
        output['selected'] = False
        
    tx2 = font.render(output['text'], True, textcol)
    tx2Rect = tx2.get_rect() 
    tx2Rect.center = (x+w//2,y+h//2)
    tx2Rect.x = x+5
    if(output['selected']):
        for event in events:  
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    output['selected'] = False
                    return output
                elif event.key == pygame.K_BACKSPACE:
                    output['text'] = output['text'][:-1]
                else:
                    output['text'] += event.unicode
                    tx2 = font.render(output['text'], True, textcol)
                    tx2Rect = tx2.get_rect() 
                    tx2Rect.center = (x+w//2,y+h//2)
                    tx2Rect.x = x+5
                    if (tx2Rect.w > w-10):
                        output['text'] = output['text'][:-1]
    screen.blit(tx2, tx2Rect)
    return output

#colorgen
def createcol(h):
    col = colorsys.hsv_to_rgb(h/360, 1.0, 1.0) 
    return (col[0]*255,col[1]*255,col[2]*255) 

#drawing text
def DrawText(text,font,color,position,screen):
    tx = font.render(text, True, color)
    txRect = tx.get_rect() 
    txRect.center = position
    screen.blit(tx, txRect)

#button generator
def DrawButton(x,y,w,h,bgcol,bordercol,font,text,textcol,onclick,screen,events):
    mspos = pygame.mouse.get_pos() 
    pygame.draw.rect(screen, bgcol, (x,y,w,h))
    if(x <= mspos[0] <= x+w and y <= mspos[1] <= y+h):
        pygame.draw.rect(screen, bordercol, (x,y,w,h),2)
        for event in events:  
            if(event.type == pygame.MOUSEBUTTONDOWN):
                if(pygame.mouse.get_pressed()[0] == 1):
                    onclick()
    
    DrawText(text,font,textcol,((x+w//2),(y+h//2)),screen)
 