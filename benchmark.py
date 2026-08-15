from backend.algorithms import (
    insertion_sort_count,
    binary_search_count,
    linear_search_count,
)


def create_records(size):
    records = []

    for i in range(size):
        records.append({
            "title": f"Task {size - i}",
            "priority": "medium",
            "due_date": "tomorrow"
        })

    return records


sizes = [10, 500, 3000]


print("TaskFlow Algorithm Benchmark")
print("=" * 50)

for size in sizes:
    print(f"\nData size: {size}")

    # ---------------------------------------------
    # Insertion sort
    # ---------------------------------------------

    records = create_records(size)

    insertion_comparisons = insertion_sort_count(
        records,
        "title"
    )

    print(
        f"Insertion sort comparisons: "
        f"{insertion_comparisons}"
    )

    # ---------------------------------------------
    # Binary search
    # ---------------------------------------------

    binary_result = binary_search_count(
        records,
        "Task 1",
        "title"
    )

    print(
        f"Binary search: "
        f"index={binary_result['index']}, "
        f"comparisons={binary_result['comparison_count']}"
    )

    # ---------------------------------------------
    # Linear search
    # ---------------------------------------------

    linear_records = create_records(size)

    linear_result = linear_search_count(
        linear_records,
        "Task 1",
        "title"
    )

    print(
        f"Linear search: "
        f"index={linear_result['index']}, "
        f"comparisons={linear_result['comparison_count']}"
    )