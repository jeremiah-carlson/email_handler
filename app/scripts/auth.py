from scripts.setup import secrets


def auth(role: str, passWd: str)-> bool: # x-api-key auth via header
    return passWd in secrets['roles'][role]