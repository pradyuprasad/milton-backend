from .database import Database
from . import Series

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


    db._cursor.execute(insert_query, (
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
        series.notes
    ))    
        
    db._conn.commit()
