from web_app.app import get_app

defaults = {
    "size": 50,
    "duration": 100,
    "cases": 2,
}


def main():
    app = get_app(defaults=defaults)
    app.run_server()


if __name__ == "__main__":
    main()
