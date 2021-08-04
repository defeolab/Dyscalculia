import xml.etree.ElementTree as ET
from settings import Settings

# Code adapted from https://stackabuse.com/reading-and-writing-xml-files-in-python/#disqus_thread

def save_to_xml(settings):

    # create the file structure
    data = ET.Element('data')
    parameters = ET.SubElement(data, 'parameters')
    ratio = ET.SubElement(parameters, 'ratio')
    average_space_between = ET.SubElement(parameters, 'average_space_between')
    size_of_chicken = ET.SubElement(parameters, 'size_of_chicken')
    total_area_occupied = ET.SubElement(parameters, 'total_area_occupied')
    chicken_show_time = ET.SubElement(parameters, 'chicken_show_time')

    ratio.set('min', str(settings.ratio_min))
    ratio.set('max', str(settings.ratio_max))
    average_space_between.set('min', str(settings.average_space_between_min))
    average_space_between.set('max', str(settings.average_space_between_max))
    size_of_chicken.set('min', str(settings.size_of_chicken_min))
    size_of_chicken.set('max', str(settings.size_of_chicken_max))
    total_area_occupied.set('min', str(settings.total_area_occupied_min))
    total_area_occupied.set('max', str(settings.total_area_occupied_max))
    chicken_show_time.set('min', str(settings.chicken_show_time_min))
    chicken_show_time.set('max', str(settings.chicken_show_time_max))

    # create a new XML file with the results
    mydata = ET.tostring(data).decode()
    myfile = open("settings.xml", "w")
    myfile.write(mydata)
    myfile.close()


def load_from_xml():
    print("Loading Settings")
    tree = ET.parse('settings.xml')
    root = tree.getroot()

    ratio_min = float(root[0][0].attrib['min'])
    ratio_max = float(root[0][0].attrib['max'])
    average_space_between_min = float(root[0][1].attrib['min'])
    average_space_between_max = float(root[0][1].attrib['max'])
    size_of_chicken_min = float(root[0][2].attrib['min'])
    size_of_chicken_max = float(root[0][2].attrib['max'])
    total_area_occupied_min = float(root[0][3].attrib['min'])
    total_area_occupied_max = float(root[0][3].attrib['max'])
    chicken_show_time_min = float(root[0][4].attrib['min'])
    chicken_show_time_max = float(root[0][4].attrib['max'])
    max_trial_time_min = float(root[0][5].attrib['min'])
    max_trial_time_max = float(root[0][5].attrib['max'])

    return Settings(ratio_min, ratio_max, average_space_between_min, average_space_between_max, size_of_chicken_min, size_of_chicken_max, total_area_occupied_min, total_area_occupied_max, chicken_show_time_min, chicken_show_time_max, max_trial_time_min, max_trial_time_max)
