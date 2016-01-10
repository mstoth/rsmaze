=====================
The CSI 106 Maze Project
=====================

.. Here is were you specify the content and order of your new book.

.. Each section heading (e.g. "SECTION 1: A Random Section") will be
   a heading in the table of contents. Source files that should be
   generated and included in that section should be placed on individual
   lines, with one line separating the first source filename and the
   :maxdepth: line.

.. Sources can also be included from subfolders of this directory.
   (e.g. "DataStructures/queues.rst").

SECTION 1: Introduction
:::::::::::::::::::::::

We will be first creating a maze using test driven development techniques.  Each step of the way will begin with a test.  To start, we get really stupid.  The first thing we need to test for is a Maze class.  Of course there is no Maze class.  We haven't written it yet.  But we are stupid.  Let's test for it.


.. activecode:: m_test_1

   m=Maze() # see if a Maze class exists.

This code should run without an error if there is a Maze class.

You should see an error when you run the code.
It's a pretty ugly NameError:

You are in what we call condition RED.  The next step is to get into condition GREEN.  We do this by writing the minimal amount of code we need to make the test pass.

Let's make it a little prettier first and use the try statement as follows: 

.. activecode:: m_try_1

   try:
      m=Maze()
   except:
      print "Maze class does not yet exist. CONDITION RED" 

Much better.

Now let's make this class exist. 

.. activecode:: m_class_1
 
   class Maze(object):
      """ Creates a maze. (We don't know anything more than that yet.) """
      def __init__(self):
         pass

   condition="GREEN"
   try:
      m=Maze()
   except:
       condition="RED"
   print "Condition: " + condition


We will use the turtle module to make our maze. The screen is created with the following command

.. activecode:: m_w_1

   import turtle
   wn = turtle.Screen()
   wn.bgcolor("blue")


When you run this code you will see the blue screen we created. A blue color means a wall. 
This is the visual representation of our maze. We don't have any paths created yet. It's all
wall. 

Now let's put this into the maze class. First write the test for the screen.

.. activecode:: m_test_screen

   import turtle
   class Maze(object):
      """ Solves a maze """
      def __init__(self):
         pass

   m=Maze()
   assert type(m.screen)==turtle.Screen

Now add the screen.

.. activecode:: m_add_screen

   import turtle
   class Maze(object):
      """ Solves a maze """
      def __init__(self):
         self.screen=turtle.Screen()

   m=Maze()
   assert type(m.screen)==turtle.Screen

Condition is now GREEN. We also need a turtle.  Add a test for the turtle. 

.. activecode:: m_turtle_test

   import turtle
   class Maze(object):
      """ Solves a maze """
      def __init__(self):
         self.screen=turtle.Screen()

   m=Maze()
   assert type(m.turtle)==turtle.Turtle

And you know the next step to get GREEN. 

.. activecode:: m_add_turtle

   import turtle
   class Maze(object):
      """ Solves a maze """
      def __init__(self):
         self.screen=turtle.Screen()
	 self.turtle=turtle.Turtle()

   m=Maze()
   assert type(m.turtle)==turtle.Turtle

We will first be constructing our maze using the colors blue for a wall, white for a path, and yellow for the final goal.  Since we are making a path, it seems like a good starting point would be to have nothing but walls.  This means a blue screen.  We can test by looking at the bgcolor method for Screen.

.. activecode:: m_blue_bg


   import turtle
   class Maze(object):
      """ Solves a maze """
      def __init__(self):
         self.screen=turtle.Screen()
	 self.turtle=turtle.Turtle()
	 self.screen.bgcolor('blue')

   m=Maze()
   assert m.screen.bgcolor()=='blue'
   
You should now see the blue screen. (Note that I skipped the RED to GREEN and added both the test and the code) 

Now we need to think about how we will represent our maze inside the program. The screen is the interface to people but internally we need to make decisions based on the current state of the maze.

I choose a matrix as the data type best suited. Each item in the matrix corresponds to a location in the maze. The size of the screen by default is 400x400.  We will keep the default for now.  The way we will draw on the screen is by using the stamp method in the turtle module and a square for the shape. (look into the documentation on the turtle module for more clarification on those methods.) 

The default size for the square is 20x20. So we can have 20 rows and 20 columns in our matrix since the size of the screen is 400x400.  The origin is in the middle. so -190,190 corresponds to the [0][0] location of the matrix. Let's clarify our thinking a little by writing code to draw a white square in the upper left hand corner.  

.. activecode:: m_draw_square

   import turtle
   s=turtle.Screen()
   s.bgcolor('blue')
   t=turtle.Turtle()
   t.penup()
   t.goto(-190,190)
   t.shape('square')
   t.color('white')
   t.stamp()


Here's how we would draw a path along the top of the screen. 

.. activecode:: m_draw_path_1

   import turtle
   s=turtle.Screen()
   s.bgcolor('blue')
   t=turtle.Turtle()
   t.penup()
   for x in range(-190,210,20):
       t.goto(x,190)
       t.shape('square')
       t.color('white')
       t.stamp()


This is all useful for learning about the tools we have.  Let's create a test for our matrix, the internal representation of the maze. 

.. activecode:: m_test_matrix

   import turtle
   class Maze(object):
   	 """ Solves a maze """
         def __init__(self):
      	 self.screen=turtle.Screen()
      	 self.turtle=turtle.Turtle()
      	 self.screen.bgcolor('blue')

   m=Maze()
   assert len(m.matrix)==20

This only checks for the height of our matrix but it's good enough for now. You should weigh how much time you want to spend writing a test vs how risky is the failure.  To make this test pass we want to add a matrix to our maze. Here's the code that does that. Notice that all the values in the matrix are 1 which corresponds to everything being a wall. That's an arbitrary decision I just made. Seems like 0 for no wall and 1 for a wall makes sense. 

