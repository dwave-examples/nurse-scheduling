[![Linux/Mac/Windows build status](
  https://circleci.com/gh/dwave-examples/nurse-scheduling.svg?style=svg)](
  https://circleci.com/gh/dwave-examples/nurse-scheduling)

# Nurse Scheduling

This is a demo of a nurse scheduling model developed by Ikeda, Nakamura
and Humble (INH).

The nurse scheduling problem seeks to find an optimal assignment for a group of
nurses, under constraints of scheduling and personnel. INH developed a model
which is a simplified representation of a real-world nursing facility.

In the general nurse scheduling problem, there are three types of constraints,
which are mentioned here to provide background for INH's constraints.
These types of constraints, in the general problem, are:

1) Both upper and lower limits on the number of breaks.
2) The number of nurses on duty for each shift slot.
3) For each individual nurse, upper and lower limits on the time interval
   between days of duty.

These three types of constraints combine to ensure sufficient nurses
on duty at all times, without overworking any particular nurse.

INH formulated a QUBO from a simplification of these constraints, discussed
below, that tries to achieve reasonable results for nurse scheduling.

INH's three types of constraints are:

1) "hard shift" constraint: requires that at least one nurse is assigned for
   each working day.

2) "hard nurse" constraint: requires that no nurse works two or more consecutive
   days.

3) "soft nurse" constraint: promotes that all nurses should have roughly
   even work schedules.

This demo seeks to obtain reasonable results for a nurse schedule, based on
INH's model. Our implementation attempts to find a schedule for a number
`n_nurses` of nurses and a number `n_days` of days that satisfies the following
conditions:

* One, and only one, nurse has been assigned to each day (hard shift constraint)
* No nurse works two days in a row (hard nurse constraint)
* The nurses should work the same number of days

Running the demo results in the following output, at the command-line:

```bash
Size  33

Energy  0.5999999999999694

Checking Hard nurse constraint  0.0

Checking Hard shift constraint  0.0

Checking Soft nurse constraint  0.6
```

| Day     | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Nurse 0 |   |   |   | X |   | X |   | X |   | X |   |
| Nurse 1 |   | X |   |   | X |   | X |   |   |   | X |
| Nurse 2 | X |   | X |   |   |   |   |   | X |   |   |

The results show the following:

* One, and only one, nurse has been assigned to each day
* No nurse works two days in a row
* Two nurses work 4 days, and one works three days. Because two nurses work one
  extra day each, the soft nurse constraint energy is nonzero. Each nurse
  working one extra day contributes a total of gamma to the energy. Since gamma
  is 0.3, the total energy is expected to be 0.6.

## Usage

To run the demo, run the command

```bash
python nurse_scheduling.py
```

## Code Overview

Here is a general overview of the Nurse Scheduling code:

* Assign the size of the problem (number of nurses and days) and parameters
* Compute the "penalty matrix" J
* Develop the QUBO matrix
* Run the problem (solve the QUBO)
* Calculate the hard nurse constraint sum, to check if the hard nurse
  constraints are satisfied
* Calculate the hard shift constraint sum, to check if the hard shift
  constraints are satisfied
* Calculate the soft nurse constraint sum, to check if the soft nurse
  constraints are satisfied
* Print the nurse schedule

Note that the total of the three constraint sums should equal the energy.

## Code Specifics

Some notes on the code:

* We use a two-dimensional QUBO matrix, Q[`i`, `j`], in which both indices `i`
  and `j` are composite indices. Each composite index is used to represent the
  combinations of the variables `nurse` and `day`. The (`nurse`, `day`) tuples
  are placed into the one-dimensional index in the following order, where
  `nurse` is first index, and `day` is second index, in the tuples:

  (0, 0) (0, 1) (0, 2)... (0, D) (1, 0) (1, 1)... (1, D)

* The methods `get_index` and `get_nurse_and_day` are used to convert back and
  forth between (`nurse`, `day`) tuples and the composite indices.

* The three constraint sums are separated out in order to be able to confirm the
  individual effects manually. For example, if a nurse was assigned to two
  successive days, the hard nurse constraint sum would be nonzero.

* We have not yet confirmed Ikeda's results with reverse annealing

## References

Ikeda, K., Nakamura, Y. & Humble, T.S. Application of Quantum Annealing to Nurse
Scheduling Problem. Sci Rep 9, 12837 (2019).
https://doi.org/10.1038/s41598-019-49172-3

## License

Released under the Apache License 2.0. See [LICENSE](LICENSE) file.
