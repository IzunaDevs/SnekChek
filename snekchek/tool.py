
import subprocess
import twine.commands.upload


def get_tools():
    return [Pypi]


class Pypi(Linter):
    def run(self, _: list) -> None:
        proc = subprocess.Popen([sys.executable, "setup.py", "sdist", "bdist"])
        proc.wait()
        twine.commands.upload.upload(["dist/*"], self.conf.get("TWINE_REPOSITORY"),
                                     self.conf.as_bool("sign", False), self.conf.get("identity"),
                                     self.conf["TWINE_USERNAME"], self.conf["TWINE_PASSWORD"],
                                     self.conf.get("comment"), self.confpath,
                                     self.conf.get("skip-existing", True), None, None,
                                     self.conf.get("TWINE_REPOSITORY_URL"))
