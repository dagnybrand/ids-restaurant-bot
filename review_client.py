import chdb
import pandas as pd

class ReviewClient:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir

    def get_restaurants(self, city: str, cuisine: str, limit: int | None = None) -> pd.DataFrame:
        query = f"""
        SELECT b.name, b.stars, b.review_count FROM '{self.data_dir}/business.json' as b
        WHERE b.city = '{city.replace("'", "''")}' AND b.is_open=1 AND b.categories LIKE '%{cuisine.replace("'", "''")}%'
        ORDER BY (3.5 * 50 + b.review_count * b.stars) / (50 + b.review_count) DESC
        {'LIMIT ' + str(limit) if limit is not None else ''}
        """

        return chdb.query(query, "Dataframe")
    
    def get_tips(self, business_name: str, limit: int | None = None) -> pd.DataFrame:
        query = f"""
        SELECT t.text FROM '{self.data_dir}/business.json' as b 
        LEFT OUTER JOIN '{self.data_dir}/tip.json' as t ON b.business_id = t.business_id
        WHERE b.name = '{business_name.replace("'", "''")}'
        {'LIMIT ' + str(limit) if limit is not None else ''}"""

        return chdb.query(query, "Dataframe")

    def get_average_rating(self) -> float:
        query = f"""
        SELECT AVG(b.stars) as average_rating FROM '{self.data_dir}/business.json' as b 
        """
        
        result = chdb.query(query, "Dataframe")
        return result
    
if __name__ == '__main__':
    rc = ReviewClient('./data')
    # rc.filter_cities('Indianapolis')
    # print(rc.get_tips("Yannis Golden Gyros", limit=5)) 
    print(rc.get_restaurants('Indianapolis', 'American', limit=5))
    # print(rc.get_average_rating())