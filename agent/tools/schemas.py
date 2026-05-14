from pydantic import BaseModel,computed_field
from pydantic import EmailStr
from datetime import datetime,time,date
from agent.config import settings
from typing import Optional

class ClientInfo(BaseModel):
    name:Optional[str] = None
    email:Optional[EmailStr] = None
    problem:Optional[str] = None
    address:Optional[str] = None
    summary:Optional[str] = None

class WorkerInfo(BaseModel):
    name:Optional[str] = None
    available:Optional[bool] = None
    skill:Optional[str] = None
    email:Optional[EmailStr] = None
    summary:Optional[str] = None

class AppointmentInfo(BaseModel):
    schedule_date:date
    schedule_time:time
    @computed_field
    @property
    def api_time_format(self)->str:
        return f"{self.schedule_date}T{self.schedule_time}+0{settings.TIME_ZONE}:00"


class BookingPayload(BaseModel):
    client:ClientInfo
    worker:WorkerInfo
    appointment:AppointmentInfo

    
class ToolResult(BaseModel):
    success:bool
    data:dict= {}
    error:str = ""

