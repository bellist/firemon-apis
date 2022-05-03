""" Configuring configparser """
from configparser import ConfigParser
import os

thisfolder = os.path.dirname(os.path.abspath(__file__))
initfile = os.path.join(thisfolder, 'application.properties')

def get_properties_data():
    """ Returning a parser which will be used to read
        application.properties file data """
    parser = ConfigParser()
    parser.read(initfile)
    return parser