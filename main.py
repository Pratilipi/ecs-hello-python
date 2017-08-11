import bottle
import time

from datetime import datetime
from bottle import Bottle, route, run, request, response

application = Bottle()


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        tt = int((te-ts)*1000)
        ft = "timetaken - {0:4d} ms".format(tt)
        if tt > 0:
            print "timetaken - {}".format(ft)
        return result
    return timed


@application.route('/test', method=['GET'])
@timeit
def test(**kwargs):
    query_dict = request.query.__dict__
    param_dict = query_dict['dict']

    data = param_dict['id'][0]
    wait = int(param_dict['wait'][0])
    tag = param_dict['tag'][0]

    print "got request for {}-{} at {}".format(tag, data, datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    print "waiting for {}-{} for {} msec".format(tag, data, wait)
    sec = wait/1000
    time.sleep(sec)
    print "send response for {}-{} at {}".format(tag, data, datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    result = bottle.HTTPResponse(status=200, body={"message":data})
    return result


if __name__ == '__main__':
    run(application, host='127.0.0.1', port=8080)


