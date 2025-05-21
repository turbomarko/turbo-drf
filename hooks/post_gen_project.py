import random
import shutil
import string
from pathlib import Path

try:
    # Inspired by
    # https://github.com/django/django/blob/master/django/utils/crypto.py
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    using_sysrandom = False

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "

DEBUG_VALUE = "debug"


def remove_open_source_files():
    file_names = ["CONTRIBUTORS.txt", "LICENSE"]
    for file_name in file_names:
        Path(file_name).unlink()


def remove_gplv3_files():
    file_names = ["COPYING"]
    for file_name in file_names:
        Path(file_name).unlink()


def remove_custom_user_manager_files():
    users_path = Path("{{cookiecutter.project_slug}}", "users")
    (users_path / "managers.py").unlink()
    (users_path / "tests" / "test_managers.py").unlink()


def remove_user_serliazer_tests():
    (Path("api", "users", "tests", "test_serializers.py")).unlink()


def remove_nginx_docker_files():
    shutil.rmtree(Path("compose", "production", "nginx"))


def remove_celery_files():
    file_paths = [
        Path("config", "celery_app.py"),
        Path("{{ cookiecutter.project_slug }}", "users", "tasks.py"),
        Path("{{ cookiecutter.project_slug }}", "users", "tests", "test_tasks.py"),
    ]
    for file_path in file_paths:
        file_path.unlink()


def remove_async_files():
    file_paths = [
        Path("config", "asgi.py"),
        Path("config", "websocket.py"),
    ]
    for file_path in file_paths:
        file_path.unlink()


def remove_dotgitlabciyml_file():
    Path(".gitlab-ci.yml").unlink()


def remove_dotgithub_folder():
    shutil.rmtree(".github")


def remove_dotdrone_file():
    Path(".drone.yml").unlink()


def generate_random_string(length, using_digits=False, using_ascii_letters=False, using_punctuation=False):
    """
    Example:
        opting out for 50 symbol-long, [a-z][A-Z][0-9] string
        would yield log_2((26+26+50)^50) ~= 334 bit strength.
    """
    if not using_sysrandom:
        return None

    symbols = []
    if using_digits:
        symbols += string.digits
    if using_ascii_letters:
        symbols += string.ascii_letters
    if using_punctuation:
        all_punctuation = set(string.punctuation)
        # These symbols can cause issues in environment variables
        unsuitable = {"'", '"', "\\", "$"}
        suitable = all_punctuation.difference(unsuitable)
        symbols += "".join(suitable)
    return "".join([random.choice(symbols) for _ in range(length)])


def set_flag(file_path: Path, flag, value=None, formatted=None, *args, **kwargs):
    if value is None:
        random_string = generate_random_string(*args, **kwargs)
        if random_string is None:
            print(
                "We couldn't find a secure pseudo-random number generator on your "
                "system. Please, make sure to manually {} later.".format(flag)
            )
            random_string = flag
        if formatted is not None:
            random_string = formatted.format(random_string)
        value = random_string

    with file_path.open("r+") as f:
        file_contents = f.read().replace(flag, value)
        f.seek(0)
        f.write(file_contents)
        f.truncate()

    return value


def set_django_secret_key(file_path: Path):
    django_secret_key = set_flag(
        file_path,
        "!!!SET DJANGO_SECRET_KEY!!!",
        length=64,
        using_digits=True,
        using_ascii_letters=True,
    )
    return django_secret_key


def set_django_admin_url(file_path: Path):
    django_admin_url = set_flag(
        file_path,
        "!!!SET DJANGO_ADMIN_URL!!!",
        formatted="{}/",
        length=32,
        using_digits=True,
        using_ascii_letters=True,
    )
    return django_admin_url


def generate_random_user():
    return generate_random_string(length=32, using_ascii_letters=True)


def generate_postgres_user(debug=False):
    return DEBUG_VALUE if debug else generate_random_user()


def set_postgres_user(file_path, value):
    postgres_user = set_flag(file_path, "!!!SET POSTGRES_USER!!!", value=value)
    return postgres_user


