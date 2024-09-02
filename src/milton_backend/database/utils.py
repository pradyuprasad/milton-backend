from typing import Dict, List
from .database import Database
from src.milton_backend.common.models import Series


def insert_series(series: Series):
    """
    Inserts a new series record into the series table.

    Args:
        series (Series): A Pydantic model containing the series data.
    """
    db = Database()
    insert_query = """
    INSERT INTO series (
        fred_id, realtime_start, realtime_end, title, observation_start, observation_end,
        frequency, frequency_short, units, units_short, seasonal_adjustment,
        seasonal_adjustment_short, last_updated, popularity, group_popularity, notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT (fred_id) DO UPDATE
    SET realtime_start = ?, realtime_end = ?, title = ?, observation_start = ?, observation_end = ?,
        frequency = ?, frequency_short = ?, units = ?, units_short = ?, seasonal_adjustment = ?,
        seasonal_adjustment_short = ?, last_updated = ?, popularity = ?, group_popularity = ?, notes = ?
    """

    db._cursor.execute(
        insert_query,
        (
            series.fred_id,
            series.realtime_start,
            series.realtime_end,
            series.title,
            series.observation_start,
            series.observation_end,
            series.frequency,
            series.frequency_short,
            series.units,
            series.units_short,
            series.seasonal_adjustment,
            series.seasonal_adjustment_short,
            series.last_updated,
            series.popularity,
            series.group_popularity,
            series.notes,
            series.realtime_start,
            series.realtime_end,
            series.title,
            series.observation_start,
            series.observation_end,
            series.frequency,
            series.frequency_short,
            series.units,
            series.units_short,
            series.seasonal_adjustment,
            series.seasonal_adjustment_short,
            series.last_updated,
            series.popularity,
            series.group_popularity,
            series.notes,
        ),
    )

    db._conn.commit()


def get_top_series_by_popularity(n: int = 500) -> List[Dict[str, str]]:
    # Get the Database instance
    db = Database()

    # Define the query
    query = """
    SELECT s.fred_id, s.title, s.units, s.frequency, s.seasonal_adjustment, 
           s.last_updated, s.popularity, s.notes
    FROM series s
    ORDER BY s.popularity DESC
    LIMIT ?
    """

    # Execute the query with the parameter 'n'
    db._cursor.execute(query, (n,))
    rows = db._cursor.fetchall()

    # Convert the rows into a list of dictionaries
    series_list = [
        {
            "fred_id": row[0],
            "title": row[1],
            "units": row[2],
            "frequency": row[3],
            "seasonal_adjustment": row[4],
            "last_updated": row[5],
            "popularity": row[6],
            "notes": row[7],
        }
        for row in rows
    ]

    return series_list
