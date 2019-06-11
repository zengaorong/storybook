#coding=utf-8
import sys
reload(sys)
import threading
import ConfigParser
import time
import datetime
import os
from operatedb import check_story_by_author_and_story
sys.setdefaultencoding('utf-8')


if __name__ == '__main__':
    cf = ConfigParser.ConfigParser()
    cf.read(os.getcwd()+"/seting.config")
    print cf.sections()
    for section in cf.sections():
        author = cf.get(section, "author")
        story = cf.get(section, "story")
        check_story_by_author_and_story(author,story)

        print check_story_by_author_and_story(author,story)


