# Copyright 2020 D-Wave Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This code includes an implementation of the algorithm described in Ikeda,
# K., Nakamura, Y. & Humble, T.S. Application of Quantum Annealing to Nurse
# Scheduling Problem. Sci Rep 9, 12837 (2019).
# https://doi.org/10.1038/s41598-019-49172-3, © The Author(s) 2019, use of
# which is licensed under a Creative Commons Attribution 4.0 International
# License (To view a copy of this license, visit
# http://creativecommons.org/licenses/by/4.0/).

from dwave.system import LeapHybridSampler
from dimod import BinaryQuadraticModel
from collections import defaultdict
from copy import deepcopy

# count nurses n = 1 ... n_nurses
# count scheduling days as d = 1 ... n_days
# binary variable q_nd is the assignment of nurse n to day d
# a is a positive correlation coefficient for implementing the hard nurse
# constraint - value provided by Ikeda, Nakamura, Humble
a = 3.5
n_nurses = 3
n_days = 11
size = n_days * n_nurses

# Hard shift constraint: at least one nurse working every day
# Lagrange parameter, for hard nurse constraint, on workforce and effort
# Workforce function W(d) - set to a constant 'workforce' for now
# Effort function E(n) - set to a constant 'effort' for now
lagrange_parameter = 1.3
workforce = 1
effort = 1

# Soft nurse constraint: all nurses should have approximately even work
#                        schedules
# Lagrange parameter, for shift constraints, on work days
# preference function 'preference' - set to a constant for now
# Minimum duty days 'min_duty_days' - the number of work days that each
# nurse wants
# to be scheduled. At present, each will do the minimum on average.
# The parameter gamma's value suggested by Ikeda, Nakamura, Humble
gamma = 0.3
preference = 1
min_duty_days = int(n_days/n_nurses)


# Find index into 1D list for (nurse_index, day_index)
def get_index(nurse_index, day_index):
    return nurse_index * n_days + day_index


# Inverse of get_index - given an index in a 1D list, return the nurse_index
# and day_index
def get_nurse_and_day(index):
    nurse_index, day_index = divmod(index, n_days)
    return nurse_index, day_index


# Hard nurse constraint: no nurse works two consecutive days
# It does not have Lagrange parameter - instead, J matrix
# symmetric, real-valued interaction matrix J, whereas all terms are
# a or zero.
# composite indices i(n, d) and j(n, d) as functions of n and d
# In other words, the indices are not n and d. They are kind of
# (n+d)**2, and we need to take that into account. This seems to be
# a clean way to do it.
# J_i(n,d)j(n,d+1) = a and 0 otherwise.
J = defaultdict(int)
for nurse in range(n_nurses):
    for day in range(n_days - 1):
        nurse_day_1 = get_index(nurse, day)
        nurse_day_2 = get_index(nurse, day+1)
        J[nurse_day_1, nurse_day_2] = a

# Q matrix assign the cost term, the J matrix
Q = deepcopy(J)

# Hard shift constraint. The sum is over each day.
# lagrange_parameter * ((sum(effort * q) - workforce) ** 2)
for nurse_day_1 in range(size):
    _, date_index = get_nurse_and_day(nurse_day_1)
    # Diagonal term, without the workforce * workforce
    Q[nurse_day_1, nurse_day_1] += lagrange_parameter * (1 - (2 * workforce))
    for nurse_day_2 in range(size):
        _, day_index_2 = get_nurse_and_day(nurse_day_2)
        # Include only the same day, across nurses
        if (date_index == day_index_2 and nurse_day_2 != nurse_day_1):
            Q[nurse_day_1, nurse_day_2] += lagrange_parameter * 2

# Soft nurse constraint
# gamma * ((sum(h * q) - min_duty_days) ** 2)
for nurse_day_1 in range(size):
    nurse_index_1, _ = get_nurse_and_day(nurse_day_1)
    # Diagonal term, without the min_duty_days * min_duty_days
    Q[nurse_day_1, nurse_day_1] += gamma * (1 - (2 * min_duty_days))
    for nurse_day_2 in range(nurse_day_1 + 1, size):
        nurse_index_2, _ = get_nurse_and_day(nurse_day_2)
        if (nurse_index_1 == nurse_index_2 and nurse_day_2 != nurse_day_1):
            Q[nurse_day_1, nurse_day_2] += gamma * 2

# Solve the problem, and use the offset to scale the energy
e_offset = (lagrange_parameter * n_days * workforce * workforce) + (gamma * n_nurses * min_duty_days * min_duty_days)
bqm = BinaryQuadraticModel.from_qubo(Q, offset=e_offset)
sampler = LeapHybridSampler()
results = sampler.sample(bqm)

# Get the results
smpl = results.first.sample
energy = results.first.energy
print("Size ", size)
print("Energy ", energy)


# Check the results by doing the sums directly
# J sum
sum_j = 0
for i in range(size):
    for j in range(size):
        sum_j += J[i, j] * smpl[i] * smpl[j]
print("Checking Hard nurse constraint ", sum_j)

sum_w = 0
# workforce sum
for d in range(n_days):
    sum_n = 0
    for n in range(n_nurses):
        sum_n += effort * smpl[get_index(n, d)]
    sum_w += lagrange_parameter * (sum_n - workforce) * (sum_n - workforce)
print("Checking Hard shift constraint ", sum_w)

sum_f = 0
# min_duty_days sum
for n in range(n_nurses):
    sum_d = 0
    for d in range(n_days):
        sum_d += preference * smpl[get_index(n, d)]
    sum_f += gamma * (sum_d - min_duty_days) * (sum_d - min_duty_days)
print("Checking Soft nurse constraint ", sum_f)

# Graphics
sched = [get_nurse_and_day(j) for j in range(size) if smpl[j] == 1]
str_hdr = ""
for d in range(n_days):
    str_hdr += "  " + str(d)
print("     ", "  ", str_hdr)
for n in range(n_nurses):
    str_row = ""
    for d in range(n_days):
        str_row += "  " + ("X" if (n, d) in sched else " ")
    print("Nurse ", n, str_row)
