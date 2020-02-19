from pyamber.exts import amberdata


def create_server(name=__name__, extensions=None):
    server = Flask(name)

    if not extensions:
        extensions = []

    success = server.config.from_envvar('APPLICATION_SETTINGS', silent=False)
    assert success

    for extension in extensions:
        extension.init_app(server)

    return server


if __name__ == '__main__':
    server = create_server(name="amberdata", extensions=[amberdata])
    print(server)
