
def flake8_format(data):
    for row in data:
        print(f"{row['path']}:{row['line']}:{row['col']}: {row['errcode']} {row['msg']}")


def vulture_format(data):
    for row in data:
        print(f"{row['path']}:{row['line']}: {row['err']} ({row['conf']}% confidence)")
