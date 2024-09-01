from . import get_top_series_by_popularity, ChromaDBClient

def populate_chroma_db():
    series_list = get_top_series_by_popularity(n=1000)
    chroma_connection = ChromaDBClient()
    series_collection = chroma_connection.get_or_create_collection("fred-economic-series")
    if series_collection.count() != 0 :
        print("Chroma databases already populated.")
        return

    
    series_documents = []
    series_metadatas = []
    series_ids = []
    
    
    for series in series_list:
        # Series collection
        document = f"{series['title']} {series['units']} {series['frequency']} {series['seasonal_adjustment']} {series['notes']}"
        document = document.lower()  # Normalize to lowercase
        series_documents.append(document)
        
        series_metadatas.append({
            'fred_id': series['fred_id'],
            'title': series['title'],
            'units': series['units'],
            'frequency': series['frequency'],
            'seasonal_adjustment': series['seasonal_adjustment'],
            'last_updated': series['last_updated'],
            'popularity': series['popularity']
        })
        series_ids.append(series['fred_id'])
        
        # Collect unique tags
        '''
        tags = series['tags'].split(', ')
        tags_set.update(tags)
        '''
    
    # Add series to Chroma in batches
    batch_size = 10
    for i in range(0, len(series_documents), batch_size):
        for k in series_metadatas[i:i+batch_size]:
            print(i, "\n\n")
            print(k['title'])
        series_collection.add(
            documents=series_documents[i:i+batch_size],
            metadatas=series_metadatas[i:i+batch_size],
            ids=series_ids[i:i+batch_size]
        )
    print("all series inserted")
