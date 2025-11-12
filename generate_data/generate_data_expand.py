import random
import csv

# Configuration
NUM_ENTRIES = 50

failure_types = [
    "NullPointerException",
    "TimeoutError",
    "AssertionError",
    "ConnectionRefused",
    "FileNotFoundError"
]

# Related error messages (but not identical to failure_type)
error_message_map = {
    "NullPointerException": "Variable 'userToken' was null",
    "TimeoutError": "API request exceeded 30s limit",
    "AssertionError": "Expected status 'active' but got null",
    "ConnectionRefused": "Database connection to localhost:5432 refused",
    "FileNotFoundError": "Required file 'config.yaml' not found"
}

# Correlated last code changes
last_code_change_map = {
    "NullPointerException": "Refactored variable initialization",
    "TimeoutError": "Increased external API call frequency",
    "AssertionError": "Modified test assertions for new feature",
    "ConnectionRefused": "Changed database connection settings",
    "FileNotFoundError": "Updated file paths in configuration"
}

# Possible environments
environments = ["staging", "production", "unit_test"]

# Generate and save CSV
output_path = "correlated_test_failures.csv"
with open(output_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    # Header
    writer.writerow(["test_id", "failure_type", "error_message", "last_code_change", "environment"])
    
    # Rows
    for i in range(1, NUM_ENTRIES + 1):
        failure_type = random.choice(failure_types)
        writer.writerow([
            f"TEST-{i:04d}",
            failure_type,
            error_message_map[failure_type],
            last_code_change_map[failure_type],
            random.choice(environments)
        ])

print(f"CSV dataset generated and saved to {output_path}")
