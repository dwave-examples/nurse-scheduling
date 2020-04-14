================
Nurse Scheduling
================

This is a demo of a nurse scheduling model developed by Ikeda, Nakamura
and Humble (INH). 

The nurse scheduling problem seeks to find an optimal assignment
for a group of nurses, under constraints of scheduling and personnel.
INH developed a model which is a simplified representation of a real-world 
nursing facility.

In the general nurse scheduling problem, there are three types of constraints,
which are mentioned here to provide background for INH's constraints.
These types of constraints, in the general problem, are:

1) Both upper and lower limits on the number of breaks.
2) The number of nurses on duty for each shift slot.
3) For each individual nurse, upper and lower limits on the time interval 
   between days of duty.

These three types of constraints combine to ensure sufficient nurses
on duty at all times, without overworking any particular nurse.

INH took these general constraints and formulated them as a QUBO.
Their form of the constraints, discussed below, tries to achieve reasonable
results for nurse scheduling, without implementing all the detail required 
in the three general constraints.

INH's three types of constraints are:

The "hard shift" constraint requires that at least one nurse is assigned for
each working day.

The "hard nurse" constraint ensures that no nurse works two or more 
consecutive days.

The "soft nurse" constraint requires that all nurses should have roughly
even work schedules.

This demo seeks to obtain reasonable results for a nurse schedule, based on
INH's model. In our implementation, the number of days is D, and the number 
of nurses is N. We wish to find a schedule for the N nurses, on the D days, 
which satisfies the following conditions:

* One, and only one, nurse has been assigned to each day (hard shift 
  constraint)
* No nurse works two days in a row (hard nurse constraint)
* The nurses should work the same number of days

Running the demo results in the following output, at the command-line:

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

* Assign the size of the problem (number of nurses and days) and parameters
* Compute the "penalty matrix" J
* Develop the QUBO matrix
* Run the problem (solve the QUBO)
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

* The three constraint sums are separated out in order to be able to 
confirm the individual effects manually. For example, if a nurse was
assigned to two successive days, the hard nurse constraint sum would be
nonzero.

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
