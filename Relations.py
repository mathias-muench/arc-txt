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
