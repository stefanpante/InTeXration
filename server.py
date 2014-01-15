from bottle import Bottle, request, abort, static_file
import argparse,os, json
from task import InTeXrationTask


class InTeXrationServer:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._app = Bottle()
        self._route()

    def _route(self):
        self._app.route('/', method="GET", callback=self._index)
        self._app.route('/hook/<api_key>', method="POST", callback=self._hook)
        self._app.route('/out/<repo>', method="GET", callback=self._out)

    def start(self):
        self._app.run(host=self._host, port=self._port)

    @staticmethod
    def _hook(api_key):
        def validate(key_to_check):
            path = "api_keys.txt"
            if not os.path.isfile(path):
                return False
            key_file = open(path, "r")
            for line in key_file.readlines():
                key = line.rstrip()
                if key_to_check == key:
                    return True
            return False

        if not validate(api_key):
            abort(401, 'Unauthorized: API key invalid.')
        payload = request.forms.get('payload')
        try:
            data = json.loads(payload)
            url = data['repository']['url']
            name = data['repository']['name']
            commit = data['after']
            task = InTeXrationTask(url, name, commit)
            task.run()
            return 'InTeXration task started.'
        except ValueError:
            abort(400, 'Bad request: Could not decode request body.')


    @staticmethod
    def _index():
        return 'InTeXration is up and running.'

    @staticmethod
    def _out(repo):
        path = os.path.join(os.getcwd(), 'out', repo)
        return static_file('main.pdf', path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', help='hostname', default='localhost')
    parser.add_argument('-port', help='port', default=8000)
    args = parser.parse_args()
    server = InTeXrationServer(host=args.host, port=args.port)
    server.start()