.. activecode:: m_add_matrix

   import turtle
   class Maze(object):
   	 """ Solves a maze using a 20x20 matrix as an internal model
             and a 400x400 screen graphical view. """
         def __init__(self):
      	    self.screen=turtle.Screen()
      	    self.turtle=turtle.Turtle()
      	    self.screen.bgcolor('blue')
	    self.matrix=[[1 for i in range(20)] for i in range(20)]

   m=Maze()
   assert len(m.matrix)==20

We will start our path from the upper left hand corner, (another arbitrary choice). Let's imagine we are digging our path through the walls. When we dig into the space, we turn a 1 in our matrix to a 0.  This indicates we have an empty space at that location.  It's easy to then consider a function called *dig* where we pass in a direction and the turtle will dig in that direction one space if possible.  

Since we are starting from the upper left hand corner, matrix[0][0] should be 0 and the turtle location should be -190,190.  Let's put a reset function in so we can always get to this starting configuration. 

.. activecode:: m_reset_test

   import turtle
   class Maze(object):
   	 """ Solves a maze using a 20x20 matrix as an internal model
             and a 400x400 screen graphical view. """
         def __init__(self):
      	    self.screen=turtle.Screen()
      	    self.turtle=turtle.Turtle()
      	    self.screen.bgcolor('blue')
	    self.matrix=[[1 for i in range(20)] for i in range(20)]

   m=Maze()
   m.reset()
   assert m.matrix[0][0]==0
   assert m.turtle.pos()==(-190,190)

Make it pass now. 

.. activecode:: m_reset_pass

   import turtle
   class Maze(object):
      """ Solves a maze using a 20x20 matrix as an internal model
             and a 400x400 screen graphical view. """
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

   m=Maze()
   m.reset()
   assert m.matrix[0][0]==0
   assert m.turtle.pos()==(-190,190)

I think of the turtle as sort-of digging it's way through the walls to make the maze. 

We are at a point where we can consider the *dig* function.  I imagine m.dig(EAST) will move the turtle one square to the East on the screen. But what is EAST and why and I using capitals?  In programming it is common to map words to constants and when we do that we often use all capitals to indicate that's what is going on. The way we do this in python is simple. 

.. activecode:: m_const

   EAST=0
   NORTH=1
   WEST=2
   SOUTH=3

If we do this, it makes it easier since we don't have to remember 0 is East. So we know we want one argument for *dig*.  What do we want back?  If we get back the position of the turtle, we can tell if it succeeded in moving and we can tell where it is also. After a reset we should be able to dig East. So calling m.dig(EAST) should return (-170,190).  Now we know how to write our test. 

.. activecode:: m_test_dig

   import turtle
   EAST=0;NORTH=1;WEST=2;SOUTH=3
   class Maze(object):
      """ Solves a maze using a 20x20 matrix as an internal model
             and a 400x400 screen graphical view. 
          reset() puts the turtle in the upper left hand corner.
      """
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
      def dig(self,direction):
         pass

   m=Maze()
   m.reset()
   r=m.dig(EAST)
   assert r==(-170,190), "got " + str(r)

To create a passing test, we need to add the code for *dig*. One thing that becomes very obvious is that we need to map the position of the turtle into the matrix locations because we can't use the turtle position to index the matrix directly. What would be convenient is to be able to access the matrix with the turtle position.  Something like 

.. activecode:: m_access_matrix

   import turtle
   EAST=0;NORTH=1;WEST=2;SOUTH=3
   class Maze(object):
      """ Solves a maze using a 20x20 matrix as an internal model
             and a 400x400 screen graphical view. 
          reset() puts the turtle in the upper left hand corner.
      """
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
      def dig(self,direction):
         pass

   m=Maze()
   m.reset()
   value=m.getMatrixValueAt(m.turtle.position) 
   m.setMatrixValueAt(m.turtle.position,value)

At reset conditions, the matrix value would be 0 at [0][0] because we have a space there.  Our test should be 

.. activecode:: m_test_map


  m.reset()
  assert m.getMatrixValueAt(m.turtle.position)==0

Make it pass. 

.. activecode:: m_test_dig

   import turtle
   EAST=0;NORTH=1;WEST=2;SOUTH=3
   class Maze(object):
      """ Solves a maze using a 20x20 matrix as an internal model
             and a 400x400 screen graphical view. 
          reset() puts the turtle in the upper left hand corner.
          getMatrixValueAt(position) returns the matrix value at the tuple position
      """
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

   m=Maze()
   m.reset()
   assert m.getMatrixValueAt(m.turtle.position())==0
   # we are putting this test on hold for now
   # assert m.dig(EAST)==(-170,190)


Now for setMatrixValueAt(pos).

.. activecode:: m_test_dig2

   import turtle
   EAST=0;NORTH=1;WEST=2;SOUTH=3
   class Maze(object):
      """ Solves a maze using a 20x20 matrix as an internal model
             and a 400x400 screen graphical view. 
          reset() puts the turtle in the upper left hand corner.
          getMatrixValueAt(position) returns the matrix value at the tuple position
      """
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
         return True

   m=Maze()
   m.reset()
   m.reset()
   assert m.getMatrixValueAt(m.turtle.position())==0
   assert m.setMatrixValueAt(m.turtle.position(),1)==True
   assert m.matrix[0][0]==1
   # we are putting this test on hold for now
   # assert m.dig(EAST)==(-170,190)


Nice! Now we can just use our turtle position to set the matrix. But after we set the matrix to 1, we should see the white square dissappear if it properly represents our matrix. Let's fix that.


