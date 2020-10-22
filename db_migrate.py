import sys
import json
import re
import github
from common.Instance import Instance
from models.Issue import Issue
from models.Comment import Comment


def main(argv):

    instance = Instance()
    instance.migrate()


if __name__ == "__main__":
    main(sys.argv)
