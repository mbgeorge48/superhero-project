from typing import List, Optional

from pydantic import BaseModel, Field


class Appearance(BaseModel):
    gender: str
    race: Optional[str] = "Unknown"
    height: List[str]
    weight: List[str]

    # alias key word helps to handle the API's hyphens
    eye_color: str = Field(alias="eye-color")
    hair_color: str = Field(alias="hair-color")

    class ConfigDict:
        # Allows you to use 'eye_color' or 'eye-color' when creating the object
        populate_by_name = True


class Hero(BaseModel):
    id: str
    name: str
    appearance: Appearance
    # Expand as neccessary,
    # We could add support for powerstats and biography for example

    image_url: str


class HeroListItem(BaseModel):
    """Used for the list view from the scraper service"""

    id: str
    name: str
