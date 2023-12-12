# Import necessary libraries
from dwave.system import LeapHybridSampler
from dimod import BinaryQuadraticModel
from collections import defaultdict
import matplotlib.pyplot as plt

# Define the number of scrutinizers and bills
n_scrutinizerJunior = 2
n_scrutinizerIntermediate = 3
n_scrutinizerSenior = 1
n_Scrutinizers = n_scrutinizerJunior + n_scrutinizerIntermediate + n_scrutinizerSenior

n_billEasy = 3
n_billMedium = 4
n_billHard = 3
nBills = n_billEasy + n_billMedium + n_billHard

# Constants for rewards and penalties
reward = -100  # Reward for a valid assignment
junior_wrong_assignment_penalty = 10000  # Penalty for junior assigned non-easy bills
intermediate_wrong_assignment_penalty = 5000  # Penalty for intermediate assigned hard bills
senior_wrong_assignment_penalty = 100000  # Lesser penalty for senior assigned wrong bills (as they can handle all)
unique_assignment_penalty = 20000  # Penalty for assigning a bill to more than one scrutinizer
time_limit = 10 # Penalty for simple time constraint

# Initialize QUBO matrix
Q = defaultdict(int)

# Define assignment variables
variables = [(i, j) for i in range(n_Scrutinizers) for j in range(nBills)]

# Function to get index of the QUBO matrix for a given variable
def get_index(i, j):
    return i * nBills + j

# Populate the QUBO matrix with rewards and penalties based on the assignment constraints
for i, j in variables:
    index = get_index(i, j)
    level = 'Senior' if i < n_scrutinizerSenior else ('Intermediate' if i < n_scrutinizerSenior + n_scrutinizerIntermediate else 'Junior')
    difficulty = 'Hard' if j < n_billHard else ('Medium' if j < n_billHard + n_billMedium else 'Easy')

    # Apply penalties and rewards based on the level of the scrutinizer and the difficulty of the bill
    if level == 'Junior' and difficulty != 'Easy':
        Q[(index, index)] = junior_wrong_assignment_penalty
    elif level == 'Intermediate' and difficulty == 'Hard':
        Q[(index, index)] = intermediate_wrong_assignment_penalty
    elif level == 'Senior':
        if difficulty == 'Easy':
            Q[(index, index)] = senior_wrong_assignment_penalty
        elif difficulty == 'Medium':
            Q[(index, index)] = senior_wrong_assignment_penalty
        else:
            Q[(index, index)] = reward
    else:
        Q[(index, index)] = reward

    # Ensure each bill is assigned to only one scrutinizer
    for j in range(nBills):
        for i in range(n_Scrutinizers):
            for k in range(i+1, n_Scrutinizers):
                Q[(get_index(i, j), get_index(k, j))] += unique_assignment_penalty

print(Q)

# Create the QUBO model
bqm = BinaryQuadraticModel.from_qubo(Q)

# Solve the problem using a hybrid sampler
sampler = LeapHybridSampler()
results = sampler.sample(bqm, label='Example - Scrutinizer Assignment')

# Process the results
sampleset = results.first.sample
energy = results.first.energy

print("Sample:", sampleset)
print("Energy:", energy)

# Function to convert sample to scrutinizer-bill assignments including time
def sample_to_assignments_with_time(sample, n_Scrutinizers, nBills, time_limit):
    assignments = defaultdict(list)
    for index, value in sample.items():
        if value and index < n_Scrutinizers * nBills:
            scrutinizer, bill = divmod(index, nBills)
            assignments[scrutinizer].append(bill)
    return assignments

# Convert sample to assignments including time
assignments_with_time = sample_to_assignments_with_time(sampleset, n_Scrutinizers, nBills, time_limit)

# Define scrutinizer labels with levels for visualization
scrutinizer_labels_with_levels = ['Senior' if i < n_scrutinizerSenior else 'Intermediate' if i < n_scrutinizerSenior + n_scrutinizerIntermediate else 'Junior' for i in range(n_Scrutinizers)]
scrutinizer_labels_with_levels = [f"Scrutinizer {i+1} ({level})" for i, level in enumerate(scrutinizer_labels_with_levels)]

# Initialize bill count with zeros for each scrutinizer
bill_count = [0] * n_Scrutinizers

# Update bill count based on assignments
for scrutinizer, bills in assignments_with_time.items():
    bill_count[scrutinizer] = len(bills)



# Visualization for assignments
plt.figure(figsize=(12, 6))

# First subplot for Scrutinizer-Bill Assignments
plt.subplot(1, 2, 1)
for scrutinizer, bills in assignments_with_time.items():
    for bill in bills:
        bill_type = 'Hard' if bill < n_billHard else ('Medium' if bill < n_billHard + n_billMedium else 'Easy')
        plt.plot(bill, scrutinizer, 'o', label=f"{bill_type} (Bill {bill})")

# Set up the plot
plt.xlabel('Bills')
plt.ylabel('Scrutinizers')
plt.xticks(range(nBills), ['Easy'] * n_billEasy + ['Medium'] * n_billMedium + ['Hard'] * n_billHard, rotation=45)
plt.yticks(range(n_Scrutinizers), scrutinizer_labels_with_levels)
plt.title('Scrutinizer-Bill Assignments')
plt.legend(loc='upper right')
plt.grid(True)

# Second subplot for Bills per Scrutinizer
plt.subplot(1, 2, 2)
plt.bar(scrutinizer_labels_with_levels, bill_count)
plt.xlabel('Scrutinizers')
plt.ylabel('Number of Bills Assigned')
plt.title('Bills per Scrutinizer')
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig("scrutinizer_bill_assignments.png", format='png')
plt.show()
