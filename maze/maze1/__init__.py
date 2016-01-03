import turtle
EAST=0;NORTH=1;WEST=2;SOUTH=3
class Maze(object):
   """ Solves a maze """
   def __init__(self):
      self.screen=turtle.Screen()
   	 self.turtle=turtle.Turtle()
   	 self.screen.bgcolor('blue')
      self.matrix=[[1 for i in range(20)] for i in range(20)]
      self.turtle.penup()
   def reset(self):
      self.turtle.goto(-190,190)
      self.matrix=[[1 for i in range(20)] for i in range(20)]
      self.screen.bgcolor('blue')
      self.turtle.shape('square')
      self.turtle.color('white')
      self.turtle.stamp()
      self.matrix[0][0]=0
   def dig(self):
      pass
   def getMatrixValueAt(self,pos):
      x=int((pos[0]+200)/20)
      y=20-int((pos[1]+200)/20)-1
      v=self.matrix[x][y]
      return v
   def setMatrixValueAt(self,pos,value):
      x=int((pos[0]+200)/20)
      y=20-int((pos[1]+200)/20)-1
      try:
         self.matrix[y][x]=value
      except:
         return False
      if value==0:
         self.turtle.color('white')
         self.turtle.stamp()
      if value==1:
         self.turtle.color('blue')
         self.turtle.stamp()
      return True
