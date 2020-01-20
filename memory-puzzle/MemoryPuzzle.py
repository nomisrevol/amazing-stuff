# import module, neccessary 
import pygame
import random
import sys
from pygame.locals import *

# constant
WINDOW_WIDTH      = 640
WINDOW_HEIGHT     = 480
BOARD_WIDTH       = 2
BOARD_HEIGHT      = 2
NUMBERS_OF_GROUP  = 8
SPEED             = 6
BOX_SIZE          = 40
GAP_SIZE          = 10
FPS               = 30

MARGINLEFT = int((WINDOW_WIDTH - (BOARD_WIDTH * (BOX_SIZE + GAP_SIZE))) / 2)
MARGINTOP  = int((WINDOW_HEIGHT - (BOARD_HEIGHT * (BOX_SIZE + GAP_SIZE))) / 2)

# color 
#             R    G    B
GRAY      = (100, 100, 100)
NAVY_BLUE = ( 60,  60, 100)
WHITE     = (255, 255, 255)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
BLUE      = (  0,   0, 255)
YELLOW    = (255, 255,   0)
ORANGE    = (255, 128,   0)
PURPLE    = (255,   0, 255)
CYAN      = (  0, 255, 255)

BACKGROUNDCOLOR = NAVY_BLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT   = 'donut'
SQUARE  = 'square'
DIAMOND = 'diamond'
LINES   = 'lines'
OVAL    = 'oval'

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)

# create board
def createBoard():
  icons = []
  for shape in ALLSHAPES:
    for color in ALLCOLORS:
      icons.append((shape, color))

  random.shuffle(icons)
  cnt = int(BOARD_WIDTH * BOARD_HEIGHT / 2) # number of icon need to use
  icons = icons[:cnt] * 2
  random.shuffle(icons)

  board = []
  pos = 0
  for x in range(BOARD_WIDTH):
    board.append([])
    for y in range(BOARD_HEIGHT):
      board[x].append(icons[pos])
      pos += 1

  return board

# create opened state 
def createOpened(value):
  result = []
  for x in range(BOARD_WIDTH):
    result.append([value] * BOARD_HEIGHT)
  return result

# split to group to begin game
def splitIntoGroupOf(size, allList):
  result = []
  for i in range(0, len(allList), size):
    result.append(allList[i: i + size])
  return result

# draw icon
def drawIcon(shape, color, box_x, box_y):
  quarter = int(BOX_SIZE * 0.25)
  half    = int(BOX_SIZE * 0.5)  

  left, top = calcLeftTop(box_x, box_y) # get pixel coords from board coords
  # Draw the shapes
  if shape == DONUT:
    pygame.draw.circle(SURFACE, color, (left + half, top + half), half - 5)
    pygame.draw.circle(SURFACE, BACKGROUNDCOLOR, (left + half, top + half), quarter - 5)
  elif shape == SQUARE:
    pygame.draw.rect(SURFACE, color, (left + quarter, top + quarter, BOX_SIZE - half, BOX_SIZE - half))
  elif shape == DIAMOND:
    pygame.draw.polygon(SURFACE, color, ((left + half, top), (left + BOX_SIZE - 1, top + half), (left + half, top + BOX_SIZE - 1), (left, top + half)))
  elif shape == LINES:
    for i in range(0, BOX_SIZE, 4):
      pygame.draw.line(SURFACE, color, (left, top + i), (left + i, top))
      pygame.draw.line(SURFACE, color, (left + i, top + BOX_SIZE - 1), (left + BOX_SIZE - 1, top + i))
  elif shape == OVAL:
    pygame.draw.ellipse(SURFACE, color, (left, top + quarter, BOX_SIZE, half))

# calc left, top coordinate of a box
def calcLeftTop(box_x, box_y):
  left = box_x * (BOX_SIZE + GAP_SIZE) + MARGINLEFT
  top = box_y  * (BOX_SIZE + GAP_SIZE) + MARGINTOP
  return (left, top)

# draw cover box 
def drawBoxCover(board, boxes, coverage):
  for box in boxes:
    left, top = calcLeftTop(box[0], box[1])
    pygame.draw.rect(SURFACE, BACKGROUNDCOLOR, (left, top, BOX_SIZE, BOX_SIZE))
    shape, color = getShapeAndColor(board, box[0], box[1])
    drawIcon(shape, color, box[0], box[1])
    if coverage > 0:
      pygame.draw.rect(SURFACE, BOXCOLOR, (left, top, coverage, BOX_SIZE))
  pygame.display.update()
  FPSCLOCK.tick(FPS)

# highlight box when mouse motion or clicked
def highlightBox(box_x, box_y):
  left, top = calcLeftTop(box_x, box_y)
  pygame.draw.rect(SURFACE, HIGHLIGHTCOLOR, (left - 5, top - 5, BOX_SIZE + 10, BOX_SIZE + 10), 4)

