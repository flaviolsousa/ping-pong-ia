import configparser

config = configparser.ConfigParser()
config.read('config.ini')

TRAINING = config["APP"].getboolean("TRAINING", True)

group = "TRAINING" if TRAINING else "APP"

FRAMES_PER_SECOND = config[group].getint("FRAMES_PER_SECOND", 60)
INITIAL_RECORD = config[group].getint("INITIAL_RECORD")

LR = config[group].getfloat("LR")
GAMMA = config[group].getfloat("GAMMA")
MAX_LOSSES = config[group].getint("MAX_LOSSES")
EXPLORATION_GAMES = config[group].getint("EXPLORATION_GAMES")
