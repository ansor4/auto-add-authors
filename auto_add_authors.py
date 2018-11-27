#!/usr/bin/env python3

import os
import sys
import git
import yaml


def format_email(formatted_email):
    if formatted_email[0] != '<' or formatted_email[-1] != '>':
        return None
    return formatted_email[1:-1]


def process_line(line):
    tokens = line.split()
    if len(tokens) < 3:
        return None, None
    email = tokens.pop()
    email = format_email(email)
    if email is None:
        return None, None
    # Throw away first token(number of commits)
    tokens.pop(0)
    initials = None
    if len(tokens) >= 2:
        # Guess initials
        initials = "".join([name[0].lower() for name in tokens])
    name = " ".join(tokens)

    return initials, email, name


def process_gitlog():

    cwd = os.getcwd()

    if not os.path.exists(cwd + "/.git"):
        print("No git repo found here")
        sys.exit(1)

    r = git.Repo.init(cwd)
    log = r.git.shortlog(s=True, e=True)

    lines = log.split('\n')
    return [process_line(l) for l in lines]


if __name__ == '__main__':

    seen_initials = set()
    seen_emails = set()
    distinct_users = []

    # For now just alter git-authors
    # TODO: create .mailmap
    lines = process_gitlog()
    for initials, email, name in lines:
        print(initials, email, name)
        # TODO: fuzzy matching names
        if initials is None:
            continue
        if email in seen_emails:
            continue
        if initials in seen_initials:
            continue
        seen_emails.add(email)
        seen_initials.add(initials)
        distinct_users.append((initials, email, name))

    print("\nfound these unique initials")
    for u in distinct_users:
        print(u)

    print("\nAdding them to .git-authors")
    git_author_path = os.path.expanduser("~/.git-authors")
    if not os.path.exists(git_author_path):
        git_authors = yaml.safe_load(open(git_author_path, "w+"))
        authors = {}
        email_addresses = {}
        for initials, email, name in distinct_users:
            authors[initials] = name
            email_addresses[initials] = email

        git_authors = dict(
            authors=authors, email_addresses=email_addresses)

    else:
        git_authors = yaml.safe_load(open(git_author_path, "r"))
        for initials, email, name in distinct_users:
            if initials in git_authors['authors']:
                continue
            if initials in git_authors['email_addresses']:
                continue
            git_authors['authors'][initials] = name
            git_authors['email_addresses'][initials] = email

    yaml.safe_dump(git_authors, open(git_author_path, "w+"),
                   default_flow_style=False, explicit_start=False)
