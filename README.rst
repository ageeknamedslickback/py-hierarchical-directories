py-hierarchical-directories
===========================

Simple Python script to create, move and delete directories, or a simulation of the same.
A common method of organizing files on a computer is to store them in hierarchical directories. 
For instance:

.. code-block:: bash

    photos/
    birthdays/
        joe/
        mary/
    vacations/
    weddings/

How to run the CLI
==================

This assumes that you have `Python 3.10+` installed in your local machine

1. Navigate to where the code is located

.. code-block:: bash

    $ cd path/to/code

2. Run the Python script

.. code-block:: bash

    $ python3 directories.py

3. The program allows you to run commands e.g

.. code-block:: bash

    $ python3 directories.py
    CREATE photos/wedding/mike
    CREATE school/assignments/java
    LIST
    home/
     photos/
      wedding/
       mike/
    school/
     assignments/
      java/


CLI Commands
=============

CREATE
******

This command creates a directory or directories. It takes a path as an argument. The path is then used to
create the directories in a default root directory called `home`.

**How to use it**

.. code-block:: bash

    CREATE path
    CREATE path/to/dirs

DELETE
******

This command deletes/removes a directory or directories from the filesystem. It takes a path as an argument.

**How to use it**

.. code-block:: bash

    DELETE path
    DELETE path/to/dirs

LIST
****

This command displays a tree output of the current filesystem. It takes no arguments.

**How to use it**

.. code-block:: bash

    LIST 
    LIST

MOVE
****

This command is used to change the location of a directory or directories. 
It takes two arguments, the destination and the source (the dir(s) to be moved)

**How to use it**

.. code-block:: bash

    MOVE destination source 
    MOVE dir/to/destination source