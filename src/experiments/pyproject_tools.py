from pathlib import Path

import toml


def load_pyproject():
    with open(f"{project_root()}/pyproject.toml", "r") as pyproject_file:
        pyproject_data = toml.load(pyproject_file)

    return pyproject_data


def get_package_name():
    pyproject_data = load_pyproject()

    package_name = pyproject_data["tool"]["poetry"]["name"]
    return package_name


def project_root() -> str:
    return str(Path(__file__).parent.parent.parent)


def source_root() -> str:
    return str(Path(__file__).parent.parent)


def actors_folder() -> str:
    return str(Path(__file__).parent.parent / "actors")


def messages_folder() -> str:
    return str(Path(__file__).parent.parent / "messages")


if __name__ == "__main__":
    print(actors_folder())
