

SiglentWaterfall
****************

============
Introduction
============

This program obtains trace information from a Siglent oscilloscope and
displays them as a three dimension plot displaying a scrolling history
of recent traces.  The plot can be rotated and zoomed in our out
using point devices. 

The application is written in *Python3* on and uses multi-programming
techniques to allow the program to use multiple cores.   

Communication with the oscilloscope uses the *visa* instrument control
infrastructure.    

=====
Usage
=====

To start the program from the command line, see the following usage.:

.. program-output:: siglent --help


For example:

.. code-block:: none

   siglent -n tcpip::192.168.1.201 -vv --waterfall   

Will start the *Siglent Waterfall* program reading from the
instrument at IP Address 192,168.1.201, being extremely verbose (debug
level), and will display both the 2D and 3D displays.

.. code-block:: none

   siglent -n tcpip::192.168.1.201 -v   

Will start the *Siglent Waterfall* program reading from the
instrument at IP Address 192,168.1.201, being a little verbose (info
level), and will display only 2D and 3D display.


SiglentWaterfall  Modules
*************************

====
Main
====

.. automodule:: __main__
   :members:

==========
Background
==========

.. automodule:: background
   :members:

===
Log
===

.. automodule:: log
   :members:

=========
TwoDGraph
=========
.. automodule:: TwoDGraph
   :members:

===========
ThreeDGraph
===========
.. automodule:: ThreeDGraph
   :members:

License
*******
This program is licensed under the MIT license.

Copyright (c) 2020 Eric Waller

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Third Party Software
********************

Run Time Dependencies
=====================

The following modules, not provided by Python or the *Siglent Waterfall*
repository, are required at run time and are installed automatically
by *pip*:

+------------------+-----------+------------------------+
| Module Name      | Version   | Description            |
+------------------+-----------+------------------------+
| Python           | 3.8       | Interpreter            |
+------------------+-----------+------------------------+
| Click            | 7.0       | Command line interface |
+------------------+-----------+------------------------+
| numpy            | 17.4      | Vector Math            |
+------------------+-----------+------------------------+
| PyOpenGL         | 3.1.0     | 3D graphics engine     |
+------------------+-----------+------------------------+
| PyQt5            | 5.13.2    | GUI subsystem          |
+------------------+-----------+------------------------+
| PyQt5-sip        | 12.7.0    | GUI subsystem          |
+------------------+-----------+------------------------+
| pyqtgraph        | 0.10.0    | graphing package       |
+------------------+-----------+------------------------+
| pyVISA           | 1.10.1    | Instrument control     |
+------------------+-----------+------------------------+
| scipy            | 1.3.3     | Vector math            |
+------------------+-----------+------------------------+

Build Time Dependencies
=======================

This program does use *Sphinx* to automatically generate
documentation from the *doc* strings in the Python code itself.
Sphinx can create man files, HTML files, pdf files, and others.  This
program uses the HTML documentation for the web application and pdf
files for written manuals.  It also generates man files for reference
when running on Linux from a command line.

The following top level modules are required to build the documentation for this
program suite.  These modules may have dependencies of their own and
are system dependent.  These are not automatically installed.

+------------------+------------+-----------------------------+------------------------+
| Module Name      | Version    | Organization                |Description             |
+------------------+------------+-----------------------------+------------------------+
| Sphinx           | 1.8.1      | http://www.sphinx-doc.org/  |Documentation Generator |
+------------------+------------+-----------------------------+------------------------+
| texlive          | 2018.48568 | http://tug.org/             | Web Template Engine    |
+------------------+------------+-----------------------------+------------------------+


To build the HTML documentation, from the root directory, run:

    *make html*

To build the pdf documentation, from the root directory, run:

    *make latexpdf*

To build the *man* documentation, from the root directory, run:

    *make man*

Indices and tables
******************

 :ref:`genindex`
 :ref:`modindex`
 :ref:`search`
