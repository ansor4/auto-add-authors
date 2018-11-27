# Auto-add Authors

This script looks through the git log of a repo and adds their initials to your ~/.git-authors file. This can be helpful if you use [git duet](https://github.com/git-duet/git-duet) a lot.

### Tech

The script uses Python 3, [GitPython](https://github.com/gitpython-developers/GitPython), and [PyYAML](https://github.com/yaml/pyyaml).

### Run It

```
~ > cd git-repo
~/git-repo > ./auto_add_authors.py
aw ansor4@xyz.com Anson Wang

found these unique initials
('aw', 'ansor4@xyz.com', 'Anson Wang')

Adding them to .git-authors
~/git-repo > cat ~/.git-authors
authors:
  aw: Anson Wang
email_addresses:
  aw: anson.wang@artsymail.com
~/git-repo >
```

The script will never overwrite existing initials/authors in your ~/.git-authors file, so run it wherever!

### Todos

- Write tests
- Python 2.7 compatibility
- Repo-aware initials
