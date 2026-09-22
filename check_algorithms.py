from backend.algorithms import (
    insertion_sort,
    binary_search,
    insertion_sort_count,
    binary_search_count,
    linear_search_count,
)


def check(case_name, result, expected):
    if result == expected:
        print(f"PASS: {case_name}")
    else:
        print(f"FAIL: {case_name} — expected {expected}, got {result}")


# -------------------------------------------------
# 1. Empty insertion sort
# -------------------------------------------------

records = []

insertion_sort(records, "value")

check(
    "insertion_sort empty list",
    records,
    []
)


# -------------------------------------------------
# 2. Single-element insertion sort
# -------------------------------------------------

records = [
    {"value": 10}
]

insertion_sort(records, "value")

check(
    "insertion_sort single element",
    records,
    [{"value": 10}]
)


# -------------------------------------------------
# 3. Binary search first index
# -------------------------------------------------

records = [
    {"value": 1},
    {"value": 2},
    {"value": 3},
    {"value": 4},
    {"value": 5},
]

check(
    "binary_search first index",
    binary_search(records, 1, "value"),
    0
)


# -------------------------------------------------
# 4. Binary search last index
# -------------------------------------------------

check(
    "binary_search last index",
    binary_search(records, 5, "value"),
    4
)


# -------------------------------------------------
# 5. Binary search middle
# -------------------------------------------------

check(
    "binary_search middle",
    binary_search(records, 3, "value"),
    2
)


# -------------------------------------------------
# 6. Binary search not found
# -------------------------------------------------

check(
    "binary_search not found",
    binary_search(records, 99, "value"),
    -1
)


# -------------------------------------------------
# 7. insertion_sort_count
# -------------------------------------------------

records = [
    {"value": 3},
    {"value": 1},
    {"value": 2},
]

comparison_count = insertion_sort_count(
    records,
    "value"
)

if records == [
    {"value": 1},
    {"value": 2},
    {"value": 3},
] and type(comparison_count) == int and comparison_count > 0:
    print("PASS: insertion_sort_count sorting and count")
else:
    print(
        "FAIL: insertion_sort_count sorting and count "
        f"— got records={records}, count={comparison_count}"
    )


# -------------------------------------------------
# 8. binary_search_count
# -------------------------------------------------

records = [
    {"value": 1},
    {"value": 2},
    {"value": 3},
    {"value": 4},
    {"value": 5},
]

result = binary_search_count(
    records,
    3,
    "value"
)

if (
    result["index"] == 2
    and type(result["comparison_count"]) == int
    and result["comparison_count"] > 0
):
    print("PASS: binary_search_count")
else:
    print(
        "FAIL: binary_search_count "
        f"— got {result}"
    )


# -------------------------------------------------
# 9. linear_search_count absent value
# -------------------------------------------------

records = [
    {"value": 1},
    {"value": 2},
    {"value": 3},
    {"value": 4},
]

result = linear_search_count(
    records,
    99,
    "value"
)

if (
    result["index"] == -1
    and result["comparison_count"] == len(records)
):
    print("PASS: linear_search_count absent value")
else:
    print(
        "FAIL: linear_search_count absent value "
        f"— got {result}"
    )