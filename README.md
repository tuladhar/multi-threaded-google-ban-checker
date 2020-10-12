# Multi-threaded Google  Ban Checker

NOTE:
This is not a Google account, domain or advertisements ban checker

**Usage: main.py [options]**

|   Options    |  Description |
| ------------ | ------------ |
|   -d, --debug   |  Print debug information |
|  -n NUM, --threads  NUM |    set maximum number of threads to use (default: 100)  |
|  -%, --show-progress-status |    show realtime progress status and a tabular result at the end  |
|  -R, --realtime |    show results in realtime in csv format  |



# Installation


```shell
$ pip install prettytable requests
$ git clone https://github.com/tuladhar/multi-threaded-google-ban-checker
$ cat PROXIES.txt | python main.py --realtime
```

#### `PROXIES.txt` should be in following format (one proxy per line):
**NOTE:**
- Different accounts at once can be searched

```
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
  ```
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





**NOTE:**
- If ban is detected at any stage no further requests will be made.
- You will be notified once a ban is detected
- Based on progress option used (see `--help` option), console is updated and results are displayed as soon as they're available 
-Please update these files as needed.
-Always update the files before using this
.


## Author
- [Puru Tuladhar](github.com/tuladhar)


## Contributors
- See [Contributors.md](Contributors.md)

