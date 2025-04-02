import pytest
import requests

import util


def pytest_addoption(parser):
    parser.addoption("--entrypoint", action="store", required=True)
    parser.addoption("--cluster", action="store", required=True)
    parser.addoption("--secret", action="store", required=True)


def pytest_generate_tests(metafunc):
    for opt in ['entrypoint', 'cluster', 'secret']:
        if opt in metafunc.fixturenames:
            metafunc.parametrize(opt, [metafunc.config.getoption(opt)], scope='session')


@pytest.fixture(scope='session')
def call(request):
    options = request.config.option

    def f(method, path, fail=True, data=None):

        response = requests.request(
            method,
            f'http://{options.entrypoint}{path}',
            headers={'Authorization': f'{options.cluster} {options.secret}'},
            json=data,
        )

        if fail:
            response.raise_for_status() 

        try:
            result = response.json()
        except requests.exceptions.JSONDecodeError:
            print("Failed to decode content as JSON:")
            print(response.text)
            if fail:
                raise

        if not result['status']:
            raise ValueError(result.get('error', 'Request failed'))

        print(f'{method} {path}' + (f" -> {result['results']}" if method == 'POST' else ''))

        return result['results']

    return f


@pytest.fixture(scope='module')
def pool(call, cluster):
    pool_uuid = call('POST', '/pool', data={'name': 'poolX', 'cluster_id': cluster, 'no_secret': True})
    yield pool_uuid
    call('DELETE', f'/pool/{pool_uuid}')


@pytest.fixture(scope='module')
def lvol(call, cluster, pool):
    pool_name = call('GET', f'/pool/{pool}')[0]['pool_name']
    lvol_uuid = call('POST', '/lvol', data={
        'name': 'lvolX',
        'size': '1G',
        'pool': pool_name}
    )
    yield lvol_uuid
    call('DELETE', f'/lvol/{lvol_uuid}')
    util.await_deletion(call, f'/lvol/{lvol_uuid}')
