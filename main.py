from web_app.app import get_app


def main():
    app = get_app()
    app.run_server()


if __name__ == "__main__":
    main()
