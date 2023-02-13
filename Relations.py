import unittest


class Relations:
    def __init__(self, relations: list):
        self.rels = dict()
        for i in relations:
            s = (i["SType"], i["SName"])
            d = (i["DType"], i["DName"])
            self.rels[(s, d)] = {
                    "Source": (s),
                    "Destination": (d),
                    "Label": i["Label"],
                }

    def used_sbbs(self) -> list:
        used = list()
        for s, d in self.rels.keys():
            for i in [s, d]:
                if i not in used:
                    used.append(i)
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