.. activecode:: m_test_dig3   

   import turtle
   EAST=0;NORTH=1;WEST=2;SOUTH=3
   class Maze(object):
      """ Solves a maze using a 20x20 matrix as an internal model
             and a 400x400 screen graphical view. 
          reset() puts the turtle in the upper left hand corner.
          getMatrixValueAt(position) returns the matrix value at the tuple position
      """
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

   m=Maze()
   m.reset()
   m.reset()
   assert m.getMatrixValueAt(m.turtle.position())==0
   assert m.setMatrixValueAt(m.turtle.position(),1)==True
   assert m.matrix[0][0]==1
   # we are putting this test on hold for now
   # assert m.dig(EAST)==(-170,190)

Now we can map turtle position to matrix element. Remember we are trying to implement *dig* ultimately. Let's  manually do a little digging. 

.. activecode:: m_test_dig4   

   import turtle
   EAST=0;NORTH=1;WEST=2;SOUTH=3
   class Maze(object):
      """ Solves a maze using a 20x20 matrix as an internal model
             and a 400x400 screen graphical view. 
          reset() puts the turtle in the upper left hand corner.
          getMatrixValueAt(position) returns the matrix value at the tuple position
      """
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

   m=Maze()
   m.reset()

   m.turtle.goto(-170,190)
   m.turtle.stamp()
   m.setMatrixValueAt(m.turtle.position(),0)

So now with this code we see that digging east moves the turtle to -170,190 and sets the value of the matrix at that point to 0. 

Let's add our test and code to make it pass. 

.. activecode:: m_test_dig5

   import turtle
   EAST=0;NORTH=1;WEST=2;SOUTH=3
   class Maze(object):
      """ Solves a maze using a 20x20 matrix as an internal model
             and a 400x400 screen graphical view. 
          reset() puts the turtle in the upper left hand corner.
          getMatrixValueAt(position) returns the matrix value at the tuple position
      """
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
      def dig(self,dir):
	if dir == EAST:
	  self.turtle.goto(self.turtle.position()[0]+20,self.turtle.position()[1])
	  self.setMatrixValueAt(self.turtle.position(),0)
	return self.turtle.position()

      def getMatrixValueAt(self,pos):
         x=int((pos[0]+200)/20)
         y=20-int((pos[1]+200)/20)-1
         v=self.matrix[x][y]
         return v
      def setMatrixValueAt(self,pos,value):
         y=int((pos[0]+200)/20)
         x=20-int((pos[1]+200)/20)-1
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

   m=Maze()
   m.reset()
   m.dig(EAST)
   assert m.getMatrixValueAt(m.turtle.position())==0
   assert m.turtle.position() == (-170,190)


   
Now let's do a reset and dig south.  I'm showing both the test and the code to make it pass here. 

.. activecode:: m_test_dig6

   import turtle
   EAST=0;NORTH=1;WEST=2;SOUTH=3
   class Maze(object):
      """ Solves a maze using a 20x20 matrix as an internal model
             and a 400x400 screen graphical view. 
          reset() puts the turtle in the upper left hand corner.
          getMatrixValueAt(position) returns the matrix value at the tuple position
      """
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
      def dig(self,dir):
	if dir == EAST:
	  self.turtle.goto(self.turtle.position()[0]+20,self.turtle.position()[1])
	  self.setMatrixValueAt(self.turtle.position(),0)
	elif dir == SOUTH:
	  self.turtle.goto(self.turtle.position()[0],self.turtle.position()[1]-20)
	  self.setMatrixValueAt(self.turtle.position(),0)

	return self.turtle.position()


      def getMatrixValueAt(self,pos):
         x=int((pos[0]+200)/20)
         y=20-int((pos[1]+200)/20)-1
         v=self.matrix[x][y]
         return v
      def setMatrixValueAt(self,pos,value):
         y=int((pos[0]+200)/20)
         x=20-int((pos[1]+200)/20)-1
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

   m=Maze()
   m.reset()
   m.dig(SOUTH)
   assert m.getMatrixValueAt(m.turtle.position())==0
   assert m.turtle.position() == (-190,170)

We can't dig west from the reset condition so let's make sure that is understood by the function.  We need to assert that digging west just returns the original location of the turtle so we know it didn't move. Note that the previous code is included in the following. 

.. activecode:: m_test_dig7
   :include: m_test_dig6

   m=Maze()
   m.reset()
   assert m.dig(WEST) == (-190,190)


Well this test actually passed without us doing anything but it's just a fluke because we ignore WEST and in this case that's what we want to do.  Let's get a little more involved with our testing.  We can go East and South, so let's try going East, South, and then West.  We should see our failure then. 

.. activecode:: m_test_dig9

   import turtle
   EAST=0;NORTH=1;WEST=2;SOUTH=3
   class Maze(object):
      """ Solves a maze using a 20x20 matrix as an internal model
             and a 400x400 screen graphical view. 
          reset() puts the turtle in the upper left hand corner.
          getMatrixValueAt(position) returns the matrix value at the tuple position
      """
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
      def dig(self,dir):
	if dir == EAST:
	  self.turtle.goto(self.turtle.position()[0]+20,self.turtle.position()[1])
	  self.setMatrixValueAt(self.turtle.position(),0)
	elif dir == SOUTH:
	  self.turtle.goto(self.turtle.position()[0],self.turtle.position()[1]-20)
	  self.setMatrixValueAt(self.turtle.position(),0)

	return self.turtle.position()


      def getMatrixValueAt(self,pos):
         x=int((pos[0]+200)/20)
         y=20-int((pos[1]+200)/20)-1
         v=self.matrix[x][y]
         return v
      def setMatrixValueAt(self,pos,value):
         y=int((pos[0]+200)/20)
         x=20-int((pos[1]+200)/20)-1
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

   m=Maze()
   m.reset()
   m.dig(EAST)
   m.dig(SOUTH)
   r=m.dig(WEST)
   assert r == (-190,170), "should be at (-190,170) but got " + str(r)


