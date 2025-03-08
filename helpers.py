def is_valid_url(url):
    """Check if a URL starts with 'http://' or 'https://'."""
    return url.startswith("http://") or url.startswith("https://")


def collect_globs(label):
    """Collect a list of glob patterns for the given label until the user types 'done'."""
    glob_list = []
    print(f"Enter glob {label} one by one. Type 'done' when finished:")
    while True:
        user_input = input(f"Glob {label}: ")
        if user_input.lower() == 'done':
            break
        if not is_valid_url(user_input):
            print("Please enter a valid URL glob pattern (must start with 'http://' or 'https://').")
            continue
        glob_list.append(user_input)
    return glob_list
