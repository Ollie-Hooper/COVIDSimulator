from web_app.app import get_app

defaults = {
    "size": 50,
    "duration": 100,
    "cases": 2,
    "probabilities": {
        "infection": {50: 0.4, 60: 0.4, 70: 0.4, 80: 0.4, 100: 0.4},
        "recovery": {50: 0.7, 60: 0.7, 70: 0.7, 80: 0.7, 100: 0.7},
        "death": {50: 0.01, 60: 0.02, 70: 0.04, 80: 0.08, 100: 0.15},
    }
}


def main():
    app = get_app(defaults=defaults)
    app.run_server()


if __name__ == "__main__":
    main()
