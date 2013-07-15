#!/usr/bin/python2.7


import argparse
import requests
import sys

parser = argparse.ArgumentParser(description='Create issue in GitHub')

parser.add_argument('--host', help='github host used for issue creation', default='github.plaxo.com')
parser.add_argument('-s', '--subject', required=True, help='subject for the issue')
parser.add_argument('-b', '--body', required=True, help='body for the issue')
parser.add_argument('--repo', help='github repo used for issue creation', required=True)

group = parser.add_argument_group('plain auth')
group.add_argument('-u', '--user', help='github user used for plain auth', required=True)
group.add_argument('-p', '--password', help='github user password used for plain auth', required=True)

parser.add_argument('-v', '--verbose', help='output more detail', action='store_true')
parser.add_argument('-d', '--debug', help='output even more detail', action='store_true')


#parser.add_argument('--oauth', help='oauth key')
#parser.add_argument('--oauth-key', help='oauth key')
#
#group = parser.add_mutually_exclusive_group(required=True)
#group.add_argument('--plain-auth', action='store_true')
#group.add_argument('--oauth', action='store_true')

args = parser.parse_args()

if args.debug:
  args.verbose = True
  print 'ARGS: {0}'.format(args)

issue='''{{
  "title": "{0}",
  "body": "{1}",
  "labels": [
    "splunk"
  ]
}}'''.format(args.subject, args.body)

if args.debug:
  print 'ISSUE: \n' + issue

url = 'http://{0}/api/v3/repos/{1}/{2}/issues'.format(args.host, args.user, args.repo)
if args.debug:
  print 'URL: ' + url

r = requests.post(url, auth=(args.user, args.password), data=issue)

if r.status_code != 201 and r.json.has_key('number'):
  print 'something bad happened posting issue'
  sys.exit(2)

if args.verbose:
  print 'issue {0} created'.format(r.json['number'])
  print r.json['html_url']


