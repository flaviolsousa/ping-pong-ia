import configparser

config = configparser.ConfigParser()
config.read('config.ini')

FRAMES_PER_SECOND_DEFAULT = config["DEFAULT"].getint(
    "FRAMES_PER_SECOND_DEFAULT", 60)
FRAMES_PER_SECOND_TRAINING = config["DEFAULT"].getint(
    "FRAMES_PER_SECOND_TRAINING", 1000)
INITIAL_RECORD = config["DEFAULT"].getint("INITIAL_RECORD")

LR = config["DEFAULT"].getfloat("LR")
GAMMA = config["DEFAULT"].getfloat("GAMMA")
MAX_LOSSES = config["DEFAULT"].getint("MAX_LOSSES")
EXPLORATION_GAMES = config["DEFAULT"].getint("EXPLORATION_GAMES")
