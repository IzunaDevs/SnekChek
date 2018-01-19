
def flake8_format(data):
    for row in data:
        print(f"{row['path']}:{row['line']}:{row['col']}: {row['errcode']} {row['msg']}")


def vulture_format(data):
    for row in data:
        print(f"{row['path']}:{row['line']}: {row['err']} ({row['conf']}% confidence)")


def pylint_format(data):
    last_path = ""
    for row in data:
        if row['path'] != last_path:
            print(f"File: {row['path']}")
            last_path = row['path']

        print(f"{row['message-id'][0]}:{row['line']:>3}, {row['column']:>2}: "
              f"{row['message']} ({row['symbol']})")
