import chdb
import pandas as pd

class ReviewClient:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir

    def __find_business_id_by_name(self, business_name: str) -> str | None:
        query = f"""
        SELECT b.business_id FROM '{self.data_dir}/business.json' as b
        WHERE name = '{business_name.replace("'", "''")}'
        LIMIT 1
        """

        df = chdb.query(query, "Dataframe")
        return df['business_id'].values[0] if not df.empty else None
    
    def get_restaurants(self, city: str, cuisine: str, limit: int | None = None) -> pd.DataFrame:
        query = f"""
        SELECT b.* FROM '{self.data_dir}/business.json' as b
        WHERE b.city = '{city.replace("'", "''")}' AND b.is_open=1 AND b.categories LIKE '%{cuisine.replace("'", "''")}%'
        ORDER BY (3.5 * 50 + b.review_count * b.stars) / (50 + b.review_count) DESC
        {'LIMIT ' + str(limit) if limit is not None else ''}
        """

        return chdb.query(query, "Dataframe")

    def get_reviews(self, business_name: str, limit: int | None = None, sort: str | None = None) -> pd.DataFrame:
        business_id = self.__find_business_id_by_name(business_name)
        if not business_id:
            return pd.DataFrame()
        
        query = f"""
        SELECT r.* FROM '{self.data_dir}/business.json' as b 
        LEFT OUTER JOIN '{self.data_dir}/review.json' as r ON b.business_id = r.business_id
        WHERE b.name = '{business_name.replace("'", "''")}' and r.text IS NOT NULL
        {'ORDER BY ' + sort if sort is not None else ''}
        {'LIMIT ' + str(limit) if limit is not None else ''}"""

        df = chdb.query(query, "Dataframe")
        df['date'] = pd.to_datetime(df['date'], unit='s')
        return df
    
    def get_tips(self, business_name: str, limit: int | None = None, sort: str | None = None) -> pd.DataFrame:
        business_id = self.__find_business_id_by_name(business_name)
        if not business_id:
            return pd.DataFrame()
        
        query = f"""
        SELECT t.* FROM '{self.data_dir}/tip.json' as t
        WHERE t.business_id = '{business_id}' and t.text IS NOT NULL
        {'ORDER BY ' + sort if sort is not None else ''}
        {'LIMIT ' + str(limit) if limit is not None else ''}"""

        df = chdb.query(query, "Dataframe")
        df['date'] = pd.to_datetime(df['date'], unit = 's')
        return df
    
if __name__ == '__main__':
    rc = ReviewClient('./indianapolis_data')
    df= rc.get_restaurants("Indianapolis", "American", limit=5).to_string(index=False)
    # df = rc.get("Yannis Golden Gyros", sort='t.date DESC', limit=5).to_string(index=False)
    print(df)