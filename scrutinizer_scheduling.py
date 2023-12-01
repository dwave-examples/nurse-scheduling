from dwave.system import LeapHybridSampler
from dimod import BinaryQuadraticModel
from collections import defaultdict
import matplotlib.pyplot as plt

# Define the number of scrutinizers and bills
n_scrutinizerJunior = 2
n_scrutinizerIntermediate = 3
n_scrutinizerSenior = 1
n_Scrutinizers = n_scrutinizerJunior + n_scrutinizerIntermediate + n_scrutinizerSenior

n_billEasy = 2
n_billMedium = 3
n_billHard = 2
nBills = n_billEasy + n_billMedium + n_billHard

# Define the time limit for bills to be reviewed
time_limit = 10

# Initialize QUBO matrix
Q = defaultdict(int)

# Define constants for rewards and penalties
reward = -1  # Reward for a valid assignment
penalty = 10  # Penalty for an invalid assignment
time_penalty = 1  # Penalty for exceeding the time limit

# Define assignment variables
variables = [(i, j) for i in range(n_Scrutinizers) for j in range(nBills)]

# Function to get index of the QUBO matrix for a given variable
def get_index(i, j):
    return i * nBills + j

# Populate the QUBO matrix with rewards, penalties, and time constraints
for i, j in variables:
    index = get_index(i, j)
    # Determine the scrutinizer's level and the bill's difficulty
    level = 'Senior' if i < n_scrutinizerSenior else ('Intermediate' if i < n_scrutinizerSenior + n_scrutinizerIntermediate else 'Junior')
    difficulty = 'Hard' if j < n_billHard else ('Medium' if j < n_billHard + n_billMedium else 'Easy')

    # Assign rewards and penalties based on the level and difficulty
    if (level == 'Senior') or (level == 'Intermediate' and difficulty != 'Hard') or (level == 'Junior' and difficulty == 'Easy'):
        Q[(index, index)] = reward
    else:
        Q[(index, index)] = penalty

    # Time penalties (simplified)
    # For simplicity, assume each scrutinizer works in sequential order and each bill takes a day
    if level == 'Junior':
        capacity = 1  # Junior can check only easy bills
    elif level == 'Intermediate':
        capacity = 2  # Intermediate can check easy and medium bills
    elif level == 'Senior':
        capacity = 3  # Senior can check all bills

    for k in range(capacity, nBills):
        # Only for bills that are beyond the scrutinizer's capacity
        Q[(index, get_index(i, k))] += time_penalty

# Ensure each bill is assigned to only one scrutinizer
for j in range(nBills):
    for i in range(n_Scrutinizers):
        for k in range(i+1, n_Scrutinizers):
            Q[(get_index(i, j), get_index(k, j))] += penalty

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
    assignments = {bill: None for bill in range(nBills)}  # Change to a dictionary mapping bills to a single scrutinizer
    for index, value in sample.items():
        if value and index < n_Scrutinizers * nBills:
            scrutinizer, bill = divmod(index, nBills)
            assignments[bill] = scrutinizer  # Assign the bill to one scrutinizer
    return assignments

# Convert sample to assignments including time
assignments_with_time = sample_to_assignments_with_time(sampleset, n_Scrutinizers, nBills, time_limit)

# Check the assignment validity to include skill level check
def check_assignments(assignments, n_Scrutinizers, nBills):
    # Check if every bill is assigned exactly once
    if len(assignments) != nBills:
        return False, "Not all bills are assigned."
    # Check if bills are assigned according to skill level
    for bill, scrutinizer in assignments.items():
        if scrutinizer is not None:
            level = 'Senior' if scrutinizer < n_scrutinizerSenior else ('Intermediate' if scrutinizer < n_scrutinizerSenior + n_scrutinizerIntermediate else 'Junior')
            difficulty = 'Hard' if bill < n_billHard else ('Medium' if bill < n_billHard + n_billMedium else 'Easy')
            if (level == 'Junior' and difficulty != 'Easy') or (level == 'Intermediate' and difficulty == 'Hard'):
                return False, f"Invalid assignment: {level} assigned to {difficulty} bill."
    return True, "All assignments are valid."

# Check assignments
is_valid, message = check_assignments(assignments_with_time, n_Scrutinizers, nBills)
print(message)

# Define scrutinizer_labels
scrutinizer_labels = [f"Scrutinizer {i+1}" for i in range(n_Scrutinizers)]



# Visualization for assignments
plt.figure(figsize=(12, 6))

# First subplot for Scrutinizer-Bill Assignments
plt.subplot(1, 2, 1)
for bill, scrutinizer in assignments_with_time.items():
    if scrutinizer is not None:  # Only plot if there is an assignment
        # Map the bill index to the correct x-position based on bill type
        bill_x_position = n_billEasy if bill < n_billEasy else (n_billEasy + n_billMedium if bill < n_billEasy + n_billMedium else nBills)
        plt.plot(bill_x_position, scrutinizer, 'bo')

# Generate bill labels dynamically based on the number of each type
bill_labels = ['Easy'] * n_billEasy + ['Medium'] * n_billMedium + ['Hard'] * n_billHard

# Set up the plot
plt.xlabel('Bills')
plt.ylabel('Scrutinizers')
plt.xticks(range(nBills), bill_labels)
plt.yticks(range(n_Scrutinizers), scrutinizer_labels)
plt.title('Scrutinizer-Bill Assignments')
plt.grid(True)

# Second subplot for Bills per Scrutinizer
plt.subplot(1, 2, 2)
bill_count = [0] * n_Scrutinizers
for bill, scrutinizer in assignments_with_time.items():
    if scrutinizer is not None:
        bill_count[scrutinizer] += 1

plt.bar(scrutinizer_labels, bill_count)
plt.xlabel('Scrutinizers')
plt.ylabel('Number of Bills Assigned')
plt.title('Bills per Scrutinizer')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
