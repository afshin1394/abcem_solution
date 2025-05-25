
from pydantic import BaseModel, field_validator


class LoginRequestDto(BaseModel):
     msisdn : str

     @field_validator('msisdn')
     def validate_iranian_mobile_number(cls, v):
          v = v.strip()  # Remove spaces

          # Normalize: replace leading "0" with "+98"
          if v.startswith("+98"):
               v = "09" + v[1:]  # remove '0', keep rest

          elif not v.startswith("09"):
               raise ValueError("Phone number must start with 09")

          print("phone number ",v)

          if len(v) != 11:
               raise ValueError("Phone number of characters incorrect")

          # Remove the +98 and check the next digits
          national_number = v[1:]

          # Match allowed prefixes (Irancell and MCI ranges)
          valid_prefixes = [
               "910", "911", "912", "913", "914", "915", "916", "917", "918", "919",  # MCI Hamrah Aval
               "930", "933", "935", "936", "937", "938", "939",  # Irancell
               "901", "902", "903", "904", "905", "941",  # Irancell TDD / other services
               "990", "991", "992", "993", "994",  # Newer MCI ranges
               "920", "921", "922",  # Rightel
               "998",  # Shatel Mobile
               "999"  # Samantel
          ]
          print("national_number", national_number)
          if not any(national_number.startswith(prefix) for prefix in valid_prefixes):
               raise ValueError("Phone number prefix is not a recognized MCI or Irancell SIM card")

          if not national_number.isdigit():
               raise ValueError("Phone number must only contain digits after +98")

          return v

