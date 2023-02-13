import unittest


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


class TestRelations(unittest.TestCase):
    def test_used_sbbs(self):
        relations = [
            {
                "SType": "SBB",
                "SName": "SBB1",
                "DType": "SBB",
                "DName": "SBB2",
                "Label": "Label1",
            },
            {
                "SType": "SBB",
                "SName": "SBB1",
                "DType": "SBB",
                "DName": "SBB3",
                "Label": "Label2",
            },
            {
                "SType": "SBB",
                "SName": "SBB2",
                "DType": "SBB",
                "DName": "SBB3",
                "Label": "Label3",
            },
            {
                "SType": "SBB",
                "SName": "SBB4",
                "DType": "SBB",
                "DName": "SBB5",
                "Label": "Label4",
            },
        ]
        rels = Relations(relations)
        self.assertEqual(
            rels.used_sbbs(),
            [
                ("SBB", "SBB1"),
                ("SBB", "SBB2"),
                ("SBB", "SBB3"),
                ("SBB", "SBB4"),
                ("SBB", "SBB5"),
            ],
        )
