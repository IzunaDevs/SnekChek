"""Formatting functions for each linter"""


def flake8_format(data: list) -> None:
    for row in data:
        print(
            ("{row['path']}:{row['line']}:{row['col']}: "
             "{row['errcode']} {row['msg']}").format(row=row)
        )


def vulture_format(data: list) -> None:
    for row in data:
        print(
            ("{row['path']}:{row['line']}: "
             "{row['err']} ({row['conf']}% confidence)").format(row=row)
        )


def pylint_format(data: list) -> None:
    last_path = ""
    for row in data:
        if row['path'] != last_path:
            print("File: {row['path']}".format(row=row))
            last_path = row['path']

        print(
            ("{row['type'][0].upper()}:{row['line']:>3}, {row['column']:>2}: "
             "{row['message']} ({row['symbol']})").format(row=row))


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


def safety_format(data: list) -> None:
    for row in data:
        print("[{row[4]}] ({row[0]+row[1]}) {row[3]}".format(row=row))


def dodgy_format(data: list) -> None:
    for row in data:
        print("{row[1]}:{row[0]}: {row[2]}".format(row=row))


def pytest_format(data: list) -> None:
    for test in data:
        print(test['name'])
        print(test['call']['longrepr'])