Of course we can see how ignoring WEST was just a fluke here. Sometimes writing tests is a little more involved than at first perceived.  Now let's get this test to pass. 

.. activecode:: m_test_dig10

   import turtle
   EAST=0;NORTH=1;WEST=2;SOUTH=3
   class Maze(object):
      """ Solves a maze using a 20x20 matrix as an internal model
             and a 400x400 screen graphical view. 
          reset() puts the turtle in the upper left hand corner.
          getMatrixValueAt(position) returns the matrix value at the tuple position
      """
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
      def dig(self,dir):
	if dir == EAST:
	  if self.turtle.position()[0]<190:
	    self.turtle.goto(self.turtle.position()[0]+20,self.turtle.position()[1])
	    self.setMatrixValueAt(self.turtle.position(),0)
	elif dir == SOUTH:
	  if self.turtle.position()[1]>-190:
	    self.turtle.goto(self.turtle.position()[0],self.turtle.position()[1]-20)
	    self.setMatrixValueAt(self.turtle.position(),0)
	elif dir ==  WEST:
	  if self.turtle.position()[0]>-190:
	    self.turtle.goto(self.turtle.position()[0]-20,self.turtle.position()[1])
	    self.setMatrixValueAt(self.turtle.position(),0)
	return self.turtle.position()


      def getMatrixValueAt(self,pos):
         x=int((pos[0]+200)/20)
         y=20-int((pos[1]+200)/20)-1
         v=self.matrix[x][y]
         return v
      def setMatrixValueAt(self,pos,value):
         y=int((pos[0]+200)/20)
         x=20-int((pos[1]+200)/20)-1
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

   m=Maze()
   m.reset()
   m.dig(EAST)
   m.dig(SOUTH)
   r=m.dig(WEST)
   assert r == (-190,170), "should be at (-190,170) but got " + str(r)


We have dug ourselves a nice square. One last direction to test, NORTH.  Here's both the test and the solution. 


.. activecode:: m_test_dig11

   import turtle
   EAST=0;NORTH=1;WEST=2;SOUTH=3
   class Maze(object):
      """ Solves a maze using a 20x20 matrix as an internal model
             and a 400x400 screen graphical view. 
          reset() puts the turtle in the upper left hand corner.
          getMatrixValueAt(position) returns the matrix value at the tuple position
      """
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
      def dig(self,dir):
	if dir == EAST:
	  if self.turtle.position()[0]<190:
	    self.turtle.goto(self.turtle.position()[0]+20,self.turtle.position()[1])
	    self.setMatrixValueAt(self.turtle.position(),0)
	elif dir == SOUTH:
	  if self.turtle.position()[1]>-190:
	    self.turtle.goto(self.turtle.position()[0],self.turtle.position()[1]-20)
	    self.setMatrixValueAt(self.turtle.position(),0)
	elif dir ==  WEST:
	  if self.turtle.position()[0]>-190:
	    self.turtle.goto(self.turtle.position()[0]-20,self.turtle.position()[1])
	    self.setMatrixValueAt(self.turtle.position(),0)
	elif dir ==  NORTH:
	  if self.turtle.position()[1]<190:
	    self.turtle.goto(self.turtle.position()[0],self.turtle.position()[1]+20)
	    self.setMatrixValueAt(self.turtle.position(),0)
	return self.turtle.position()


      def getMatrixValueAt(self,pos):
         x=int((pos[0]+200)/20)
         y=20-int((pos[1]+200)/20)-1
         v=self.matrix[x][y]
         return v
      def setMatrixValueAt(self,pos,value):
         y=int((pos[0]+200)/20)
         x=20-int((pos[1]+200)/20)-1
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

   m=Maze()
   m.reset()
   m.dig(EAST)
   m.dig(SOUTH)
   m.dig(WEST)
   r=m.dig(NORTH)
   assert r == (-190,190), "should be at (-190,190) but got " + str(r)


Here is our Maze class. 

.. activecode:: m_maze_class

   import turtle
   EAST=0;NORTH=1;WEST=2;SOUTH=3
   class Maze(object):
      """ Solves a maze using a 20x20 matrix as an internal model
             and a 400x400 screen graphical view. 
          reset() puts the turtle in the upper left hand corner.
          getMatrixValueAt(position) returns the matrix value at the tuple position
      """
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
      def dig(self,dir):
	if dir == EAST:
	  if self.turtle.position()[0]<190:
	    self.turtle.goto(self.turtle.position()[0]+20,self.turtle.position()[1])
	    self.setMatrixValueAt(self.turtle.position(),0)
	elif dir == SOUTH:
	  if self.turtle.position()[1]>-190:
	    self.turtle.goto(self.turtle.position()[0],self.turtle.position()[1]-20)
	    self.setMatrixValueAt(self.turtle.position(),0)
	elif dir ==  WEST:
	  if self.turtle.position()[0]>-190:
	    self.turtle.goto(self.turtle.position()[0]-20,self.turtle.position()[1])
	    self.setMatrixValueAt(self.turtle.position(),0)
	elif dir ==  NORTH:
	  if self.turtle.position()[1]<190:
	    self.turtle.goto(self.turtle.position()[0],self.turtle.position()[1]+20)
	    self.setMatrixValueAt(self.turtle.position(),0)
	return self.turtle.position()


      def getMatrixValueAt(self,pos):
         x=int((pos[0]+200)/20)
         y=20-int((pos[1]+200)/20)-1
         v=self.matrix[x][y]
         return v
      def setMatrixValueAt(self,pos,value):
         y=int((pos[0]+200)/20)
         x=20-int((pos[1]+200)/20)-1
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


Our code examples will now just include that invisibly and we will override functions. 

