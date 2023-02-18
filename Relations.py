import unittest


class Relations:
    def __init__(self, relations: list):
        self.rels = dict()
        for i in relations:
            s = tuple(i["Source"].split(":"))
            d = tuple(i["Destination"].split(":"))
            self.rels[(s, d)] = {
                "Source": s,
                "Destination": d,
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
                "Source": "SBB:SBB1:1",
                "Destination": "SBB:SBB2:1",
                "Label": "Label1",
            },
            {
                "Source": "SBB:SBB1:1",
                "Destination": "SBB:SBB3:1",
                "Label": "Label2",
            },
            {
                "Source": "SBB:SBB2:1",
                "Destination": "SBB:SBB3:1",
                "Label": "Label3",
            },
            {
                "Source": "SBB:SBB4:1",
                "Destination": "SBB:SBB5:1",
                "Label": "Label4",
            },
        ]
        rels = Relations(relations)
        self.assertEqual(
            rels.used_sbbs(),
            [
                ("SBB", "SBB1", "1"),
                ("SBB", "SBB2", "1"),
                ("SBB", "SBB3", "1"),
                ("SBB", "SBB4", "1"),
                ("SBB", "SBB5", "1"),
            ],
        )
