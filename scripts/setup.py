from . import FredAPIClient, Config, initialize_database, Series, insert_series

def main():
    config = Config()
    fred = FredAPIClient(config.get('FRED_API_KEY'))
    initialize_database()

    top_20_tags = fred.get_tags(limit=20, order_by='popularity', sort_order='desc')

    for i, value in enumerate(top_20_tags['tags']):
        print(i, value)
        series_by_tag = fred.get_series_by_tags(tag_names=value['name'], limit=50, order_by='popularity', sort_order='desc')

        for j, series_data in enumerate(series_by_tag['seriess']):
            print(j, series_data)
            series_data['fred_id'] = series_data.pop('id')


            # Map the dictionary to the Series model
            series = Series(**series_data)

            # Insert the series into the database
            insert_series(series)

if __name__ == '__main__':
    main()
