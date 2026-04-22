from utils import args
import time
from Matrix import Matrix
from datetime import date
import datetime
import random

COUNTRIES = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola",
    "Antigua & Barbuda", "Argentina", "Armenia", "Australia", "Austria",
    "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados",
    "Belarus", "Belgium", "Belize", "Benin", "Bhutan",
    "Bolivia", "Bosnia", "Botswana", "Brazil", "Brunei",
    "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia",
    "Cameroon", "Canada", "C.A.R.", "Chad", "Chile",
    "China", "Colombia", "Comoros", "Congo", "Costa Rica",
    "Croatia", "Cuba", "Cyprus", "Czechia", "Denmark",
    "Djibouti", "Dominica", "Dominican Rep.", "DR Congo", "Ecuador",
    "Egypt", "El Salvador", "Eq. Guinea", "Eritrea", "Estonia",
    "Eswatini", "Ethiopia", "Fiji", "Finland", "France",
    "Gabon", "Gambia", "Georgia", "Germany", "Ghana",
    "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau",
    "Guyana", "Haiti", "Honduras", "Hungary", "Iceland",
    "India", "Indonesia", "Iran", "Iraq", "Ireland",
    "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan",
    "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kosovo",
    "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon",
    "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania",
    "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives",
    "Mali", "Malta", "Marshall Isl.", "Mauritania", "Mauritius",
    "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia",
    "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia",
    "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua",
    "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway",
    "Oman", "Pakistan", "Palau", "Palestine", "Panama",
    "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland",
    "Portugal", "Qatar", "Romania", "Russia", "Rwanda",
    "Samoa", "San Marino", "Sao Tome", "Saudi Arabia", "Senegal",
    "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia",
    "Slovenia", "Solomon Isl.", "Somalia", "South Africa", "South Korea",
    "South Sudan", "Spain", "Sri Lanka", "St. Kitts&Nevis", "St. Lucia",
    "St. Vincent", "Sudan", "Suriname", "Sweden", "Switzerland",
    "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand",
    "Timor-Leste", "Togo", "Tonga", "Trinidad&Tobago", "Tunisia",
    "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine",
    "UAE", "UK", "USA", "Uruguay", "Uzbekistan",
    "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen",
    "Zambia", "Zimbabwe",
]

def center_text(text, matrix_width=64, char_width=4, char_spacing=1):
    text_width = len(text) * char_width + (len(text) - 1) * char_spacing
    x_position = (matrix_width - text_width) // 2
    return max(x_position, 0)

def get_country_of_the_day():
    today = date.today()
    random.seed(today.toordinal())
    return random.choice(COUNTRIES)

if __name__ == "__main__":
    cliArgs = args()

    matrix_width = 64
    matrix_height = 64
    matrix = Matrix(matrix_width, matrix_height,
                    brightness=cliArgs.led_brightness, debug=cliArgs.debug)

    # Split
    workout_split = [ "Push", "Run/Mobility", "Pull", "Legs" ]
    workout_split_seed = 2

    # Start date: October 2, 2025
    start_date = datetime.datetime(2025, 10, 2, 0, 0, 0)

    # Country of the day (recomputed when date changes at midnight)
    last_country_date = None
    country = ""

    while True:
        try:
            current_time = datetime.datetime.now()
            elapsed = current_time - start_date

            day = (elapsed.days) + 1

            # Update country when the date changes
            today = date.today()
            if today != last_country_date:
                country = get_country_of_the_day()
                last_country_date = today

            workout = workout_split[(day + workout_split_seed) % len(workout_split)]
            time_str = current_time.strftime('%I:%M:%S %p')

            # --- Country section ---
            matrix.drawText("COUNTRY", "small", (center_text("COUNTRY", char_width=3), 7), (80, 80, 80))
            matrix.drawText(country, "medium", (center_text(country), 17), (230, 180, 60))

            # --- Separator ---
            matrix.drawHLine(21, 4, 59, (40, 40, 40))

            # --- Workout section ---
            matrix.drawText(f"Day {day}", "medium", (center_text(f"Day {day}"), 32), (220, 220, 220))
            matrix.drawText(workout, "medium", (center_text(workout), 43), (180, 180, 180))
            matrix.drawText(time_str, "medium", (center_text(time_str), 54), (80, 80, 80))

        except Exception as e:
            print(f"Exception: {e}")

        matrix.debugShow()

        time.sleep(1)  # Update every second
        matrix.clear()
