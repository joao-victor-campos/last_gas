import requests

from last_gas.domain.ports import APILoader


class GraphqlLoader(APILoader):
    def query(self, query, url):
        resp = requests.post(url, json={"query": query})
        return resp.json()
