# covid-vaccine-spotter-checker

Super quick and dirty script. Checks [COVID-19 Vaccine Spotter](https://www.vaccinespotter.org/) website every (default) 30 seconds to see if vaccines are available in a state -- plays sound if vaccine is found. Works on Windows (tested) and Mac/Linux (in theory, haven't tested). Uses the "Very Beta API" on Vaccine Spotter, is subject to breaking.

## Usage

Run `python check_vaccine_spotter.py` from Terminal or Command Prompt. Follow the on-screen prompts to enter your OS, U.S. state, and specified refresh rate. Press `Ctrl + C` to terminate script.

Alternatively, if you do not have Python installed, download the executable for respective OS (Windows or Mac/Linux) [here](https://github.com/vsub21/covid-vaccine-spotter-checker/releases/tag/v1.0) and run. For Windows, double-click the .exe file after downloading. For Mac/Linux, open Terminal, navigate to the folder containing the downloaded file, and type `./check_vaccine_spotter`.
