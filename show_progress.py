import sys
import time


def progress_bar(
    iterable, total, prefix="", suffix="", length=50, fill="█", print_end=""
):
    """
    A single-line progress bar for terminal applications.

    Args:
        iterable: The data to iterate over.
        total: Total iterations for calculating the progress.
        prefix (str): Text before the progress bar.
        suffix (str): Text after the progress bar.
        length (int): The length of the progress bar.
        fill (str): The character to fill the progress bar.
        print_end (str): The character to end the print with.
    """

    def print_progress(iteration):
        percent = f"{100 * (iteration / float(total)):.1f}"
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + "-" * (length - filled_length)
        # Clear the line and print progress on the same line
        sys.stdout.write(f"\r{prefix} |{bar}| {percent}% {suffix}")
        sys.stdout.flush()
        if iteration == total:  # Print new line on completion
            print(print_end)

    for i, item in enumerate(iterable, 1):
        yield item
        print_progress(i)


# Example usage
if __name__ == "__main__":
    items = range(100)
    sum = 0
    for _ in progress_bar(
        items, total=len(items), prefix="Progress", suffix="Complete", length=40
    ):
        time.sleep(0.05)  # Simulate some work
        sum += 1
    print(f"Sum of items: {sum}")
