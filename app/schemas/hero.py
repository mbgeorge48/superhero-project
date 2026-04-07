from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, computed_field


class Powerstats(BaseModel):
    intelligence: str
    strength: str
    speed: str
    durability: str
    power: str
    combat: str


class Biography(BaseModel):
    full_name: str = Field(alias="full-name")
    alter_egos: str = Field(alias="alter-egos")
    aliases: List[str]
    place_of_birth: str = Field(alias="place-of-birth")
    first_appearance: str = Field(alias="first-appearance")
    publisher: str
    alignment: str

    model_config = ConfigDict(populate_by_name=True)


class Work(BaseModel):
    occupation: str
    base: str


class Connections(BaseModel):
    group_affiliation: str = Field(alias="group-affiliation")
    relatives: str

    model_config = ConfigDict(populate_by_name=True)


class Image(BaseModel):
    url: str


class Appearance(BaseModel):
    gender: str
    race: Optional[str] = "Unknown"
    height: List[str]
    weight: List[str]

    # alias key word helps to handle the API's hyphens
    eye_color: str = Field(alias="eye-color")
    hair_color: str = Field(alias="hair-color")

    model_config = ConfigDict(populate_by_name=True)


class Hero(BaseModel):
    id: str
    name: str
    powerstats: Powerstats
    biography: Biography
    appearance: Appearance
    work: Work
    connections: Connections
    image: Image

    @computed_field
    @property
    def image_url(self) -> str:
        """
        Implements the specific requirement from the PDF:
        https://github.com/akabab/superhero-api/tree/master/.backup/images
        Format: [hero_id]-[hero-name].jpg (lowercase, spaces to hyphens)
        """
        new_domain = "https://raw.githubusercontent.com"
        new_path = "akabab/superhero-api/master/.backup/images/md"
        clean_name = self.name.lower().replace(" ", "-")
        return f"{new_domain}/{new_path}/{self.id}-{clean_name}.jpg"


class HeroListItem(BaseModel):
    """Used for the list view from the scraper service"""
    id: str
    name: str


class HeroDetailEndpointOption(str, Enum):
    POWERSTATS = "powerstats"
    BIOGRAPHY = "biography"
    APPEARANCE = "appearance"
    WORK = "work"
    CONNECTIONS = "connections"
    IMAGE = "image"
