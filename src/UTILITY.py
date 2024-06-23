from requests import get


def read_token() -> str:
    with open("token.txt") as token:
        token = token.read()
        token = token.splitlines()
        token = [item for item in token if item != '']
        token = ''.join(token)
        token = [item for item in token if item != ' ']
        token = ''.join(token)
    return token


def validate_token(token, bot: bool = False) -> bool:
    headers = {"Authorization": token}
    if bot is True:
        headers = {"Authorization":f"Bot {token}"}
    response = get(f"https://discord.com/api/v9/users/@me", headers=headers)
    print(response.json())
    if response.status_code != 200:
        return False
    return True

if __name__ == '__main__':
    print(validate_token(read_token()))
