#from django.test import TestCase

# Create your tests here.
import urllib
import urllib2
import socket
import sys
import json

HOST = '127.0.0.1'
PORT = '3000'

debug = True

suffix = ''

list_key = None


def request_resource(url, method='GET', requestData=None):
    if debug:
        print url
        print method
        print requestData

    code = 0
    responseData = ''

    try:
        # create get request using url
        req = urllib2.Request(url, data=requestData)
        if requestData:
            req.add_header('Content-Type', 'application/json')

        req.get_method = lambda: method

        # read content of webpage pointed by url
        res = urllib2.urlopen(req, timeout=30)
        if debug: print url, res.code, res.msg

        code = res.code

        # read content of webpage pointed by url
        responseData = res.read()
    except urllib2.HTTPError, e:
        code = e.code
        responseData = e.read()
        print e
    except urllib2.URLError, e:
        print e
        pass
    except socket.error, e:
        print e
        pass
    return responseData, code


def check(response, code):
    if code == 200:
        return json.loads(response)
    else:
        print "failed"


def check_list(resource, user_id, id_list, key=None):
    obj = check(*request_resource(server + 'user/' + str(user_id) + '/' + resource + '/'))
    if key:
        l = obj[key]
    else:
        l = obj
    id_list2 = [i['id'] for i in l]
    if len(id_list2) != len(id_list): return False
    return len([i for i in id_list if i not in id_list2]) == 0


if __name__ == '__main__':
    if len(sys.argv) > 1:
        HOST = sys.argv[1]
    if len(sys.argv) > 2:
        PORT = sys.argv[2]
    if len(sys.argv) > 3:
        debug = sys.argv[3] == 'y'
    if len(sys.argv) > 4:
        suffix = sys.argv[4]
    if len(sys.argv) > 5:
        list_key = sys.argv[5]

    server = 'http://' + HOST + ':' + PORT + '/cubeapp/'

    user1 = {"name": "a" + suffix, "city": "abad" + suffix}
    user2 = {"name": "b" + suffix, "city": "bad" + suffix}

    cube1 = {"name": "c1" + suffix}

    content1 = {"link": "http://cubeit" + suffix + ".io/"}
    content2 = {"link": "http://www.google" + suffix + ".com/"}

    user1 = check(*request_resource(server + 'user/', 'POST', json.dumps(user1)))
    user2 = check(*request_resource(server + 'user/', 'POST', json.dumps(user2)))
    if debug: print user1, user2

    # TC 1
    # action: create cube1 by user1
    # check: cube1 is in cube list of user1
    cube1 = check(*request_resource(server + 'user/' + str(user1['id']) + '/cube/', 'POST', json.dumps(cube1)))
    if debug: print cube1
    print check_list('cube', user1['id'], [cube1['id']], list_key), ''
    print '\n' * 2

    # TC 2
    # action: share cube1 with user2
    # check: cube1 is in cube list of user2
    share_cube1 = check(*request_resource(server + 'user/' + str(user1['id']) + '/cube/' + str(cube1['id']) + '/share/',
                                          'POST', json.dumps({"user_id": user2['id']})))
    if debug: print share_cube1
    print check_list('cube', user2['id'], [cube1['id']], list_key), ''
    print '\n' * 2

    # TC 3
    # action: create content1 by user1
    # check: content1 is in content list of user1
    content1 = check(*request_resource(server + 'user/' + str(user1['id']) + '/content/', 'POST', json.dumps(content1)))
    if debug: print content1
    print check_list('cube', user1['id'], [cube1['id']], list_key), ''
    print '\n' * 2

    # TC 4
    # action: share content1 with user2
    # check: content2 is in content list of user2
    share_content1 = check(
        *request_resource(server + 'user/' + str(user1['id']) + '/content/' + str(content1['id']) + '/share/',
                          'POST', json.dumps({"user_id": user2['id']})))
    if debug: print share_content1
    print check_list('content', user2['id'], [content1['id']], list_key), ''
    print '\n' * 2

    # TC 5
    # action: create content2 by user1 and add it to cube1
    # check: content1 and content2 is in content list of user1 and user2
    content2 = check(*request_resource(server + 'user/' + str(user1['id']) + '/content/', 'POST', json.dumps(content2)))
    add_content2 = check(
        *request_resource(server + 'user/' + str(user1['id']) + '/cube/' + str(cube1['id']) + '/content/',
                          'POST', json.dumps({"content_id": content2['id']})))
    print check_list('content', user1['id'], [content1['id'], content2['id']], list_key), ''
    print check_list('content', user2['id'], [content1['id'], content2['id']], list_key), ''
    print '\n' * 2

    # TC 6
    # action: delete content2 by user2
    # check: content1 and content2 is in content list of user1 and only content1 is in content list of user2
    delete_content2 = check(*request_resource(
        server + 'user/' + str(user2['id']) + '/cube/' + str(cube1['id']) + '/content/' + str(content2['id']) + '/',
        'DELETE'))
    print check_list('content', user1['id'], [content1['id'], content2['id']], list_key), ''
    print check_list('content', user2['id'], [content1['id']], list_key), ''
    print '\n' * 2

    # TC 7
    # action: delete cube1 by user2
    # check: cube list of user1 and user2 are empty
    delete_cube1 = check(*request_resource(server + 'user/' + str(user2['id']) + '/cube/' + str(cube1['id']) + '/',
                                           'DELETE'))
    print check_list('cube', user1['id'], [], list_key), ''
    print check_list('cube', user2['id'], [], list_key), ''
    print '\n' * 2

    # TC 8
    # action: delete all cubes (already taken in TC 7)
    # check: content1 and content2 is in content list of user1 and only content1 is in content list of user2
    print check_list('content', user1['id'], [content1['id'], content2['id']], list_key), ''
    print check_list('content', user2['id'], [content1['id']], list_key), ''
    print '\n' * 2
