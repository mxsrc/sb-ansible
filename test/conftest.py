import pytest
import requests


def pytest_addoption(parser):
    parser.addoption("--entrypoint", action="store", required=True)
    parser.addoption("--cluster", action="store", required=True)
    parser.addoption("--secret", action="store", required=True)


def pytest_generate_tests(metafunc):
    for opt in ['entrypoint', 'cluster', 'secret']:
        if opt in metafunc.fixturenames:
            metafunc.parametrize(opt, [metafunc.config.getoption(opt)])


@pytest.fixture(scope='session')
def call(request):
    options = request.config.option

    def f(method, path, data=None):

        response = requests.request(
            method,
            f'http://{options.entrypoint}{path}',
            headers={'Authorization': f'{options.cluster} {options.secret}'},
            json=data,
        )
        result = response.json()

        if not result['status']:
            raise ValueError(result.get('error', 'Request failed'))

        print(f'{method} {path}' + (f" -> {result['results']}" if method == 'POST' else ''))

        return result['results']

    return f
