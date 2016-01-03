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

We will be solving a maze using test driven development techniques. 
The code should be able to be constructed here in the document. 

.. activecode:: m_test_1

   m=Maze() # see if a Maze class exists.

You should see an error when you run the code.
It's pretty ugly NameError:

Let's make it a little prettier. and use the try statement as follows: 

.. activecode:: m_try_1

   try:
      m=Maze()
   except:
      print "Maze class does not yet exist. CONDITION RED" 

Much better.

Now let's make this class exist. 

.. activecode:: m_class_1
 
   class Maze(object):
      """ Solves a maze """
      def __init__(self):
         pass

   error=False
   try:
      m=Maze()
   except:
      error=True
      print "Maze class does not yet exist." 
   if error:
      print "CONDITION RED"
   else:
      print "CONDITION GREEN"


We will use the turtle module to make our maze. The screen is created with the following command

.. activecode:: m_w_1

   import turtle
   wn = turtle.Screen()
   wn.bgcolor("lightblue")


When you run this code you will see the blue screen we created. A blue color means a wall. 
This is the visual representation of our maze. We don't have any paths created yet. It's all
wall. 

Now let's put this into the maze class. 

.. activecode:: m_class_2

   import turtle
   class Maze(object):
      """ creates a maze """
      def __init__(self):
         self.w = turtle.Screen()
         self.w.bgcolor('lightblue')

   m=Maze()

We need a turtle too. We kind of skipped a little of the TDD philosophy with the screen but now let's write a test for the turtle.  The turtle class is <class '__main__.Turtle'>.  

.. activecode:: m_test_turtle

   import turtle

   


Congratulations!   If you can see this file you have probably successfully run the ``runestone init`` command.  If you are looking at this as a source file you should now run ``runestone build``  to generate html files.   Once you have run the build command you can run ``runestone serve`` and then view this in your browser at ``http://localhost:8000``

This is just a sample of what you can do.  The index.rst file is the table of contents for your entire project.  You can put all of your writing in the index, or as you will see in the following section you can include additional rst files.  those files may even be in subdirectories that you can reference using a relative path.

The overview section, which follows is an ideal section to look at both online and at the source.  It is pretty easy to see how to write using any of the interactive features just by looking at the examples in ``overview.rst``


SECTION 2: An Overview of the extensions
::::::::::::::::::::::::::::::::::::::::

.. toctree::
   :maxdepth: 2

   overview.rst


SECTION 2: Add more stuff here
::::::::::::::::::::::::::::::

You can add more stuff here.


