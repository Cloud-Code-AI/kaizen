import random
import time

# Global variable
GLOBAL_COUNTER = 0


def process_data(data):
    global GLOBAL_COUNTER
    result = []
    for i in range(len(data)):
        item = data[i]
        if item % 2 == 0:
            result.append(item * 2)
        else:
            result.append(item * 3)
        GLOBAL_COUNTER += 1
    return result


def fetch_user_data(user_id):
    # Simulating a database query
    time.sleep(2)
    return {"id": user_id, "name": f"User{user_id}", "score": random.randint(1, 100)}


def calculate_average(numbers):
    total = 0
    count = 0
    for num in numbers:
        total += num
        count += 1
    return total / count if count > 0 else 0


def write_to_file(filename, content):
    f = open(filename, "w")
    f.write(content)
    f.close()


def main():
    data = [1, 2, 3, 4, 5]
    processed_data = process_data(data)
    print("Processed data:", processed_data)

    user_data = fetch_user_data(123)
    print("User data:", user_data)

    numbers = [10, 20, 30, 40, 50]
    avg = calculate_average(numbers)
    print("Average:", avg)

    write_to_file("output.txt", "Hello, World!")

    unused_var = 42
    print("Unused variable:", unused_var)

    db_password = "password123"
    print("DB Password:", db_password)

    squared_numbers = [num * num for num in range(100)]
    print("Squared numbers:", squared_numbers)


if __name__ == "__main__":
    main()
