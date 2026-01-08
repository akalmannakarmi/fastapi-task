import csv
import random
import argparse

def create_csv(filename, count, prefix):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        
        # Header
        writer.writerow(["name", "email", "amount"])
        
        # Rows
        for i in range(1, count + 1):
            name = f"{prefix}{i}"
            email = f"{name}@example.com"
            amount = random.choice([500, 1000, 3000, 5000])
            writer.writerow([name, email, amount])

    print(f"CSV file '{filename}' created with {count} records.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a CSV file with users")
    parser.add_argument("--count", type=int, required=True, help="Number of users")
    parser.add_argument("--prefix", type=str, required=True, help="User name prefix")
    parser.add_argument("--output", type=str, default="users.csv", help="Output CSV file name")

    args = parser.parse_args()

    create_csv(args.output, args.count, args.prefix)
