Output
======

A Python module providing helpers for fancy looking shell output.
It is based on the output module found in Gentoo Linux but removes the
dependency on portage.


Classes
-------

``EOutput``
***********

Performs fancy terminal formatting for status and informational messages as
known by various init script implementations.

Example Usage:
^^^^^^^^^^^^^^

.. code-block:: python

    from output.eoutput import EOutput

    out = EOutput()
    out.ebegin('Starting skynet')
    out.eend(0)

The argument to ``EOutput.eend()`` is a standard UNIX errno code. ``0`` renders
a success and ``1`` or above a error status message.

In a real world example you would usually make the result dependent an a
certain condition or spit out a warning.

.. code-block:: python

    import random
    from output.eoutput import EOutput

    level = random.randint(50, 125)
    out = EOutput()

    out.ebegin('Starting skynet')
    if level > 75:
        if level < 100:
            out.ewarn('Link power level not at full capacity. Proceeding anyway.')
        out.eend(0)
    else:
        out.eend(1)


``TermProgressBar``
*******************

A tty progress bar similar to wget's.

Example Usage:
^^^^^^^^^^^^^^

.. code-block:: python

    from time import sleep
    from output.progress import TermProgressBar

    pb = TermProgressBar()
    for i in range(1, 100):
        pb.set(i, 100)
        sleep(0.01)


The progress bar can be useful when a routine takes some time to process and
isn't verbose about what's going on. Well - it's a progress bar.

.. code-block:: python

    import random
    from time import sleep
    from output.eoutput import EOutput
    from output.progress import TermProgressBar

    level = random.randint(50, 125)
    out = EOutput()

    out.ebegin('Starting skynet')
    if level > 75:
        if level < 100:
            out.ewarn('Link power level not at full capacity')
            out.einfo('Tranfering shield power to resonators')
            pb = TermProgressBar(title='Power transfer progress')
            for i in range(1, 100):
                pb.set(i, 99)
                sleep(0.05)
            print
        out.eend(0)
    else:
        out.eend(1)
