from colored import attr, fg


def colorize(message: str, color: str = "yellow_1") -> str:
    return f"{fg(color)}{message}{attr('reset')}"


def log(message: str, color: str = "yellow_1") -> None:
    print(colorize(message, color))
