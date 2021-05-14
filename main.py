import matplotlib
import webbrowser

from web_app.app import get_app

matplotlib.use('agg')  # Use non-GUI backend

# Default configuration dictionary
defaults = {
    "size": 50,
    "duration": 100,
    "cases": 2,
    "length": 14,
    "probabilities": {
        "Infection": {50: 0.1, 60: 0.1, 70: 0.1, 80: 0.1, 100: 0.1},
        "Recovery": {50: 0.7, 60: 0.7, 70: 0.7, 80: 0.7, 100: 0.7},
        "Death": {50: 0.01, 60: 0.02, 70: 0.04, 80: 0.08, 100: 0.15},
    },
    "vaccinator": {
        "start": 20,
        "rate": 0.25,
        "max": 20,
    },
    "measures": {
        "Lockdown": {"enabled": False, "starts": [25], "ends": [75], "multiplier": 0.5},
        "Social Distancing": {"enabled": False, "starts": [10], "ends": [], "multiplier": 0.5},
        "Improved Treatment": {"enabled": True, "starts": [50], "ends": [], "multiplier": 1.25},
        "Ventilators": {"enabled": False, "starts": [0], "ends": [], "multiplier": 0.6},
    }
}


def main():
    app = get_app(defaults=defaults)  # Get dash web app
    webbrowser.open("http://127.0.0.1:8050", new=1)  # Open web browser
    app.run_server()  # Serve web app


if __name__ == "__main__":
    main()
