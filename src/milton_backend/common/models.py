from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime
from dateutil import parser


class Series(BaseModel):
    id: Optional[int] = None
    fred_id: str
    realtime_start: Optional[datetime] = None
    realtime_end: Optional[datetime] = None
    title: str
    observation_start: Optional[datetime] = None
    observation_end: Optional[datetime] = None
    frequency: Optional[str] = None
    frequency_short: Optional[str] = None
    units: Optional[str] = None
    units_short: Optional[str] = None
    seasonal_adjustment: Optional[str] = None
    seasonal_adjustment_short: Optional[str] = None
    last_updated: Optional[datetime] = None
    popularity: Optional[int] = None
    group_popularity: Optional[int] = None
    notes: Optional[str] = None

    @field_validator(
        "realtime_start",
        "realtime_end",
        "observation_start",
        "observation_end",
        "last_updated",
        mode="before",
    )
    def parse_datetime(cls, value):
        if isinstance(value, str):
            return parser.parse(value)
        return value

    class Config:
        from_attributes = True


class Keywords(BaseModel):
    keyword_list: List[str]


class SeriesForSearch(BaseModel):
    fred_id: str
    title: str
    units: str
    popularity: int
    relevance_lower_better: Optional[float]

    class Config:
        frozen = True

    def __str__(self):
        return (
            f"SeriesForSearch:\n"
            f"  FRED ID:               {self.fred_id}\n"
            f"  Title:                 {self.title}\n"
            f"  Units:                 {self.units}\n"
            f"  Popularity:            {self.popularity}\n"
            f"  Relevance (Lower is Better): {self.relevance_lower_better}\n"
        )

    def __repr__(self):
        return self.__str__()


class ClassifiedSeries(BaseModel):
    relevant: List[SeriesForSearch]
    notRelevant: List[SeriesForSearch]
