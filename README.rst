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
between days of duty.

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

========= =  =  =  =  =  =  =  =  =  =  ==
   Day    0  1  2  3  4  5  6  7  8  9  10
========= =  =  =  =  =  =  =  =  =  =  ==
Nurse  0           X     X     X     X   
Nurse  1     X        X     X           X
Nurse  2  X     X                 X      
========= =  =  =  =  =  =  =  =  =  =  ==

The results show the following:

* One, and only one, nurse has been assigned to each day
* No nurse works two days in a row
* Two nurses work 4 days, and one works three days

Usage
-----

To run the demo, run the command

.. code-block:: bash

  python nurse_scheduling.py


Code Overview
-------------

Here is a general overview of the Nurse Scheduling code:

* Assign the size of the problem (Number of nurses and days) and parameters
* Compute the "penalty matrix" J
* Develop the QUBO matrix
* Run the problem
* Compute the hard shift constraint sum
* Compute the hard nurse constraint sum
* Compute the soft nurse constraint sum
* Print the nurse schedule

Note that the total of the three constraint sums should equal the energy.

Code Specifics
--------------

Some notes on the code:

* We use a vector to store the two-dimensional (nurse, day) matrix:

(0, 0) (0, 1) (0, 2)... (0, D) (1, 0) (1, 1)... (1, D)

in order to simplify the sums

* The three constraint sums are separated out in order to be able to 
confirm the individual effects

* We have not yet confirmed Ikeda's results with reverse annealing

References
----------

Ikeda, K., Nakamura, Y. & Humble, T.S. 
Application of Quantum Annealing to Nurse Scheduling Problem. 
Sci Rep 9, 12837 (2019). 
https://doi.org/10.1038/s41598-019-49172-3

License
-------

Released under the Apache License 2.0. See `LICENSE <LICENSE>`_ file.
