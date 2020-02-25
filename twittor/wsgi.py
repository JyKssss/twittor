import os,sys

sys.path.insert(0,os.getcwd())

from twittor import create_app

application = create_app()

# CREATE DATABASE twittor CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;