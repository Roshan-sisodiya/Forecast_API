from pydantic import BaseModel



class ForecastRequestDTO(BaseModel):
   Latitude: float
   Longitude: float

class ForecastResponseDTO(BaseModel):
   ReturnCode: int
   ReturnCodeDescription: str