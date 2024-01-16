# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2


class AnimeScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'sypnosis':
                value = adapter.get(field_name)
                if isinstance(value, list):
                    adapter[field_name] = ' '.join(value).strip()
                else:
                    adapter[field_name] = value.strip()


        # Format Type and Genre to lowercase
        lower_keys = ['type', 'genre']
        for lower_key in lower_keys:
            value = adapter.get(lower_key)
            adapter[lower_key] = value.lower()

        """
        # Price convert to float
        price_keys = ['price', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('₱', '')
            adapter[price_key] = float(value)
        """

        """
        # Extract number from string
        # Assume 'availability' has a value like "In stock (18 available)"
        availability_str = adapter.get('availability')
        split_str_arr = availability_str.split('(') #It returns ['In stock ', '18 available)']
        if len(split_str_arr) < 2:
            adapter['availability'] = 0
        else:    
            availability_arr = split_str_arr[1].split(' ') #It returns ['18', 'available)']
            adapter['availability'] = int(availability_arr[0])
        """

        return item
    
class SaveToPostgreSQLPipeline:
    def __init__(self):
        # Connect to PostgreSQL
        self.conn = psycopg2.connect(
            host='localhost',
            user='postgres',  # Replace with your PostgreSQL username
            password='password121012',  # Replace with your PostgreSQL password
            database='scrapy_db'
        )

        # Create a cursor, used to execute commands
        self.cur = self.conn.cursor()

        # Create 'books' table if it doesn't exist
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS anime(
            id SERIAL PRIMARY KEY,
            url VARCHAR(255),
            title TEXT,
            poster VARCHAR(255),
            sypnosis TEXT,
            type VARCHAR(255),
            genre VARCHAR(255),
            duration VARCHAR(255),
            episodes INTEGER
        )
        """)

    def process_item(self, item, spider):
        # Define insert statement
        self.cur.execute("""
            INSERT INTO anime (
                url, title, poster, sypnosis, type,
                genre, duration, episodes
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s
            )""",
            (
                item["url"],
                item["title"],
                item["poster"],
                item["sypnosis"],
                item["type"],
                item["genre"],
                item["duration"],
                item["episodes"],
            )
        )

        # Execute insert of data into the database
        self.conn.commit()
        return item

    def close_spider(self, spider):
        # Close cursor & connection to the database
        self.cur.close()
        self.conn.close()