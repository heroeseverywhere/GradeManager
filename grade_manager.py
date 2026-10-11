"""
Student Grade Manager
Week 1, Day 2 - Social Eagle

Stores student marks, works out each student's grade, and prints the
results as an aligned table with the class average, highest and lowest mark.

Storage choice:
    A dictionary keyed by the student's name in lowercase.
    - Lookups for duplicates are instant (no scanning a list).
    - Lowercase keys mean "Priya", "priya" and "PRIYA" are treated as the
      same student, so a typo in capitals can't create a second record.
    - Each value keeps the name as the user typed it (for display) and the mark.
    - Dictionaries keep insertion order, so the table prints in the order
      students were added.

Duplicate names (two students called Priya):
    The program does not silently overwrite. It asks whether to update the
    existing mark. If the user says no, they are asked to enter a name that
    tells the two apart, e.g. "Priya S" or "Priya R".

Invalid input:
    - Marks must be numbers between 0 and 100 (105, -5, "abc" are rejected
      with a message and the user is asked again).
    - Blank input when asked for a name or mark cancels back to the menu.
    - Names must contain at least one letter.
    - Showing results with no students prints a friendly message.
    - Ctrl+C / Ctrl+D exits cleanly instead of showing a traceback.
"""

# name in lowercase -> {"name": name as typed, "mark": number}
students = {}


def get_grade(mark):
    """Return the letter grade for a mark from 0 to 100 (boundaries inclusive)."""
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "E"


def format_mark(mark):
    """Show whole numbers without a decimal point (92, not 92.0)."""
    return str(int(mark)) if mark == int(mark) else f"{mark:.1f}"


def ask_name():
    """Ask for a student name. Returns the cleaned name, or None to cancel."""
    while True:
        name = input("Student name (press Enter to cancel): ").strip()
        if name == "":
            return None
        # Collapse extra spaces, e.g. "  priya    s " -> "priya s"
        name = " ".join(name.split())
        if not any(ch.isalpha() for ch in name):
            print("  A name needs at least one letter. Try again.")
            continue
        if len(name) > 30:
            print("  Please keep the name to 30 characters or fewer.")
            continue
        return name


def ask_mark(name):
    """Ask for a mark between 0 and 100. Returns the number, or None to cancel."""
    while True:
        text = input(f"Mark for {name} (0-100, press Enter to cancel): ").strip()
        if text == "":
            return None
        try:
            mark = float(text)
        except ValueError:
            print(f"  '{text}' is not a number. Please enter a mark like 78.")
            continue
        if mark != mark or mark in (float("inf"), float("-inf")):  # nan / inf
            print("  Please enter a real number between 0 and 100.")
            continue
        if mark < 0 or mark > 100:
            print(f"  {format_mark(mark)} is out of range. Marks must be between 0 and 100.")
            continue
        return mark


def add_student():
    """Ask for a name and mark, validate both, and store the student."""
    while True:
        name = ask_name()
        if name is None:
            print("  Cancelled. Back to the menu.")
            return

        key = name.lower()
        if key in students:
            existing = students[key]
            print(f"  A student called {existing['name']} already exists "
                  f"(mark {format_mark(existing['mark'])}).")
            choice = input("  Update their mark? (y/n): ").strip().lower()
            if choice in ("y", "yes"):
                mark = ask_mark(existing["name"])
                if mark is None:
                    print("  Cancelled. Mark unchanged.")
                    return
                existing["mark"] = mark
                print(f"  Updated {existing['name']}: {format_mark(mark)} "
                      f"({get_grade(mark)})")
                return
            # Different person with the same name: ask for a name that tells them apart.
            print("  Please enter a name that tells them apart, e.g. "
                  f"'{existing['name']} S'.")
            continue

        mark = ask_mark(name)
        if mark is None:
            print("  Cancelled. Back to the menu.")
            return
        students[key] = {"name": name, "mark": mark}
        print(f"  Added {name}: {format_mark(mark)} ({get_grade(mark)})")
        return


def show_results():
    """Print an aligned table of name, mark and grade, plus average, highest and lowest."""
    if not students:
        print("\nNo students yet. Choose 1 to add one first.")
        return

    records = list(students.values())
    name_width = max(len("Name"), max(len(s["name"]) for s in records)) + 4

    print()
    print(f"{'Name':<{name_width}}{'Mark':>5}{'Grade':>8}")
    print("-" * (name_width + 13))
    for s in records:
        print(f"{s['name']:<{name_width}}{format_mark(s['mark']):>5}"
              f"{get_grade(s['mark']):>7}")
    print("-" * (name_width + 13))

    marks = [s["mark"] for s in records]
    average = sum(marks) / len(marks)
    print(f"Average: {average:.1f}    Highest: {format_mark(max(marks))}    "
          f"Lowest: {format_mark(min(marks))}")


def main():
    print("=== Student Grade Manager ===")
    while True:
        print("\n1. Add student")
        print("2. Show results")
        print("3. Quit")
        choice = input("Choose 1, 2 or 3: ").strip().lower()

        if choice in ("1", "add", "a"):
            add_student()
        elif choice in ("2", "show", "s"):
            show_results()
        elif choice in ("3", "quit", "q", "exit"):
            print("Goodbye!")
            break
        elif choice == "":
            print("Please type 1, 2 or 3.")
        else:
            print(f"'{choice}' is not an option. Please type 1, 2 or 3.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C or Ctrl+D: exit cleanly instead of showing an error.
        print("\nGoodbye!")
