import functools
import io
import pathlib
import random
import string

import click
import dotenv
import fabric
import invoke
from patchwork import files


def info(info):
    """Display some information."""
    click.secho(info, fg="green", bold=True)


def sub_info(info):
    """Display some sub-information."""
    click.secho(info, fg="red", bold=True)


def style_as_prompt(text):
    """Style some text as a prompt."""
    return click.style(text, bold=True)


def confirm(message):
    """Display a confirmation prompt."""
    return click.confirm(style_as_prompt(message))


def prompt(message):
    """Display a prompt."""
    return click.prompt(style_as_prompt(message))


def exit_on_nonzero(f):
    """Exit the wrapped function when an UnexpectedExit exception is raised."""

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except invoke.runners.UnexpectedExit:
            exit()

    return wrapper


def validate_file_path(ctx, param, value):
    """Validate that a path exists and represents a file."""
    if value is not None:
        if not value.exists():
            raise click.BadParameter(f"{value} doesn't exist")
        elif not value.is_file():
            raise click.BadParameter(f"{value} isn't a file")

    return value


@click.command(context_settings={"max_content_width": 100})
@click.argument("destination", type=str)
@click.option("--repo", "-r", type=str, help="Repository to pull the source from.", metavar="<REPO>")
@click.option(
    "--checkout",
    "-c",
    type=str,
    default="master",
    help="Branch/commit to checkout.",
    show_default=True,
    metavar="<BRANCH/COMMIT>",
)
@click.option("--env", "-e", "env_args", type=str, multiple=True, help="Set environment variable.", metavar="<VAR=VAL>")
@click.option(
    "--env-file",
    "-f",
    type=pathlib.Path,
    callback=validate_file_path,
    help="Path to .env file to read variables from. Variables set with --env/-e will override these.",
    metavar="<PATH>",
)
@exit_on_nonzero
def deploy(destination, repo, checkout, env_args, env_file):
    """
    \b
    Deploy the application by:
      - pulling the latest source and checking out a branch/commit
      - updating the remote .env file
      - building the Docker Compose services
      - applying the database migrations
      - collecting the static files together
      - starting the Docker containers
    """
    c = fabric.Connection(host=destination)

    app_dir = f"/home/{c.user}/app"
    c.run(f"mkdir -p {app_dir}")

    with c.cd(app_dir):
        pull_latest_source(c, repo, checkout)
        create_or_update_dot_env(c, env_args, env_file)
        build_services(c)
        apply_migrations(c)
        collect_static(c)
        start_containers(c)

    info("Deployment complete")


def pull_latest_source(c: fabric.Connection, repo, checkout):
    """Pull the latest source and checkout the desired branch/commit."""
    info(f"Pulling the latest source and checking out {checkout}")

    if files.exists(c, ".git"):
        sub_info("Resetting the working tree")
        c.run("git reset --hard")

        sub_info("Fetching the latest source")
        c.run(f"git fetch origin {checkout}")
    else:
        if repo is None:
            repo = prompt("Enter repository to pull source from")

        sub_info(f"Cloning {repo}")
        c.run(f"git clone {repo} .")

    sub_info(f"Checking out {checkout}")
    c.run(f"git checkout {checkout}")


def create_or_update_dot_env(c: fabric.Connection, env_args, env_file):
    """
    Create or update the remote .env file by merging its contents with the
    variables passed in as CLI args and the contents of the passed in local .env
    file. Generate SECRET_KEY if not provided and prompt for DOMAIN/EMAIL if not
    provided.
    """
    info("Creating/updating the remote .env")

    local_env = {}

    if env_file:
        sub_info(f"Reading variables from {env_file}")
        file_env = dotenv.dotenv_values(env_file)
        local_env.update(file_env)

    if env_args:
        sub_info("Compiling variables passed through CLI")
        cli_env_content = "\n".join(env_args)
        cli_env = dotenv.dotenv_values(stream=io.StringIO(cli_env_content))
        local_env.update(cli_env)

    if files.exists(c, ".env"):
        sub_info("Reading variables from remote .env")
        remote_env_content = c.run("cat .env", hide=True).stdout
        remote_env = dotenv.dotenv_values(stream=io.StringIO(remote_env_content))
    else:
        remote_env = {}

    for key, value in local_env.items():
        if key in remote_env:
            prompt_text = f"{key} is already set to {remote_env[key]}, are you sure that you want to set it to {value}?"
            if not confirm(prompt_text):
                continue
        sub_info(f"Setting {key} to {value}")
        remote_env[key] = value

    if not remote_env.get("SECRET_KEY"):
        sub_info("Generating value for SECRET_KEY")
        remote_env["SECRET_KEY"] = "".join(random.choices(string.ascii_letters + string.digits, k=50))

    for key in ["DOMAIN", "EMAIL"]:
        while not remote_env.get(key):
            value = prompt(f"Enter value for {key}")
            remote_env[key] = value

    sub_info("Writing variables to remote .env")
    remote_env_content = "\n".join(f"{key}={value or ''}" for key, value in remote_env.items())
    remote_env_content_bytes = io.BytesIO(remote_env_content.encode("utf-8"))
    c.put(remote_env_content_bytes, f"{c.cwd}/.env")


def build_services(c):
    """Build the Docker Compose services."""
    info("Building the Docker Compose services")
    c.run("docker-compose build")


def apply_migrations(c):
    """Apply the database migrations."""
    info("Applying the database migrations")
    c.run("docker-compose run app python manage.py migrate --noinput")


def collect_static(c):
    """Collecting the static files."""
    info("Collecting the static files")
    c.run("docker-compose run app python manage.py collectstatic --noinput")


def start_containers(c):
    """Start the Docker containers."""
    info("Starting the Docker containers")

    sub_info("Stopping and removing any exitisting containers")
    c.run("docker-compose down")

    sub_info("Starting up the new containers")
    c.run("docker-compose up -d")


if __name__ == "__main__":
    deploy()
