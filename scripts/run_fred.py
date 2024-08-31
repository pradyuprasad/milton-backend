from . import FredAPIClient, Config

def main():
    config = Config()
    fred = FredAPIClient(config.get('FRED_API_KEY'))
    series = fred.get_series_by_tags(tag_names="usa", limit=10)
    print(series)

if __name__ == '__main__':
    main()

