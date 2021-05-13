from web_app.app import get_app

defaults = {
    "size": 50,
    "duration": 100,
    "cases": 2,
    "probabilities": {
        "infection": {50: 0.1, 60: 0.1, 70: 0.1, 80: 0.1, 100: 0.1},
        "recovery": {50: 0.7, 60: 0.7, 70: 0.7, 80: 0.7, 100: 0.7},
        "death": {50: 0.01, 60: 0.02, 70: 0.04, 80: 0.08, 100: 0.15},
    },
    "vaccinator": {
        "start": 20,
        "rate": 0.25,
        "max": 20,
    },
    "measures": {
        "Lockdown": {"starts": [25], "ends": [75], "multiplier": 0.5},
        "Social Distancing": {"starts": [10], "ends": [], "multiplier": 0.5},
        "Improved Treatment": {"starts": [50], "ends": [], "multiplier": 1.25},
        "Ventilators": {"starts": [0], "ends": [], "multiplier": 0.6},
    }
}


def main():
    app = get_app(defaults=defaults)
    app.run_server()


if __name__ == "__main__":
    main()
