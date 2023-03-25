from last_gas.adapters.api_adapters import GraphqlLoader


class Pelando:
    API_URL = "https://www.pelando.com.br/api/graphql"

    pelando_search_params_pattern = """
        query: "{search}", sortBy: CREATED_AT, limit: {limit}
    """

    pelando_searchoffers_query_pattern = """
        query{{
            public{{
                searchOffers({search_params}){{
                    edges{{
                        {edges}
                    }}
                }}
            }}
        }}
    """

    def search_offers(self, search: str, columns: str, limit: int = 5):
        columns_str = "\n".join(columns)

        search_params = self.pelando_search_params_pattern.format(
            search=search,
            limit=limit,
        )

        query = self.pelando_searchoffers_query_pattern.format(
            search_params=search_params,
            edges=columns_str,
        )

        loader = GraphqlLoader()
        results = loader.query(query, self.API_URL)

        offers = results["data"]["public"]["searchOffers"]["edges"]
        return offers

    @staticmethod
    def format_value(value, kind):
        kind = kind.lower()
        formatted_value = str(value)
        if "fixed" in kind or "price" in kind:
            formatted_value = "R$" + formatted_value
        if "discount" in kind:
            formatted_value = "-" + formatted_value
        if "percentage" in kind:
            formatted_value += "%"
        return formatted_value

    @staticmethod
    def get_value_description(offer):
        for value_kind in ["price", "discountFixed", "discountPercentage"]:
            if offer[value_kind]:
                return Pelando.format_value(offer[value_kind], value_kind)
