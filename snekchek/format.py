def flake8_format(data: list) -> None:
    for row in data:
        print(
            f"{row['path']}:{row['line']}:{row['col']}: {row['errcode']} {row['msg']}"
        )


def vulture_format(data: list) -> None:
    for row in data:
        print(
            f"{row['path']}:{row['line']}: {row['err']} ({row['conf']}% confidence)"
        )


def pylint_format(data: list) -> None:
    last_path = ""
    for row in data:
        if row['path'] != last_path:
            print(f"File: {row['path']}")
            last_path = row['path']

        print(
            f"{row['type'][0].upper()}:{row['line']:>3}, {row['column']:>2}: "
            f"{row['message']} ({row['symbol']})")


def pyroma_format(data: dict) -> None:
    for row in list(data['modules'].values())[0]:
        print(row)


def isort_format(data: list) -> None:
    for diff in data:
        print(diff)


def yapf_format(data: list) -> None:
    for row in data:
        print(row)


def pypi_format(data: list) -> None:
    for row in data:
        print(row)
