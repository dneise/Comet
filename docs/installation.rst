Obtaining and Installing Comet
==============================

Installation using pip
----------------------

The latest version of Comet and all of the tools it depends upon can be
installed using `pip <https://pip.pypa.io/>`_. It is generally a good
idea to use `virtualenv <https://virtualenv.pypa.io/>`_ to create an isolated,
self-contained installation::

  $ virtualenv comet
  $ . comet/bin/activate
  $ pip install comet

Manual installation
-------------------

Requirements
^^^^^^^^^^^^

Comet is developed targeting Python 3.6 and later. It depends upon:

* `Twisted <https://twistedmatrix.com/>`_ (version 16.1.0 or later);
* `lxml <https://lxml.de/index.html>`_ (version 3.4.0 or later);
* `zope.interface <https://docs.zope.org/zope.interface/>`_ (version 4.1.1 or
  later);

How you make these dependencies available on your system is up to your (or,
perhaps, to your system administrator). However, the author strongly suggests
you might start by taking a look at `virtualenv
<https://virtualenv.pypa.io/>`_.

Downloading
^^^^^^^^^^^

See the :doc:`release history <history>` to obtain the latest version of Comet
or check out the source from the `GitHub repository
<https://www.github.com/jdswinbank/Comet>`_. The latest version of the source
can be obtained using `git <https://git-scm.org>`_::

  $ git clone https://github.com/jdswinbank/Comet.git

Installation
^^^^^^^^^^^^

Comet includes a `distutils <https://docs.python.org/distutils/index.html>`_
setup script which can be used for installation. To install in your
system-default location, run::

  $ python setup.py install

A number of other options are available: see also::

  $ python setup.py --help

Testing
-------

After installation, you should check that Comet is working properly. The
Twisted framework used by Comet makes this easy with its ``trial`` tool.
Simply run::

  $ trial comet

No failures or errors are expected in the test suite. If you see a problem,
please contact the author for help.
