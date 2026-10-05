from dataclasses import dataclass, field
from typing import List, Dict, Any


REQUIRED_FIELDS = [
    "id",
    "name",
    "author",
    "version",
    "description",
    "gameVersion",
    "frameworkVersion",
    "dependencies",
    "optionalDependencies",
    "loadBefore",
    "loadAfter",
    "conflicts",
    "entryPoint",
]


@dataclass
class ModManifest:
    id: str
    name: str
    author: str
    version: str
    description: str
    gameVersion: str
    frameworkVersion: str
    dependencies: List[str] = field(default_factory=list)
    optionalDependencies: List[str] = field(default_factory=list)
    loadBefore: List[str] = field(default_factory=list)
    loadAfter: List[str] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)
    entryPoint: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        missing = [
            field
            for field in REQUIRED_FIELDS
            if field not in data
        ]

        if missing:
            raise ValueError(
                "Missing required manifest fields: "
                + ", ".join(missing)
            )

        return cls(
            id=data["id"],
            name=data["name"],
            author=data["author"],
            version=data["version"],
            description=data["description"],
            gameVersion=data["gameVersion"],
            frameworkVersion=data["frameworkVersion"],
            dependencies=data["dependencies"],
            optionalDependencies=data["optionalDependencies"],
            loadBefore=data["loadBefore"],
            loadAfter=data["loadAfter"],
            conflicts=data["conflicts"],
            entryPoint=data["entryPoint"],
        )