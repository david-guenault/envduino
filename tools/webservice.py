from bottle import route, run, response
import json
import os


@route('/get/<name>',method="GET")
def wget(name=''):
    response.content_type = 'application/json'
    return json.dumps({ "success" : False, "paths" : [], "error" : "not implemented yet" })

@route('/put/<name>',method="GET")
def wput(name=''):
    response.content_type = 'application/json'
    return json.dumps({ "success" : False, "paths" : [], "error" : "not implemented yet" })

@route('/delete/<name>',method="GET")
def wdelete(name=''):
    response.content_type = 'application/json'
    return json.dumps({ "success" : False, "paths" : [], "error" : "not implemented yet" })

if __name__ == "__main__":
    run(host='localhost', port=8181)
