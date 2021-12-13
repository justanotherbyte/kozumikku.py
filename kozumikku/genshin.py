from typing import Optional


class CharacterImage:
    def __init__(self, data: dict):
        self.url = data["url"]
        self.height = int(data["height"])
        self.width = int(data["width"])

    def __repr__(self) -> str:
        # this basically shows the whole object
        fmt = "<CharacterImage url={0.url!r} height={0.height!r} width={0.width!r}>"
        return fmt.format(self)

class CharacterInfo:
    # "star_rank": "5",
    # "alternative_names": "None",
    # "title": "Unknown",
    # "vision": "Geo / Earth",
    # "weapon": "Claymore",
    # "constellation": "",
    # "gender": "♂ male",
    # "birthday": "Unknown",
    # "body_type": "Adult",
    # "voice_actor_jp": "Nishikawa Takanori",
    # "voice_actor_ch": "Unannounced",
    # "voice_actor_eng": "Max Mittelman"
    def __init__(self, data: dict):
        self.star_rank: str = data["star_rank"]
        self.alternative_names: str = data["alternative_names"]
        self.title: str = data["title"]
        self.vision: str = data["vision"]
        self.weapon: str = data["weapon"]
        self.constellation: str = data["constellation"]
        self.gender: str = data["gender"]
        self.birthday: str = data["birthday"]
        self.body_type: str = data["body_type"]
        self.voice_actor_jp: str = data["voice_actor_jp"]
        self.voice_actor_ch: str = data["voice_actor_ch"]
        self.voice_actor_eng: str = data["voice_actor_eng"]

        self.origin: Optional[str] = data.get("origin")

    def __repr__(self) -> str:
        # just show some important stuff
        # that might be useful while debugging
        fmt = "<CharacterInfo star_rank={0.star_rank!r} title={0.title!r} {0.vision!r} {0.weapon!r}>"
        return fmt.format(self)


class GenshinCharacter:
    def __init__(self, data: dict):
        self.name: str = data["name"]
        self.description: str = data["description"]
        self.game_description: str = data["game_description"]
        
        info = data["character_info"]
        image = data["character_image"]
        self.info = CharacterInfo(info)
        self.image = CharacterImage(image)

    def __repr__(self) -> str:
        fmt = "<GenshinCharacter name={0.name!r}> info={0.info!r}>"
        return fmt.format(self)
