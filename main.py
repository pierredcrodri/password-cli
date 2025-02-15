import typer
import sys
import json
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()

arg = sys.argv

registered_passwords = []


def read_save():
    global registered_passwords
    with open(".password", "r") as file:
        registered_passwords = json.loads(file.read())
        file.close()


def write_save():
    with open(".password", "w") as file:
        json.dump(registered_passwords, file)


try:
    read_save()
except FileNotFoundError:
    write_save()


@app.command()
def register(alias: str, password: str):
    registered_passwords.append([alias, password])
    write_save()


@app.command()
def view():
    if len(registered_passwords) > 0:
        table = Table("Alias", "Password")
        for password in registered_passwords:
            table.add_row(password[0], password[1])
        console.print(table)
    else:
        print("No passwords to view.")


@app.command()
def remove(alias: str, password: str):
    try:
        registered_passwords.remove([ alias, password ])
        write_save()
        print("Password successfully removed!")
    except ValueError:
        print(f"Didn't find the password {alias}.")


@app.command()
def see(alias: str):
    found_password = False
    for password in registered_passwords:
        if password[0] == alias:
            found_password = True
            print(password[1])
    if not found_password:
        print(f"Couldn't find password with the alias: \"{alias}\"")


if __name__ == "__main__":
    app()

# print("Nefertari's Password Utility")
# print("Use the \"help\" command if you want to know how to use this CLI.")