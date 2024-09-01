from pydantic import BaseModel, field_validator
from typing import Optional
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


    @field_validator('realtime_start', 'realtime_end', 'observation_start', 'observation_end', 'last_updated', mode='before')
    def parse_datetime(cls, value):
        if isinstance(value, str):
            return parser.parse(value)
        return value


    class Config:
        orm_mode = True
