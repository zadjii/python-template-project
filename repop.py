from common.ResultAndData import *
from common.Instance import Instance
from models.Issue import Issue
from models.Comment import Comment


def main():
    instance = Instance()
    db = instance.get_db()

    # This file should be used for some quick populating of the DB with dummy data.
    # currently, it does nothing.

if __name__ == "__main__":
    main()
