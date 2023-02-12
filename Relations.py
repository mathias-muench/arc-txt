class Relations:
    def __init__(self, relations: list):
        self.rels = list()
        for i in relations:
            self.rels.append(
                {
                    "Source": (i["SType"], i["SName"]),
                    "Destination": (i["DType"], i["DName"]),
                    "Label": i["Label"],
                }
            )

    def used_sbbs(self) -> list:
        used = list()
        for rel in self.rels:
            for i in ["Source", "Destination"]:
                if rel[i] not in used:
                    used.append(rel[i])
        return used
