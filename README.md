# Multi-threaded Google  Ban Checker


[![Contributors](https://img.shields.io/github/contributors/tuladhar/multi-threaded-google-ban-checker)](https://github.com/tuladhar/multi-threaded-google-ban-checker/blob/main/Contributors.md)
[![Issues](https://img.shields.io/github/issues/tuladhar/multi-threaded-google-ban-checker)](https://github.com/tuladhar/multi-threaded-google-ban-checker/issues)
[![Open Pull Requests](https://img.shields.io/github/issues-pr-raw/tuladhar/multi-threaded-google-ban-checker)](https://github.com/tuladhar/multi-threaded-google-ban-checker/pulls)
[![Last Commit](https://img.shields.io/github/last-commit/tuladhar/multi-threaded-google-ban-checker)](https://github.com/tuladhar/multi-threaded-google-ban-checker/commits/main)
[![Stars](https://img.shields.io/github/stars/tuladhar/multi-threaded-google-ban-checker)](https://github.com/tuladhar/multi-threaded-google-ban-checker/stargazers)
[![Forks](https://img.shields.io/github/forks/tuladhar/multi-threaded-google-ban-checker)](https://github.com/tuladhar/multi-threaded-google-ban-checker/network/members)
[![Watchers](https://img.shields.io/github/watchers/tuladhar/multi-threaded-google-ban-checker)](https://github.com/tuladhar/multi-threaded-google-ban-checker/watchers)
[![License](https://img.shields.io/github/license/tuladhar/multi-threaded-google-ban-checker)](https://github.com/tuladhar/multi-threaded-google-ban-checker/blob/main/LICENSE)

NOTE:
This is not a Google account, domain or advertisements ban checker

## Table of Contents
* [Installation](#Installation)
* [How it works](#How it works?)
* [Contributing](#Contributing)
* [Author](#Author)
* [Contributors](#Contributors)


**Usage: main.py [options]**

|   Options    |  Description |
| ------------ | ------------ |
|   -d, --debug   |  Print debug information |
|  -n NUM, --threads  NUM |    set maximum number of threads to use (default: 100)  |
|  -%, --show-progress-status |    show realtime progress status and a tabular result at the end  |
|  -R, --realtime |    show realtime results in csv format  |



# Installation


```shell
$ pip install prettytable requests
$ git clone https://github.com/tuladhar/multi-threaded-google-ban-checker
$ cat PROXIES.txt | python main.py --realtime
```

#### `PROXIES.txt` should be in following format (one proxy per line):
**NOTE:**
- Only one unique account can be searched at a time

```markdown
username:password@proxy1:port
username:password@proxy2:port
...
```

#### Google Keywords and User Agents used by the script:
- `helper/keywords.txt`
- `helper/useragents.txt`

**NOTE:**
- Please make sure your username and password exist here before using this
- Please update these files as needed.
- Always update the files before using this

How it works?
-------------

1. List of proxies (one per line) are read from standard input in following format and randomize internally by the script:
  ```markdown
  username:password@proxy1:port
  username:password@proxy2:port
  ...
  ```

2. `X` number of worker threads are created (see `--threads` option)

3. Proxies are distributed among pool of available threads and each thread does the following:

	1. Each proxy makes 3 requests, retrieving default 10 page per request.
	2. First page is requested as normal
	3. Google ban is checked (50x), and if not banned then thread waits 40 seconds before using the proxy for another request
	4. After 40 seconds wait, second page is requested by adding `&start=10` to query string
	5. Repeats step iii.
	6. After 40 seconds wait, third page is requested by adding `&start=20` to query string
	7. Finally thread returns with result.


## Contributing: Getting Started 
* Fork this repository (Click the Form button, top right of this page)
* Clone your fork down to your local machine
```markdown
git clone https://github.com/your-username/multi-threaded-google-ban-checker.git
```
* Comment to the Issue you want to work on - so I can assign you to it OR create a new Issue from a LeetCode Problem that is not implemented yet
* Create a branch for a new feature
```markdown
git checkout -b feature/branch-name
```
* Or if its a bugfix to a file
```markdown
git checkout -b bugfix/branch-name
```
* Make your changes (choose from the Tasks above!)
* Commit and Push
```markdown
git add .
git commit -m 'commit message'
git push origin branch-name
```
* Create a New Pull Request from your forked repository ( Click the 'New Pull Request' Button located at the top of your repo)
* Wait for your PR review and merge approval!
* __Star this repository__ if you had fun!


**NOTE:**
- If ban is detected at any stage no further requests will be made.
- You will be notified once a ban is detected
- Based on progress option used (see `--help` option), console is updated and results are displayed as soon as they're available 
- Please update these files as needed.
- Always update the files before using this
.


## Author
- [Puru Tuladhar](github.com/tuladhar)


## Contributors
- See [Contributors.md](Contributors.md)