We now have our dig method.  We can dig in all 4 directions.  There are more tests we can add for more complete confidence in the method but for now, let's move on.   We may go back and add some more tests for *dig* if we find things are breaking. 

One thing we need to be careful about when digging our paths in the maze is that we need to make sure we don't go into another preexisting path.  Our tests make a big square in the upper left hand corner but we really don't want that to happen.  We want some wall between paths.  Lets prevent digging if it means we connect to a preexisting path.  This means that the 3 locations surrounding the new space must be walls.  Spaces outside the boundary of the screen are considered walls.  

How do we test this? If we make a space at location m.matrix[0][2] then we should not be able to dig EAST from m.matrix[0][0].  

.. activecode:: m_dig_noconnect_test
   :include: m_maze_class

   class Maze2(Maze):
      """ Solves a maze using a 20x20 matrix as an internal model
             and a 400x400 screen graphical view. 
          reset() puts the turtle in the upper left hand corner.
          getMatrixValueAt(position) returns the matrix value at the tuple position
      """
      def dig(self,dir):
	if dir == EAST:
	  if self.turtle.position()[0]<190:
	    if self.getMatrixValueAt((self.turtle.position()[0]+40,self.turtle.position()[1]))>0:
	      self.turtle.goto(self.turtle.position()[0]+20,self.turtle.position()[1])
	      self.setMatrixValueAt(self.turtle.position(),0)
	elif dir == SOUTH:
	  if self.turtle.position()[1]>-190:
	    self.turtle.goto(self.turtle.position()[0],self.turtle.position()[1]-20)
	    self.setMatrixValueAt(self.turtle.position(),0)
	elif dir ==  WEST:
	  if self.turtle.position()[0]>-190:
	    self.turtle.goto(self.turtle.position()[0]-20,self.turtle.position()[1])
	    self.setMatrixValueAt(self.turtle.position(),0)
	elif dir ==  NORTH:
	  if self.turtle.position()[1]<190:
	    self.turtle.goto(self.turtle.position()[0],self.turtle.position()[1]+20)
	    self.setMatrixValueAt(self.turtle.position(),0)
	return self.turtle.position()


   m=Maze2()
   m.reset()
   m.setMatrixValueAt((-150,190),0)
   r=m.dig(EAST)
   assert r==(-190,190),"Not at Home position, got " + str(r)


This passes but why don't we see the white square appearing at location (-150,190)?  We assumed the turtle was where it should be to stamp the value but we need to move the turtle to that location first and then move the turtle back. So we correct the setMatrixValueAt method. 

.. activecode:: m_dig_noconnect_test2
   :include: m_maze_class

   class Maze2(Maze):
      """ Solves a maze using a 20x20 matrix as an internal model
             and a 400x400 screen graphical view. 
          reset() puts the turtle in the upper left hand corner.
          getMatrixValueAt(position) returns the matrix value at the tuple position
      """
      def dig(self,dir):
	if dir == EAST:
	  if self.turtle.position()[0]<190:
	    if self.getMatrixValueAt((self.turtle.position()[0]+40,self.turtle.position()[1]))>0:
	      self.turtle.goto(self.turtle.position()[0]+20,self.turtle.position()[1])
	      self.setMatrixValueAt(self.turtle.position(),0)
	elif dir == SOUTH:
	  if self.turtle.position()[1]>-190:
	    self.turtle.goto(self.turtle.position()[0],self.turtle.position()[1]-20)
	    self.setMatrixValueAt(self.turtle.position(),0)
	elif dir ==  WEST:
	  if self.turtle.position()[0]>-190:
	    self.turtle.goto(self.turtle.position()[0]-20,self.turtle.position()[1])
	    self.setMatrixValueAt(self.turtle.position(),0)
	elif dir ==  NORTH:
	  if self.turtle.position()[1]<190:
	    self.turtle.goto(self.turtle.position()[0],self.turtle.position()[1]+20)
	    self.setMatrixValueAt(self.turtle.position(),0)
	return self.turtle.position()
      def setMatrixValueAt(self,pos,value):
         y=int((pos[0]+200)/20)
         x=20-int((pos[1]+200)/20)-1
	 try:
	    self.matrix[y][x]=value
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


   m=Maze2()
   m.reset()
   m.setMatrixValueAt((-150,190),0)
   r=m.dig(EAST)
   assert r==(-190,190),"Not at Home position, got " + str(r)


Now we see the white square at (-150,190).  I will leave it to you to handle the other directions. After you are done, you should have a class that looks like this. 

.. activecode:: m_maze_class_2

   import turtle
   EAST=0;NORTH=1;WEST=2;SOUTH=3
   class Maze(object):
      """ Solves a maze using a 20x20 matrix as an internal model
             and a 400x400 screen graphical view. 
          reset() puts the turtle in the upper left hand corner.
          getMatrixValueAt(position) returns the matrix value at the tuple position
      """
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
      def dig(self,dir):
        if dir == EAST:
          if self.turtle.position()[0]<190:
            if self.turtle.position()[0]+40 > 190:
               return self.turtle.position
            if self.getMatrixValueAt((self.turtle.position()[0]+40,self.turtle.position()[1]))>0:
              self.turtle.goto(self.turtle.position()[0]+20,self.turtle.position()[1])
              self.setMatrixValueAt(self.turtle.position(),0)
        elif dir == SOUTH:
          if self.turtle.position()[1]>-190:
            if self.turtle.position()[1]-40 < -190:
              return self.turtle.position()
            if self.getMatrixValueAt((self.turtle.position()[0],self.turtle.position()[1]-40))>0:
              self.turtle.goto(self.turtle.position()[0],self.turtle.position()[1]-20)
              self.setMatrixValueAt(self.turtle.position(),0)
        elif dir ==  WEST:
          if self.turtle.position()[0]>-190:
            if self.turtle.position()[0]-40 < -190:
              return self.turtle.position()
            if self.getMatrixValueAt((self.turtle.position()[0]-40,self.turtle.position()[1]))>0:
              self.turtle.goto(self.turtle.position()[0]-20,self.turtle.position()[1])
              self.setMatrixValueAt(self.turtle.position(),0)
        elif dir ==  NORTH:
          if self.turtle.position()[1]<190:
            if self.turtle.position()[1]+40 > 190:
              return self.turtle.position()
            if self.getMatrixValueAt((self.turtle.position()[0],self.turtle.position()[1]+40))>0:
              self.turtle.goto(self.turtle.position()[0],self.turtle.position()[1]+20)
              self.setMatrixValueAt(self.turtle.position(),0)
        return self.turtle.position()
      def setMatrixValueAt(self,pos,value):
         x=int((pos[0]+200)/20)
         y=20-int((pos[1]+200)/20)-1
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
         x=int((pos[0]+200)/20)
         y=20-int((pos[1]+200)/20)-1
	 if (pos[0]+200)/20<0 or x>19:
	     return -1
	 if y<0 or y>19: 
             return -1
         v=self.matrix[x][y]
         return v
      

