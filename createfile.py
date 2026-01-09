import csv
import random
import argparse


def create_csv(filename, count, prefix, randomize, dup_percent):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)

        # Header
        writer.writerow(["name", "email", "amount"])

        # Calculate max number range for duplicates
        if randomize:
            max_number = max(1, int(count * (dup_percent / 100)))
        else:
            max_number = count

        for i in range(1, count + 1):
            if randomize:
                number = random.randint(1, max_number)
            else:
                number = i

            name = f"{prefix}{number}"
            email = f"{name}@example.com"
            amount = random.choice([500, 1000, 3000, 5000])

            writer.writerow([name, email, amount])

    print(f"CSV file '{filename}' created with {count} records.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a CSV file with users")

    parser.add_argument("--count", type=int, required=True, help="Number of users")
    parser.add_argument("--prefix", type=str, required=True, help="User name prefix")
    parser.add_argument(
        "--output", type=str, default="users.csv", help="Output CSV file name"
    )

    parser.add_argument(
        "--randomize",
        action="store_true",
        help="Randomize number after prefix (creates duplicates)",
    )
    parser.add_argument(
        "--dup-percent",
        type=float,
        default=80,
        help="Percentage of unique range (lower = more duplicates)",
    )

    args = parser.parse_args()

    create_csv(
        args.output,
        args.count,
        args.prefix,
        args.randomize,
        args.dup_percent,
    )
