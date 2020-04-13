================
Nurse Scheduling
================

This is a demo of a nurse scheduling algorithm developed by Ikeda, Nakamura
and Humble. The nurse scheduling problem seeks to find an optimal assignment
for a group of nurses, under constraints of scheduling and personnel.
The example is a simplified representation of a real-world nursing facility,
but the model includes many parameters which are not explored here.

There are three overall constraints in the full problem:

1) Both upper and lower limits on the number of breaks.
2) The number of nurses on duty for each shift slot.
3) For each individual nurse, upper and lower limits on the time interval 
between days of duty
The overall requirements combine to ensure that there are enough nurses
on duty at all times, and that the individual nurses are not expected to work
more than they can.

The "hard shift" constraint requires that at least one nurse is assigned for
each working day.
The "hard nurse" constraint ensures that no nurse works two or more 
consecutive days.
The "soft nurse" constraint requires that all nurses should have roughly
even work schedules.

Running the demo results in the following output:

    Size  33

    Energy  0.5999999999999694

    Checking Hard shift constraint  0.0

    Checking Hard nurse constraint  0.0

    Checking Soft nurse constraint  0.6

               0  1  2  3  4  5  6  7  8  9  10

    Nurse  0            X     X     X     X   

    Nurse  1      X        X     X           X

    Nurse  2   X     X                 X      


Usage
-----

A simple command that runs the demo. For example,

.. code-block:: bash

  python <demo_name>.py


Code Overview
-------------

A general overview of how the code works.

Prefer bite-sized descriptions in bullet points:

* Here's an example bullet point


Code Specifics
--------------

Notable parts of the code implementation.

This is the place to:

* Highlight a part of the code implementation
* Talk about unusual or potentially difficult parts of the code
* Explain a code decision

Note: there is no need to repeat everything that is already well-documented in
the code.


References
----------

Ikeda, K., Nakamura, Y. & Humble, T.S. 
Application of Quantum Annealing to Nurse Scheduling Problem. 
Sci Rep 9, 12837 (2019). 
https://doi.org/10.1038/s41598-019-49172-3

License
-------

Released under the Apache License 2.0. See `LICENSE <LICENSE>`_ file.