And the tests. 

.. activecode:: m_test_dig2path 
   :include: m_maze_class_2

   m=Maze()
   m.reset()
   m.setMatrixValueAt((-190,150),0)
   print m.turtle.position()
   r=m.dig(SOUTH)
   assert r==(-190,190),"got " + str(r)
   m.setMatrixValueAt((-150,190),0)
   r=m.dig(EAST)
   assert r==(-190,190),"got " + str(r)
   m.turtle.goto(-150,150)
   r=m.dig(WEST)
   assert r==(-150,150),"got " + str(r)
   m.turtle.goto(-190,150)
   r=m.dig(NORTH)
   assert r==(-190,150),"got " + str(r)
   m.reset()
   r=m.dig(NORTH)
   assert r==(-190,190),"got " + str(r)
   m.turtle.goto(-190,-170)
   print m.turtle.position()[1]-20
   r=m.dig(SOUTH)
   assert r==(-190,-170),"got " + str(r)


Again, there could be more testing. It's a judgement call as to how much you want to test. How much energy you have and how important something is, etc. 

Now it's a good idea to not reinvent the wheel! Look up algorithms for maze generation and you will find a number of web sites.  We will use the depth-first search algorithm 

(https://en.wikipedia.org/wiki/Maze_generation_algorithm)

1. Start at the upper left hand corner
2. Mark that cell as visited and get a list of its neighbors.  For each neighbor, starting with a randomly selected neighbor
	- if that neighbor hasn't been visited, remove the wall between this cell and that neighborand then recur with that neighbor as the current cell. 

It might be nice to have a method called *neighbors* which returns the state of the cells neighboring the current cell. 

*neighbors* should return 4 values, the neighbors in all 4 directions.  At the boundaries, the values outside the matrix should be -1 to indicate invalid locations. 

A neighbor is actually 2 cells away since walls take up a cell's width. 

At reset condition then, *neighbors* should return [-1,1,1,-1] for the NORTH, SOUTH, EAST, and WEST neighbors.  



.. activecode:: m_test_digPath_1
   :include: m_maze_class_2

   m=Maze()
   m.reset()
   assert m.neighbors()==[-1,1,1,-1]

Now to implement.

.. activecode:: m_test_digPath_2   
   :include: m_maze_class_2
   
   class NewMaze(Maze):
      def neighbors(self):
	p=self.turtle.position()
	r=[]
	r.append([(p[0],p[1]+40),m.getMatrixValueAt((p[0],p[1]+40))])
	r.append([(p[0],p[1]-40),m.getMatrixValueAt((p[0],p[1]-40))])
	r.append([(p[0]+40,p[1]),m.getMatrixValueAt((p[0]+40,p[1]))])
	r.append([(p[0]-40,p[1]),m.getMatrixValueAt((p[0]-40,p[1]))])
        return r

   m=NewMaze()
   m.reset()
   r = m.neighbors()
   assert (r[0][1]==-1 and r[1][1]==1 and r[2][1]==1 and r[3][1]==-1),"got " + str(r)
   m.turtle.goto(-170,170)
   r = m.neighbors()
   assert (r[0][1]==-1 and r[1][1]==1 and r[2][1]==1 and r[3][1]==-1),"got " + str(r)
   m.turtle.goto(-150,150)
   r = m.neighbors()
   assert (r[0][1]==1 and r[1][1]==1 and r[2][1]==1 and r[3][1]==1), "got " + str(r)

Now that we have added neighbors, let's put it into our Maze class rather than just overloading it. 

.. activecode:: m_maze_class_3

   import turtle
   EAST=0;NORTH=1;WEST=2;SOUTH=3
   class Maze(object):
      """ Solves a maze using a 20x20 matrix as an internal model
             and a 400x400 screen graphical view. 
          reset() puts the turtle in the upper left hand corner.
          getMatrixValueAt(position) returns the matrix value at the tuple position
      """
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
          if self.turtle.position()[0]<190:
            if self.turtle.position()[0]+40 > 190:
               return self.turtle.position
            if self.getMatrixValueAt((self.turtle.position()[0]+40,self.turtle.position()[1]))>0:
              self.turtle.goto(self.turtle.position()[0]+20,self.turtle.position()[1])
              self.setMatrixValueAt(self.turtle.position(),0)
        elif dir == SOUTH:
          if self.turtle.position()[1]>-190:
            if self.turtle.position()[1]-40 < -190:
              return self.turtle.position()
            if self.getMatrixValueAt((self.turtle.position()[0],self.turtle.position()[1]-40))>0:
              self.turtle.goto(self.turtle.position()[0],self.turtle.position()[1]-20)
              self.setMatrixValueAt(self.turtle.position(),0)
        elif dir ==  WEST:
          if self.turtle.position()[0]>-190:
            if self.turtle.position()[0]-40 < -190:
              return self.turtle.position()
            if self.getMatrixValueAt((self.turtle.position()[0]-40,self.turtle.position()[1]))>0:
              self.turtle.goto(self.turtle.position()[0]-20,self.turtle.position()[1])
              self.setMatrixValueAt(self.turtle.position(),0)
        elif dir ==  NORTH:
          if self.turtle.position()[1]<190:
            if self.turtle.position()[1]+40 > 190:
              return self.turtle.position()
            if self.getMatrixValueAt((self.turtle.position()[0],self.turtle.position()[1]+40))>0:
              self.turtle.goto(self.turtle.position()[0],self.turtle.position()[1]+20)
              self.setMatrixValueAt(self.turtle.position(),0)
        return self.turtle.position()
      def setMatrixValueAt(self,pos,value):
         x=int((pos[0]+200)/20)
         y=20-int((pos[1]+200)/20)-1
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
         x=int((pos[0]+200)/20)
         y=20-int((pos[1]+200)/20)-1
	 if (pos[0]+200)/20<0 or x>19:
	     return -1
	 if ((pos[1]+200)/20)>19.5 or ((pos[1]+200)/20)<0:
             return -1
         v=self.matrix[x][y]
         return v

            
Now with these constants added we can make the code a little more readable. 

.. activecode:: cnst2
	:include: m_maze_class_3

	INVALID = -1
	EMPTY = 0
	WALL = 1
	VISITED = 2
	END = 3

	m=Maze()
	m.reset()
	r = m.neighbors()
	assert (r[0][1]==INVALID and r[1][1]==WALL and r[2][1]==WALL and r[3][1]==INVALID),"got " + str(r)
	m.turtle.goto(-170,170)
	r = m.neighbors()
	assert (r[0][1]==INVALID and r[1][1]==WALL and r[2][1]==WALL and r[3][1]==INVALID),"got " + str(r)
	m.turtle.goto(-150,150)
	r = m.neighbors()
	assert (r[0][1]==WALL and r[1][1]==WALL and r[2][1]==WALL and r[3][1]==WALL), "got " + str(r)

We are now ready to start implementing the algorithm.  We will call the method create().  It will be recursively calling itself but to start we will just have it run one iteration.  That way we can test it. 

Our Maze class as it stands now. 

.. activecode:: m_maze_class_4

	INVALID = -1
	EMPTY = 0
	WALL = 1
	VISITED = 2
	END = 3

	
        import turtle
        import random
        EAST=0;NORTH=1;WEST=2;SOUTH=3
        class Maze(object):
	    """ Solves a maze using a 20x20 matrix as an internal model
		     and a 400x400 screen graphical view. 
		  reset() puts the turtle in the upper left hand corner.
		  getMatrixValueAt(position) returns the matrix value at the tuple position
	    """

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
                    if self.turtle.position()[0]<190:
                        if self.turtle.position()[0]+20 > 190:
                            return self.turtle.position
                    if self.getMatrixValueAt((self.turtle.position()[0]+20,self.turtle.position()[1]))>0:
                        self.turtle.goto(self.turtle.position()[0]+20,self.turtle.position()[1])
                        self.setMatrixValueAt(self.turtle.position(),0)
                elif dir == SOUTH:
                    if self.turtle.position()[1]>-190:
                        if self.turtle.position()[1]-20 < -190:
                            return self.turtle.position()
                    if self.getMatrixValueAt((self.turtle.position()[0],self.turtle.position()[1]-20))>0:
                        self.turtle.goto(self.turtle.position()[0],self.turtle.position()[1]-20)
                        self.setMatrixValueAt(self.turtle.position(),0)
                elif dir ==  WEST:
                    if self.turtle.position()[0]>-190:
                        if self.turtle.position()[0]-20 < -190:
                            return self.turtle.position()
                    if self.getMatrixValueAt((self.turtle.position()[0]-20,self.turtle.position()[1]))>0:
                        self.turtle.goto(self.turtle.position()[0]-20,self.turtle.position()[1])
                        self.setMatrixValueAt(self.turtle.position(),0)
                elif dir ==  NORTH:
                    if self.turtle.position()[1]<190:
                        if self.turtle.position()[1]+20 > 190:
                            return self.turtle.position()
                    if self.getMatrixValueAt((self.turtle.position()[0],self.turtle.position()[1]+20))>0:
                        self.turtle.goto(self.turtle.position()[0],self.turtle.position()[1]+20)
                        self.setMatrixValueAt(self.turtle.position(),0)
                return self.turtle.position()

            def setMatrixValueAt(self,pos,value):
                x=int((pos[0]+200)/20)
                y=20-int((pos[1]+200)/20)-1
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
                x=int((pos[0]+200)/20)
                y=20-int((pos[1]+200)/20)-1
                if (pos[0]+200)/20<0 or x>19:
                    return -1
                if ((pos[1]+200)/20)>19.5 or ((pos[1]+200)/20)<0:
                    return -1
                v=self.matrix[x][y]
                return v

Let's just say for test number one, we will have the first part dug. So either it will be a path to the right or a path down.  Our test should check both directions and see if one has been successfully dug. 

.. activecode:: m_test_create_1
	:include: m_maze_class_4

        def direction(pos1,pos2):
            """ returns the direction from position 1 to position 2 """
            if pos1[0]==pos2[0]: # x position the same, either NORTH or SOUTH
                if pos1[1]>pos2[1]: # NORTH
                    return NORTH
                else:
                    return SOUTH
            else:
                if pos2[0]>pos1[0]: # EAST
                    return EAST
                else:
                    return WEST
                

        class Maze2(Maze):
            def makeMaze(self):
                n=self.neighbors()
                while len(n)>0:
                    nchoice=random.choice(n)
                    n.remove(nchoice)
                    if nchoice[1]==WALL:
                        d=direction(self.turtle.position(),nchoice[0])
                        self.dig(d)
                        self.dig(d)
                        return

        m=Maze2()
        m.reset()
        m.makeMaze()
        assert ((m.getMatrixValueAt((-170,190))==EMPTY and m.getMatrixValueAt((-150,190))==EMPTY) or  \
               (m.getMatrixValueAt((-190,170))==EMPTY and m.getMatrixValueAt((-190,150))==EMPTY)),"got " + \
               str(m.getMatrixValueAt((-170,190))) + "," + \
               str(m.getMatrixValueAt((-150,190))) + "," + \
               str(m.getMatrixValueAt((-190,170))) + "," + \
               str(m.getMatrixValueAt((-190,150)))
        
               
Now the algorithm says we should recur what we just did. So let's try. 

.. activecode:: m_test_create_2
	:include: m_maze_class_4

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
                

        class Maze2(Maze):
            def makeMaze(self):
                n=self.neighbors() # get the 4 neighbors. 
                # save the position of the turtle
                # we need to start there for each neighbors
                oldpos=self.turtle.position()
                while len(n)>0:
                    nchoice=random.choice(n) 
                    n.remove(nchoice) # remove so eventually the length will be 0
                    self.turtle.goto(oldpos) 
                    # we must use getMatrixValueAt rather than the value in nchoice
                    # because it may have changed from a prior recursive call.
                    if self.getMatrixValueAt(nchoice[0])==WALL: 
                        d=direction(self.turtle.position(),nchoice[0])
                        self.dig(d) # this removes the wall
                        self.dig(d) # this is the next occupied cell. 
			self.makeMaze() # recursively do it again from the new cell
	

	import sys
	sys.setExecutionLimit(50000)
        m=Maze2()
        m.reset()
        m.makeMaze()
        assert ((m.getMatrixValueAt((-170,190))==EMPTY and m.getMatrixValueAt((-150,190))==EMPTY) or  \
               (m.getMatrixValueAt((-190,170))==EMPTY and m.getMatrixValueAt((-190,150))==EMPTY)),"got " + \
               str(m.getMatrixValueAt((-170,190))) + "," + \
               str(m.getMatrixValueAt((-150,190))) + "," + \
               str(m.getMatrixValueAt((-190,170))) + "," + \
               str(m.getMatrixValueAt((-190,150)))

Hooray!


Now let's put it all together in our Maze model

.. activecode:: m_maze_class_5


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
	    """ Solves a maze using a 20x20 matrix as an internal model
		     and a 400x400 screen graphical view. 
		  reset() puts the turtle in the upper left hand corner.
		  getMatrixValueAt(position) returns the matrix value at the tuple position
	    """
            
            def __init__(self):
                self.screen=turtle.Screen()
                self.turtle=turtle.Turtle()
                self.screen.bgcolor('blue')
                self.matrix=[[1 for i in range(20)] for i in range(20)]
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
                self.turtle.goto(-190,190)
                self.matrix=[[1 for i in range(20)] for i in range(20)]
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
                    if self.turtle.position()[0]<190:
                        if self.turtle.position()[0]+20 > 190:
                            return self.turtle.position
                    if self.getMatrixValueAt((self.turtle.position()[0]+20,self.turtle.position()[1]))>0:
                        self.turtle.goto(self.turtle.position()[0]+20,self.turtle.position()[1])
                        self.setMatrixValueAt(self.turtle.position(),0)
                elif dir == SOUTH:
                    if self.turtle.position()[1]>-190:
                        if self.turtle.position()[1]-20 < -190:
                            return self.turtle.position()
                    if self.getMatrixValueAt((self.turtle.position()[0],self.turtle.position()[1]-20))>0:
                        self.turtle.goto(self.turtle.position()[0],self.turtle.position()[1]-20)
                        self.setMatrixValueAt(self.turtle.position(),0)
                elif dir ==  WEST:
                    if self.turtle.position()[0]>-190:
                        if self.turtle.position()[0]-20 < -190:
                            return self.turtle.position()
                    if self.getMatrixValueAt((self.turtle.position()[0]-20,self.turtle.position()[1]))>0:
                        self.turtle.goto(self.turtle.position()[0]-20,self.turtle.position()[1])
                        self.setMatrixValueAt(self.turtle.position(),0)
                elif dir ==  NORTH:
                    if self.turtle.position()[1]<190:
                        if self.turtle.position()[1]+20 > 190:
                            return self.turtle.position()
                    if self.getMatrixValueAt((self.turtle.position()[0],self.turtle.position()[1]+20))>0:
                        self.turtle.goto(self.turtle.position()[0],self.turtle.position()[1]+20)
                        self.setMatrixValueAt(self.turtle.position(),0)
                return self.turtle.position()

            def setMatrixValueAt(self,pos,value):
                x=int((pos[0]+200)/20)
                y=20-int((pos[1]+200)/20)-1
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
                x=int((pos[0]+200)/20)
                y=20-int((pos[1]+200)/20)-1
                if (pos[0]+200)/20<0 or x>19:
                    return -1
                if ((pos[1]+200)/20)>19.5 or ((pos[1]+200)/20)<0:
                    return -1
                v=self.matrix[x][y]
                return v

        import sys
        sys.setExecutionLimit(50000)
        
        m=Maze()
        m.makeMaze()
	m.turtle.goto(170,-170)
	m.turtle.color("yellow")
	m.turtle.stamp()

I'll leave that for you.


Next part: Part 2
Part 2: SOLVING THE MAZE

In this part, we will be adding to the Maze class to solve the maze we just built.




