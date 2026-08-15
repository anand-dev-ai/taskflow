from backend.ai_parser import parse_task_description


examples = [
    "This is urgent, mark it ASAP please",
    " ",
    "Finish the report next Friday, it's urgent",
    "tomorrow review tomorrow",
    "Fix the scanner ASAP next Monday",
]


for description in examples:
    print("\nInput:")
    print(description)

    print("Output:")
    print(parse_task_description(description))