# open animation 
def openBox(board, boxesToOpen):
  for coverage in range(BOX_SIZE, (-SPEED) - 1, -SPEED):
    drawBoxCover(board, boxesToOpen, coverage)

# close animation
def closeBox(board, boxesToClose):
  for coverage in range(0, BOX_SIZE + SPEED, SPEED):
    drawBoxCover(board, boxesToClose, coverage)


# get shape and color
def getShapeAndColor(board, box_x, box_y):
  return (board[box_x][box_y][0], board[box_x][box_y][1])

# draw board
def drawBoard(board, opened):
  for box_x in range(BOARD_WIDTH):
    for box_y in range(BOARD_HEIGHT):
      left, top = calcLeftTop(box_x, box_y)
      if not opened[box_x][box_y]:
        pygame.draw.rect(SURFACE, BOXCOLOR, (left, top, BOX_SIZE, BOX_SIZE))
      else:
        shape, color = getShapeAndColor(board, box_x, box_y)
        drawIcon(shape, color, box_x, box_y)

# start game animation
def startGame(board):
  boxes = []
  for x in range(BOARD_WIDTH):
    for y in range(BOARD_HEIGHT):
      boxes.append((x, y))
  random.shuffle(boxes)
  boxGroups = splitIntoGroupOf(NUMBERS_OF_GROUP, boxes)
  openedBox = createOpened(False)
  drawBoard(board, openedBox)
  for x in boxGroups:
    (board, x)
    closeBox(board, x)

# get pixel of box
def getBox(x, y):
  for box_x in range(BOARD_WIDTH):
    for box_y in range(BOARD_HEIGHT):
      left, top = calcLeftTop(box_x, box_y)
      boxRect = pygame.Rect(left, top, BOX_SIZE, BOX_SIZE)
      if boxRect.collidepoint(x, y):
        return (box_x, box_y)
  return (None, None)

# if win game
def gameWon(board):
  openedBoxes = createOpened(True)
  color1 = LIGHTBGCOLOR
  color2 = BACKGROUNDCOLOR

  for _ in range(10):
    color1, color2 = color2, color1
    SURFACE.fill(color1)
    drawBoard(board, openedBoxes)
    pygame.display.update()
    pygame.time.wait(300)

# check win game
def hasWon(opened):
  for i in opened:
    if False in opened:
      return False
  return True

# def draw exit button
def drawExitButton():
  fontObj = pygame.font.Font('freesansbold.ttf', 30)
  textSurfaceObj = fontObj.render('EXIT!', True, YELLOW, RED)
  textRectObj = textSurfaceObj.get_rect()
  textRectObj.center = (550, 450)
  SURFACE.blit(textSurfaceObj, textRectObj)  

# main 
def main():
  # init surface
  pygame.init()
  global SURFACE, FPSCLOCK
  SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
  FPSCLOCK = pygame.time.Clock()
  pygame.display.set_caption('Memory Puzzle Game')    

  mainBoard = createBoard()
  opened = createOpened(False)
  SURFACE.fill(BACKGROUNDCOLOR)
  startGame(mainBoard)

  firstSelect = None
  mouse_x = 0
  mouse_y = 0

  while True:
    SURFACE.fill(BACKGROUNDCOLOR)
    drawBoard(mainBoard, opened)

    drawExitButton()
    clicked = False

    for event in pygame.event.get():
      if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
        pygame.quit()
        sys.exit()
      elif event.type == MOUSEMOTION:
        mouse_x, mouse_y = event.pos
      elif event.type == MOUSEBUTTONUP:
        clicked = True

    if clicked == True and mouse_x >= 508 and mouse_x <= 590 and mouse_y >= 436 and mouse_y <= 466:
      pygame.quit()
      sys.exit()

    box_x, box_y = getBox(mouse_x, mouse_y)

    if box_x != None and box_y != None:
      if not opened[box_x][box_y]:
        highlightBox(box_x, box_y)
      if not opened[box_x][box_y] and clicked:
        openBox(mainBoard, [(box_x, box_y)])
        opened[box_x][box_y] = True
        if firstSelect == None:
          firstSelect = (box_x, box_y)
        else:
          shape1, color1 = getShapeAndColor(mainBoard, firstSelect[0], firstSelect[1])
          shape2, color2 = getShapeAndColor(mainBoard, box_x, box_y)

          if shape1 != shape2 or color1 != color2:
            pygame.time.wait(1000)
            closeBox(mainBoard, [(firstSelect[0], firstSelect[1]), (box_x, box_y)])
            opened[firstSelect[0]][firstSelect[1]] = False
            opened[box_x][box_y] = False
          elif hasWon(opened):
            gameWon(mainBoard)
            pygame.time.wait(2000)

            mainBoard = createBoard()
            opened = createOpened(False)

            drawBoard(mainBoard, opened)
            pygame.display.update()
            pygame.time.wait(1000)

            startGame(mainBoard)
          firstSelect = None

    pygame.display.update()
    FPSCLOCK.tick(FPS)


if __name__ == '__main__':
  main()
