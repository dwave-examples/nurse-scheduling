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
# K., # Nakamura, Y. & Humble, T.S. Application of Quantum Annealing to Nurse 
# Scheduling Problem. Sci Rep 9, 12837 (2019). 
# https://doi.org/10.1038/s41598-019-49172-3, © The Author(s) 2019, use of 
# which is licensed under a Creative Commons Attribution 4.0 International 
# License (To view a copy of this license, visit 
# http://creativecommons.org/licenses/by/4.0/).

from dwave.system import LeapHybridSampler
from dimod import BinaryQuadraticModel

# count nurses n = 1 ... N_NURSES
# count scheduling days as d = 1 ... N_DAYS
# binary variable q_nd is the assignment of nurse n to day d
a = 3.5
N_NURSES = 3
N_DAYS = 11
SIZE = N_DAYS * N_NURSES

# Hard shift constraint: at least one nurse is working each day
# implemented by penalizing any nurses scheduled on two successive
# days

# Hard nurse constraint: no nurse works two or more consecutive days
# Lagrange parameter, for hard nurse constraint, on workforce and effort
# Workforce function W(d) - set to a constant for now
# Effort function E(n) - set to a constant for now
lamda = 1.3
W = 1
E = 1

# Soft nurse constraint: all nurses should have approximately even work
#                        schedules
# Lagrange parameter, for shift constraints, on work days
# preference function G - set to a constant for now
# Minimum duty days F - the number of work days that each nurse wants
# to be scheduled. At present, each will do the minimum on average.
gamma = 0.3
G = 1
F = int(N_DAYS/N_NURSES)


def indx(n, d):
    return n * N_DAYS + d


def get_nurse_and_day(indx):
    return (int(indx / N_DAYS), indx % N_DAYS)


# Hard shift constraint - does not have Lagrange parameter - J matrix
# symmetric, real-valued interaction matrix J, whereas all terms are
# a or zero.
# composite indices i(n, d) and j(n, d) as functions of n and d
# In other words, the indices are not n and d. They are kind of
# (n+d)**2, and we need to take that into account. This seems to be
# a clean way to do it.
# J_i(n,d)j(n,d+1) = a and 0 otherwise.
J = {}
for nurse_day_1 in range(SIZE):
    for nurse_day_2 in range(SIZE):
        J[nurse_day_1, nurse_day_2] = 0
        if int(nurse_day_1 / N_DAYS) == int(nurse_day_2 / N_DAYS) and nurse_day_2 == nurse_day_1 + 1:
            J[nurse_day_1, nurse_day_2] = a

# Q matrix assign the cost term, the J matrix
Q = {}
for nurse_day_1 in range(SIZE):
    for nurse_day_2 in range(SIZE):
        Q[nurse_day_1, nurse_day_2] = J[nurse_day_1, nurse_day_2]

# Hard nurse constraint. The sum is over each day.
# lamda * ((sum(E * q) - W) ** 2)
for nurse_day_1 in range(SIZE):
    _, date_index = get_nurse_and_day(nurse_day_1)
    # Diagonal term, without the W * W
    Q[nurse_day_1, nurse_day_1] += lamda * (1 - (2 * W))
    for nurse_day_2 in range(SIZE):
        _, day_index_2 = get_nurse_and_day(nurse_day_2)
        # Include only the same day, across nurses
        if (date_index == day_index_2 and nurse_day_2 != nurse_day_1):
            Q[nurse_day_1, nurse_day_2] += lamda * 2

# Soft nurse constraint
# gamma * ((sum(h * q) - F) ** 2)
for nurse_day_1 in range(SIZE):
    nurse_index_1, _ = get_nurse_and_day(nurse_day_1)
    # Diagonal term, without the F * F
    Q[nurse_day_1, nurse_day_1] += gamma * (1 - (2 * F))
    for nurse_day_2 in range(nurse_day_1 + 1, SIZE):
        nurse_index_2, _ = get_nurse_and_day(nurse_day_2)
        if (nurse_index_1 == nurse_index_2 and nurse_day_2 != nurse_day_1):
            Q[nurse_day_1, nurse_day_2] += gamma * 2

# Solve the problem, and use the offset to scale the energy
e_offset = (lamda * N_DAYS * W * W) + (gamma * N_NURSES * F * F)
bqm = BinaryQuadraticModel.from_qubo(Q, offset=e_offset)
sampler = LeapHybridSampler()
results = sampler.sample(bqm)

# Get the results
smpl, energy = next(iter(results.data(['sample', 'energy'])))
print("Size ", SIZE)
print("Energy ", energy)


# Check the results by doing the sums directly
# J sum
sum_j = 0
for i in range(SIZE):
    for j in range(SIZE):
        sum_j += J[i, j] * smpl[i] * smpl[j]
print("Checking Hard shift constraint ", sum_j)

sum_w = 0
# W sum
for d in range(N_DAYS):
    sum_n = 0
    for n in range(N_NURSES):
        sum_n += E * smpl[indx(n, d)]
    sum_w += lamda * (sum_n - W) * (sum_n - W)
print("Checking Hard nurse constraint ", sum_w)

sum_f = 0
# F sum
for n in range(N_NURSES):
    sum_d = 0
    for d in range(N_DAYS):
        sum_d += G * smpl[indx(n, d)]
    sum_f += gamma * (sum_d - F) * (sum_d - F)
print("Checking Soft nurse constraint ", sum_f)

# Graphics
sched = [get_nurse_and_day(j) for j in range(SIZE) if smpl[j] == 1]
str_hdr = ""
for d in range(N_DAYS):
    str_hdr += "  " + str(d)
print("     ", "  ", str_hdr)
for n in range(N_NURSES):
        str_row = ""
        for d in range(N_DAYS):
            str_row += "  " + ("X" if (n, d) in sched else " ")
        print("Nurse ",n, str_row)
