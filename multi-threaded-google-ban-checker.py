#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
# 
# Copyright (c) 2016 Puru
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

__author__ = "Puru Tuladhar <tuladharpuru@gmail.com>"
__github__ = "https://github.com/tuladhar/multi-threaded-google-ban-checker"
__version__ = "Multi-threaded Google Ban Checker v1.0 by {0} ({1})".format(__author__, __github__)

try:
        ####################
        # standard modules #
        ####################
        import sys
        import time
        import math
        import random
        import logging

        from urlparse import urlparse
        from pprint import pprint as pp
        from optparse import OptionParser, OptionGroup
        from collections import deque
        from multiprocessing.pool import ThreadPool
        
        ######################
        # third-part modules #
        ######################
        import requests
        import requests.packages.urllib3
        from prettytable import PrettyTable

        ########################
        # custom helper module #
        ########################
        from helper.useragents import get_random_useragent
        from helper.keywords import get_random_keyword
        import helper.proxy

except ImportError as e:
        print(e)
        print('\ntry installing the missing module using: pip install <module>')
        print("note: helper.useragent, helper.keywords, helper.proxy are custom modules and can't be installed via pip.")
        sys.exit(-1)

else:
        # Disable InsecurePlatformWarning Message
        requests.packages.urllib3.disable_warnings()

def bp():
        """ break point """
        print('<<< BREAK POINT >>>')
        sys.exit(-1)

def check_google_ban(proxy):
        proxy_address = helper.proxy.REGEX.match(proxy).group('proxy')
        result = { 'proxy': proxy_address, 'status_code': 0, 'reason': '', 'google_ban': 'NO', 'redirected_to': '-' }
        proxies = {}
        proxies['http'] = proxies['https'] = 'http://'+proxy

        keyword = get_random_keyword()
        headers = {
                'User-Agent': get_random_useragent(),
                'Accept-Encoding': 'gzip, deflate',
                'Accept': '*/*',
        }

        pages = [0, 10, 20]
        result['pages_ok'] = '0/{}'.format(len(pages))
        for page_no, page in enumerate(pages, 1):
                status_code = 0
                reason = ''
                
                url = 'https://www.google.com/search?q={}'.format(keyword)
                if page != 0:
                        url += '&start=%d' % page

                # logging.debug('url:',url)
                try:
                        resp = requests.get(url, proxies=proxies, headers=headers, timeout=(helper.proxy.TIMEOUT, helper.proxy.TIMEOUT))
                        status_code = resp.status_code
                        reason = resp.reason
                        result['redirected_to'] = urlparse(resp.url).netloc

                except requests.exceptions.ConnectTimeout:
                        reason = 'Proxy Connect Timeout ({}s): Proxy unreachable'.format(helper.proxy.TIMEOUT)

                except requests.exceptions.ReadTimeout:
                        reason = 'Proxy Read Timeout ({}s): Proxy reachable but responding slow (try increasing timeout)'.format(helper.proxy.TIMEOUT)

                except Exception as unknown:
                        reason = 'Unknown Error: {}'.format(unknown)

                finally:
                        result['status_code'] = status_code
                        result['reason'] = reason

                        if status_code == 200:
                                result['pages_ok'] = "{}/{}".format(page_no, len(pages))
                        else:
                                if status_code == 503 or status_code >= 500:
                                        result['google_ban'] = 'BANNED'
                                break

                        # we've reached the end of the page
                        if pages[-1] == page:
                                break
                        # sleep 40 seconds between each page
                        else:
                                logging.debug('sleeping after page {}...'.format(page))
                                time.sleep(40)

        # results.append(result)
        return result

