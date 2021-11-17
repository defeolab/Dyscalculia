import PySimpleGUI as sg
import settings_manager
from settings import Settings

title_column = [
    [sg.Text("Ratio - ")],
    [sg.Text("Average Space Between - ")],
    [sg.Text("Size Of Chicken - ")],
    [sg.Text("Total Area Occupied - ")]
]

input_column = [
    [sg.Text("Min:"), sg.In("0.5", size=(3, 1), key="RATIO_MIN"), sg.Text("Max:"), sg.In("1.4", size=(3, 1), key="RATIO_MAX")],
    [sg.Text("Min:"), sg.In("0.7", size=(3, 1), key="AVG_SPACE_MIN"), sg.Text("Max:"), sg.In("1.2", size=(3, 1), key="AVG_SPACE_MAX")],
    [sg.Text("Min:"), sg.In("1.2", size=(3, 1), key="SIZE_MIN"), sg.Text("Max:"), sg.In("2", size=(3, 1), key="SIZE_MAX")],
    [sg.Text("Min:"), sg.In("10", size=(3, 1), key="TOTAL_AREA_MIN"), sg.Text("Max:"), sg.In("15", size=(3, 1), key="TOTAL_AREA_MAX")],
    [sg.Text("Min:"), sg.In("2", size=(3, 1), key="CHICKEN_SHOW_MIN"), sg.Text("Max:"), sg.In("4", size=(3, 1), key="CHICKEN_SHOW_MAX")],
]

layout = [
    [sg.Column(title_column), sg.Column(input_column)],
    [sg.Button("Close"), sg.Button("Save")]
]

# Create the window
window = sg.Window("Demo", layout)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "Close" or event == sg.WIN_CLOSED:
        break
    elif event == "Save":
        ratio_min = values["RATIO_MIN"]
        ratio_max = values["RATIO_MAX"]
        average_space_between_min = values["AVG_SPACE_MIN"]
        average_space_between_max = values["AVG_SPACE_MAX"]
        size_of_chicken_min = values["SIZE_MIN"]
        size_of_chicken_max = values["SIZE_MAX"]
        total_area_occupied_min = values["TOTAL_AREA_MIN"]
        total_area_occupied_max = values["TOTAL_AREA_MAX"]
        chicken_show_time_min = values["CHICKEN_SHOW_MIN"]
        chicken_show_time_max = values["CHICKEN_SHOW_MAX"]
        new_settings = Settings(ratio_min, ratio_max, average_space_between_min, average_space_between_max, size_of_chicken_min, size_of_chicken_max, total_area_occupied_min, total_area_occupied_max, chicken_show_time_min, chicken_show_time_max)
        settings_manager.save_to_xml(new_settings)
        print("Settings Saved")

window.close()
