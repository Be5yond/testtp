from testtp import Session, defaultdata


class Client(Session):
    def __init__(self, host):
        self.host = host
        super().__init__()

    @defaultdata(
        headers={"X-API-header": "default-API"},
        json={"default-body-data": "some_api"}
    )
    def some_api(self, **kwargs):
        self.post(self.host+'/post', **kwargs)


def test_default_data():
    c = Client('http://httpbin.org')
    c.some_api(json={'real': 'hadogen'})

    
