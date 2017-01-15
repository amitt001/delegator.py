Delegator.py — Subprocesses for Humans 2.0
=======================================

**Delegator.py** is a simple library for dealing with subprocesses, inspired
by both `envoy <https://github.com/kennethreitz/envoy>`_ and `pexpect <http://pexpect.readthedocs.io>`_ (in fact, it depends on it!).

This module features two main functions ``delegator.run()`` and ``delegator.chain()``. One runs commands, blocking or non-blocking, and the other runs a chain of commands, seperated by the standard unix pipe operator: ``|``.

Basic Usage
-----------

Basic run functionality:

.. code:: pycon

    >>> c = delegator.run('ls')
    >>> print c.out
    README.rst   delegator.py

    >>> c = delegator.run('long-running-process', block=False)
    >>> c.pid
    35199
    >>> c.block()
    >>> c.return_code
    0

Commands can be passed in as lists as well (e.g. ``['ls', '-lrt']``), for parameterization.

Basic chain functionality:

.. code:: pycon

   # Can also be called with ([['fortune'], ['cowsay']]).
   # or, delegator.run('fortune').pipe('cowsay')

   >>> c = delegator.chain('fortune | cowsay')
   >>> print c.out
     _______________________________________
    / Our swords shall play the orators for \
    | us.                                   |
    |                                       |
    \ -- Christopher Marlowe                /
     ---------------------------------------
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||


Expect functionality is built-in too, on non-blocking commands:

.. code:: pycon

    >>> c.expect('Password:')
    >>> c.send('PASSWORD')
    >>> c.block()

Other functions:

.. code:: pycon

    >>> c.kill()
    >>> c.send('SIGTERM', signal=True)

    # Only available when block=True, otherwise, use c.out.
    >>> c.err
    ''

    # Direct access to pipes.
    >>> c.std_err
    <open file '<fdopen>', mode 'rU' at 0x10a5351e0>

Daemonize anything!

.. code:: pycon

    # Turns the subprocess into a daemon.
    >>> c.daemonize()


Installation
------------

::

    $ pip install delegator.py
    
✨🍰✨
