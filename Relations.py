import unittest


class Relations:
    def __init__(self, relations: list):
        self.rels = dict()
        for i in relations:
            row = i.copy()
            row["Source"] = tuple(i["Source"].split(":"))
            row["Destination"] = tuple(i["Destination"].split(":"))
            self.rels[(row["Source"], row["Destination"])] = row
        self.aggregations = self._aggregations()

    def _aggregations(self) -> set:
        return {
            (i["Source"], i["Destination"])
            for i in self.rels.values()
            if i["Label"] == "__Aggregation__"
        }

    def used_sbbs(self) -> list:
        coll = dict()
        for s, d in self.rels.keys():
            for t, n, v in [s, d]:
                if (t, n) not in coll:
                    coll[(t, n)] = list()
                coll[(t, n)].append(int(v))
        used = list()
        for t, n in coll.keys():
            i = (t, n, str(max(coll[(t, n)])))
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
                "Destination": "SBB:SBB3:2",
                "Label": "Label3",
            },
            {
                "Source": "SBB:SBB4:1",
                "Destination": "SBB:SBB5:1",
                "Label": "Label4",
            },
        ]
        rels = Relations(relations)
        self.assertListEqual(
            rels.used_sbbs(),
            [
                ("SBB", "SBB1", "1"),
                ("SBB", "SBB2", "1"),
                ("SBB", "SBB3", "2"),
                ("SBB", "SBB4", "1"),
                ("SBB", "SBB5", "1"),
            ],
        )

    def test_aggregations(self):
        relations = [
            {
                "Source": "SBB:SBB1:1",
                "Destination": "SBB:SBB2:1",
                "Label": "__Aggregation__",
            },
            {
                "Source": "SBB:SBB1:1",
                "Destination": "SBB:SBB3:1",
                "Label": "Label2",
            },
        ]
        rels = Relations(relations)
        self.assertSetEqual(
            rels.aggregations, {(("SBB", "SBB1", "1"), ("SBB", "SBB2", "1"))}
        )
