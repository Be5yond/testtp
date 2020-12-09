from testtp import Session, defaultdata


class Client(Session):
    def __init__(self, host):
        self.host = host
        super().__init__()
        self.headers = {"X-Session-header": "default-Header"}
        self.params = {"session-params": "default-params"}

    @defaultdata(
        headers={"X-API-header": "default-API"},
        json={"api-body": "some_api"}
    )
    def some_api(self, **kwargs):
        self.post(self.host+'/post', **kwargs)

    @defaultdata(
        json={"api-another-body": "another_api"}
    )
    def another_api(self, **kwargs):
        self.post(self.host+'/post', **kwargs)

def test_default_data():
    c = Client('http://httpbin.org')
    c.some_api(json={'real': 'hadogen'})
    scm = {
        "headers": {
            "X-Api-Header": "default-API",
            "X-Session-Header": "default-Header"
        },
        "json": {
            "api-body": "some_api",
            "real": "hadogen"
        }
    }
    c.validate(schema=scm)
