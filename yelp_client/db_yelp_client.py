import clickhouse_connect
import pandas as pd

class DatabaseYelpClient:
    def __init__(self, db_host: str = 'localhost', db_port: int = 8123):
        self.host = db_host
        self.port = db_port

        self.client = clickhouse_connect.get_client(host=self.host, port=self.port)

    def __find_business_id_by_name(self, business_name: str) -> str | None:
        query = """
        SELECT b.business_id FROM business as b
        WHERE name = {business_name:String}
        LIMIT 1
        """

        parameters = {'business_name': business_name.replace("'", "''")}

        df = self.client.query_df(query, parameters=parameters)
        return df['business_id'].values[0] if not df.empty else None
    
    def get_restaurants(self, city: str, cuisine: str, limit: int = 5) -> pd.DataFrame:
        query = """
        SELECT b.* FROM business as b
        WHERE b.city = {city:String} AND b.is_open=1 AND b.categories ILIKE {cuisine:String}
        ORDER BY (3.5 * 50 + b.review_count * b.stars) / (50 + b.review_count) DESC
        LIMIT {limit:UInt8}
        """

        cuisine = cuisine.replace("'", "''")

        parameters = {'city': city.replace("'", "''"), 'cuisine': f"%{cuisine}%", 'limit': limit}

        df =  self.client.query_df(query, parameters=parameters)
        return df

    def get_reviews(self, business_name: str, limit: int = 5) -> pd.DataFrame:
        business_id = self.__find_business_id_by_name(business_name)
        if not business_id:
            return pd.DataFrame()
        
        query = """
        SELECT r.* FROM business as b 
        LEFT OUTER JOIN review as r ON b.business_id = r.business_id
        WHERE b.name = {business_name:String} and r.text IS NOT NULL
        LIMIT {limit:UInt8}"""

        parameters = {'business_name': business_name.replace("'", "''"), 'limit': limit}

        df = self.client.query_df(query, parameters=parameters)
        return df
    
    def get_tips(self, business_name: str, limit: int = 5) -> pd.DataFrame:        
        query = """
        SELECT t.* FROM tip as t
        LEFT OUTER JOIN business as b ON t.business_id = b.business_id
        WHERE b.name = {business_name:String} and t.text IS NOT NULL
        LIMIT {limit:UInt8}"""

        parameters = {'business_name': business_name, 'limit': limit}

        df = self.client.query_df(query, parameters=parameters)
        return df
    
if __name__ == '__main__':
    client = DatabaseYelpClient()
    restaurants = client.get_restaurants('Tampa', 'Burger', 5)
    print(restaurants)