import random
import csv

# Configuration
NUM_TESTS = 50
NUM_USERS = 10
MODULES = ['M1', 'M2', 'M3', 'M4', 'M5']

# Heavily biased module failure weights
MODULE_FAILURE_WEIGHTS = {
    'M1': 1,
    'M2': 1,
    'M3': 5,  # extremely failure-prone
    'M4': 1,
    'M5': 4   # very failure-prone
}

# High-failure users
USER_FAILURE_BIAS = {
    'user_4': 0.2,  # 20% chance to pass
    'user_7': 0.3   # 30% chance to pass
}

# Function to simulate pass/fail based on duration
def get_pass_probability(user, duration):
    base = USER_FAILURE_BIAS.get(user, 0.35)  # default 35% pass rate
    if duration > 180:
        base -= 0.1  # less likely to pass if test is long
    elif duration < 30:
        base += 0.1  # more likely to pass if quick
    return max(min(base, 0.95), 0.05)

def generate_test_data(num_tests):
    data = []

    for i in range(1, num_tests + 1):
        test_id = f'TEST-{i:04d}'
        user = f'user_{random.randint(1, NUM_USERS)}'
        duration = round(random.uniform(10.0, 300.0), 2)

        # Adjust pass probability
        pass_chance = get_pass_probability(user, duration)
        status = random.choices(['Passed', 'Failed'], weights=[pass_chance, 1 - pass_chance])[0]

        failed = []
        if status == 'Failed':
            # Choose 1–3 failed modules, weighted
            num_failed = random.randint(1, 3)
            failed = random.choices(
                MODULES,
                weights=[MODULE_FAILURE_WEIGHTS[m] for m in MODULES],
                k=num_failed
            )

        data.append({
            'test_id': test_id,
            'run_by': user,
            'duration_seconds': duration,
            'status': status,
            'failed_modules': ', '.join(sorted(set(failed))) if failed else None
        })

    return data

def save_to_csv(data, filename='biased_test_results.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

# Run script
test_data = generate_test_data(NUM_TESTS)
save_to_csv(test_data)

# Preview
for row in test_data[:5]:
    print(row)