def set_postgres_password(file_path, value=None):
    postgres_password = set_flag(
        file_path,
        "!!!SET POSTGRES_PASSWORD!!!",
        value=value,
        length=64,
        using_digits=True,
        using_ascii_letters=True,
    )
    return postgres_password


def set_celery_flower_user(file_path, value):
    celery_flower_user = set_flag(file_path, "!!!SET CELERY_FLOWER_USER!!!", value=value)
    return celery_flower_user


def set_celery_flower_password(file_path, value=None):
    celery_flower_password = set_flag(
        file_path,
        "!!!SET CELERY_FLOWER_PASSWORD!!!",
        value=value,
        length=64,
        using_digits=True,
        using_ascii_letters=True,
    )
    return celery_flower_password


def append_to_gitignore_file(ignored_line):
    with Path(".gitignore").open("a") as gitignore_file:
        gitignore_file.write(ignored_line)
        gitignore_file.write("\n")


def set_flags_in_envs(postgres_user, celery_flower_user, debug=False):
    local_django_envs_path = Path(".envs", ".local", ".django")
    production_django_envs_path = Path(".envs", ".production", ".django")
    local_postgres_envs_path = Path(".envs", ".local", ".postgres")
    production_postgres_envs_path = Path(".envs", ".production", ".postgres")

    set_django_secret_key(production_django_envs_path)
    set_django_admin_url(production_django_envs_path)

    set_postgres_user(local_postgres_envs_path, value=postgres_user)
    set_postgres_password(local_postgres_envs_path, value=DEBUG_VALUE if debug else None)
    set_postgres_user(production_postgres_envs_path, value=postgres_user)
    set_postgres_password(production_postgres_envs_path, value=DEBUG_VALUE if debug else None)

    set_celery_flower_user(local_django_envs_path, value=celery_flower_user)
    set_celery_flower_password(local_django_envs_path, value=DEBUG_VALUE if debug else None)
    set_celery_flower_user(production_django_envs_path, value=celery_flower_user)
    set_celery_flower_password(production_django_envs_path, value=DEBUG_VALUE if debug else None)


def set_flags_in_settings_files():
    set_django_secret_key(Path("config", "settings", "local.py"))
    set_django_secret_key(Path("config", "settings", "test.py"))


def remove_celery_compose_dirs():
    shutil.rmtree(Path("compose", "local", "django", "celery"))
    shutil.rmtree(Path("compose", "production", "django", "celery"))


def remove_aws_dockerfile():
    shutil.rmtree(Path("compose", "production", "aws"))


def main():
    debug = "{{ cookiecutter.debug }}".lower() == "y"

    set_flags_in_envs(
        DEBUG_VALUE if debug else generate_random_user(),
        DEBUG_VALUE if debug else generate_random_user(),
        debug=debug,
    )
    set_flags_in_settings_files()

    if "{{ cookiecutter.open_source_license }}" == "Not open source":
        remove_open_source_files()
    if "{{ cookiecutter.open_source_license}}" != "GPLv3":
        remove_gplv3_files()

    if "{{ cookiecutter.username_type }}" == "username":
        remove_custom_user_manager_files()
        remove_user_serliazer_tests()

    if "{{ cookiecutter.cloud_provider }}".lower() != "none":
        remove_nginx_docker_files()

    if "{{ cookiecutter.cloud_provider}}" != "AWS":
        remove_aws_dockerfile()

    if "{{ cookiecutter.keep_local_envs_in_vcs }}".lower() == "y":
        append_to_gitignore_file("!.envs/.local/")

    if "{{ cookiecutter.use_celery }}".lower() == "n":
        remove_celery_files()
        remove_celery_compose_dirs()

    if "{{ cookiecutter.ci_tool }}" != "Gitlab":
        remove_dotgitlabciyml_file()

    if "{{ cookiecutter.ci_tool }}" != "Github":
        remove_dotgithub_folder()

    if "{{ cookiecutter.ci_tool }}" != "Drone":
        remove_dotdrone_file()

    if "{{ cookiecutter.use_async }}".lower() == "n":
        remove_async_files()

    print(SUCCESS + "Project initialized, keep up the good work!" + TERMINATOR)


if __name__ == "__main__":
    main()