if __name__ == "__main__":
        ################
        # COMMAND-LINE #
        ################
        parser = OptionParser()
        
        parser.add_option("-d", "--debug", action='store_true',
                default=False,dest="debug", help="Print debug information")
        parser.add_option("-n", "--threads", type='int', metavar='NUM',
                default=100, dest="num_threads", help="set maximum number of threads to use (default: %default)")
        # parser.add_option("-f", "--display-format", type='string', metavar='NAME', default='table', dest="display_format", help="set display format. available: csv or table (default: %default)")

        group = OptionGroup(parser, "Select one of the following progress option:")

        group.add_option("-%", "--show-progress-status", action='store_true', default=False, dest="show_progress_status", help="show realtime progress status and a tabular result at the end")
        group.add_option("-R", "--realtime", action='store_true', default=False, dest="realtime", help="show results in realtime in csv format")

        parser.add_option_group(group)

        (opts, args) = parser.parse_args()

        if opts.debug:
                logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)-15s [%(levelname)s] (%(threadName)s) %(message)s')
                logging.debug('debug mode enabled')
        else:
                logging.basicConfig(level=logging.ERROR,
                        format='%(asctime)-15s [%(levelname)s] (%(threadName)s) %(message)s')

        if opts.show_progress_status and opts.realtime:
                parser.error("only one option -% or -R must be selected. try: --help")
                sys.exit(-1)

        if not True in [opts.show_progress_status, opts.realtime]:
                parser.error("atleast one option -% or -R must be selected. try: --help")
                parser.print_usage()
                sys.exit(-1)


        ###########
        # PROXIES #
        ###########
        try:
                all_proxies = [x.strip() for x in sys.stdin.readlines() if x.strip()]
                num_all_proxies = len(all_proxies)

                # first shuffle all proxies
                random.shuffle(all_proxies)
        except KeyboardInterrupt:
                logging.debug('trapped KeyboardInterrupt. exiting...')
                sys.exit(0)
        else:
                # valid proxies
                proxies = filter(helper.proxy.is_valid, all_proxies)
                num_proxies = len(proxies)

                # second shuffle valid proxies
                random.shuffle(proxies)

                logging.debug('total proxies all/valid/invalid: {}/{}/{}'.format(
                        num_all_proxies, num_proxies, num_all_proxies - num_proxies))
        
                if num_proxies == 0:
                        logging.error('no valid proxies available.')
                        sys.exit(-1)

        ##########
        # THREAD #
        ##########
        num_threads = num_proxies if num_proxies < opts.num_threads else opts.num_threads
        logging.debug('max. allowed threads: {}'.format(opts.num_threads))
        logging.debug('starting threads: {} (max or adjusted as per # of proxies)'.format(num_threads))

        # Prepare 'x' number of worker threads
        pool = ThreadPool(num_threads)


        # distrbibute check_google_ban task to all workers
        # and get the result as soon as it's available.
        start_time = time.time()
        finished = 0
        results = []
        banned = 0
        try:
                if opts.realtime:
                        sys.stdout.write('proxy,google-ban,pages-ok,redirected-to,status-code,reason\n')
                        sys.stdout.flush()
                if opts.show_progress_status:
                        sys.stdout.write('\rstarting, please wait....')
                        sys.stdout.flush()
                for result in pool.imap_unordered(check_google_ban, proxies):
                        results.append(result)
                        if result['google_ban'] == 'BANNED':
                                banned += 1
                        finished += 1
                        pct = int(math.floor(finished/float(num_proxies) * 100))
                        remaining = num_proxies - finished
                        
                        seconds = int(math.floor(time.time() - start_time))
                        minutes = seconds / 60
                        hours = minutes / 60

                        human_elapsed = []

                        if hours > 0:
                                human_elapsed.append("{}h".format(hours))
                                minutes = minutes % 60
                        if minutes > 0:
                                human_elapsed.append("{}m".format(minutes))
                                seconds = seconds % 60
                        if seconds:
                                human_elapsed.append("{}s".format(seconds))

                        human_elapsed = " ".join(human_elapsed)

                        if opts.show_progress_status:
                                sys.stdout.write('\r{}% completed, total proxies: {}, finished: {}, remaining: {}, banned: {} (time elapsed: {})'.format(pct, num_proxies, finished, remaining, banned, human_elapsed))
                                sys.stdout.flush()
                        if opts.realtime:
                                sys.stdout.write('{},{},"{}","{}",{},"{}"\n'.format(result['proxy'], result['google_ban'], result['pages_ok'], result['redirected_to'], result['status_code'], result['reason']))
                                sys.stdout.flush()
                else:
                        sys.stdout.write('\n')
                pool.close()
                pool.join()
        except KeyboardInterrupt:
                logging.debug('trapped KeyboardInterrupt. exiting...')
                sys.exit(0)


        if opts.show_progress_status:
                headers = ["Proxy", "Google Ban", "Pages OK", "Redirected To", "Status Code", "Reason"]
                pt = PrettyTable(headers)
                for result in results:
                        pt.add_row([result['proxy'], result['google_ban'], result['pages_ok'], result['redirected_to'], result['status_code'], result['reason']])
                print(pt)