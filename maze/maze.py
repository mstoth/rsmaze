def direction(pos1,pos2):
    """ returns the direction from position 1 to position 2 """
    if pos1[0]==pos2[0]: # x position the same, either NORTH or SOUTH
        if pos1[1]<pos2[1]: # NORTH
            return NORTH
        else:
            return SOUTH
    else:
        if pos2[0]>pos1[0]: # EAST
            return EAST
        else:
            return WEST


import turtle
import random
INVALID = -1; EMPTY = 0; WALL = 1; VISITED = 2; END = 3
EAST=0;NORTH=1;WEST=2;SOUTH=3
class Maze(object):
    """ Solves a maze using a 40x40 matrix as an internal model
             and a 400x400 screen graphical view.
          reset() puts the turtle in the upper left hand corner.
          getMatrixValueAt(position) returns the matrix value at the tuple position
    """

    def __init__(self):
        self.screen=turtle.Screen()
        self.turtle=turtle.Turtle()
        self.screen.bgcolor('blue')
        self.matrix=[[1 for i in range(40)] for i in range(40)]
        self.turtle.penup()
        self.reset()

    def makeMaze(self):
        n=self.neighbors()
        oldpos=self.turtle.position()
        while len(n)>0:
            nchoice=random.choice(n)
            n.remove(nchoice)
            self.turtle.goto(oldpos)
            if self.getMatrixValueAt(nchoice[0])==WALL:
                d=direction(self.turtle.position(),nchoice[0])
                self.dig(d)
                self.dig(d)
                self.makeMaze()

    def reset(self):
        self.turtle.goto(-390,390)
        self.matrix=[[1 for i in range(40)] for i in range(40)]
        self.screen.bgcolor('blue')
        self.turtle.shape('square')
        self.turtle.color('white')
        self.turtle.stamp()
        self.matrix[0][0]=0

    def neighbors(self):
        p=self.turtle.position()
        r=[]
        r.append([(p[0],p[1]+40),m.getMatrixValueAt((p[0],p[1]+40))])
        r.append([(p[0],p[1]-40),m.getMatrixValueAt((p[0],p[1]-40))])
        r.append([(p[0]+40,p[1]),m.getMatrixValueAt((p[0]+40,p[1]))])
        r.append([(p[0]-40,p[1]),m.getMatrixValueAt((p[0]-40,p[1]))])
        return r

    def dig(self,dir):
        if dir == EAST:
            if self.turtle.position()[0]<390:
                if self.turtle.position()[0]+20 > 390:
                    return self.turtle.position
            if self.getMatrixValueAt((self.turtle.position()[0]+20,self.turtle.position()[1]))>0:
                self.turtle.goto(self.turtle.position()[0]+20,self.turtle.position()[1])
                self.setMatrixValueAt(self.turtle.position(),0)
        elif dir == SOUTH:
            if self.turtle.position()[1]>-390:
                if self.turtle.position()[1]-20 < -390:
                    return self.turtle.position()
            if self.getMatrixValueAt((self.turtle.position()[0],self.turtle.position()[1]-20))>0:
                self.turtle.goto(self.turtle.position()[0],self.turtle.position()[1]-20)
                self.setMatrixValueAt(self.turtle.position(),0)
        elif dir ==  WEST:
            if self.turtle.position()[0]>-390:
                if self.turtle.position()[0]-20 < -390:
                    return self.turtle.position()
            if self.getMatrixValueAt((self.turtle.position()[0]-20,self.turtle.position()[1]))>0:
                self.turtle.goto(self.turtle.position()[0]-20,self.turtle.position()[1])
                self.setMatrixValueAt(self.turtle.position(),0)
        elif dir ==  NORTH:
            if self.turtle.position()[1]<390:
                if self.turtle.position()[1]+20 > 390:
                    return self.turtle.position()
            if self.getMatrixValueAt((self.turtle.position()[0],self.turtle.position()[1]+20))>0:
                self.turtle.goto(self.turtle.position()[0],self.turtle.position()[1]+20)
                self.setMatrixValueAt(self.turtle.position(),0)
        return self.turtle.position()

    def setMatrixValueAt(self,pos,value):
        x=int((pos[0]+400)/20)
        y=40-int((pos[1]+400)/20)-1
        try:
            self.matrix[x][y]=value
        except:
            return False
        oldPos=self.turtle.position()
        self.turtle.goto(pos)
        if value==0:
            self.turtle.color('white')
            self.turtle.stamp()
        if value==1:
            self.turtle.color('blue')
            self.turtle.stamp()
        self.turtle.goto(oldPos)
        return True

    def getMatrixValueAt(self,pos):
        x=int((pos[0]+400)/20)
        y=40-int((pos[1]+400)/20)-1
        if (pos[0]+400)/20<0 or x>19:
            return -1
        if ((pos[1]+400)/20)>19.5 or ((pos[1]+400)/20)<0:
            return -1
        v=self.matrix[x][y]
        return v


