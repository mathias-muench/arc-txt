import unittest


class Relations:
    def __init__(self, model: list):
        m = dict()
        for i in model:
            row = i.copy()
            row["Source"] = tuple(i["Source"].split(":"))
            row["Destination"] = tuple(i["Destination"].split(":"))
            m[(row["Source"], row["Destination"])] = row
        self.relations: dict = {(k[0][0:-1], k[1][0:-1]): v for k, v in m.items()}
        self.associations: set = {
            k for k, v in self.relations.items() if v["Label"] != "__Aggregation__"
        }
        self.aggregations: set = {
            k for k, v in self.relations.items() if v["Label"] == "__Aggregation__"
        }
        self.elements: dict = {
            k: v
            for k, v in self.used_sbbs(m).items()
            if k not in {j[1] for j in self.aggregations}
        }
        self.aggregates: dict = {
            k: v
            for k, v in self.used_sbbs(m).items()
            if k not in {j[1] for j in self.associations}
        }

    def render(self, renderer):
        return renderer.render(self)

    def system_organization_matrix(self) -> dict:
        owns = {
            (i[1], i[0]): "owns"
            for i in self.aggregations
            if i[0][0] == "System" and i[1][0] == "Enterprise"
        }
        uses = {
            ({s: e for e, s in owns}[i[0]], i[1]): "uses"
            for i in self.associations
            if i[0][0] == "System" and i[1][0] == "System"
        }
        return {**uses, **owns}

    @staticmethod
    def used_sbbs(model: dict) -> dict:
        coll: dict = dict()
        for s, d in model.keys():
            for t, n, v in [s, d]:
                if (t, n) not in coll:
                    coll[(t, n)] = list()
                coll[(t, n)].append(int(v))
        used = dict()
        for t, n in coll.keys():
            i = (t, n, str(max(coll[(t, n)])))
            if (i[0:-1]) not in used:
                used[i[0:-1]] = i
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
        self.assertDictEqual(
            rels.elements,
            {
                ("SBB", "SBB1"): ("SBB", "SBB1", "1"),
                ("SBB", "SBB2"): ("SBB", "SBB2", "1"),
                ("SBB", "SBB3"): ("SBB", "SBB3", "2"),
                ("SBB", "SBB4"): ("SBB", "SBB4", "1"),
                ("SBB", "SBB5"): ("SBB", "SBB5", "1"),
            },
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
        self.assertSetEqual(rels.aggregations, {(("SBB", "SBB1"), ("SBB", "SBB2"))})

    def test_system_organization_matrix(self):
        relations = [
            {
                "Source": "System:SBB1:1",
                "Destination": "Enterprise:SBB2:1",
                "Label": "__Aggregation__",
            },
            {
                "Source": "System:SBB1:1",
                "Destination": "System:SBB3:1",
                "Label": "Label2",
            },
            {
                "Source": "System:SBB3:1",
                "Destination": "Enterprise:SBB4:1",
                "Label": "__Aggregation__",
            },
            {
                "Source": "System:SBB1:1",
                "Destination": "Container:SBB5:1",
                "Label": "Label2",
            },
            {
                "Source": "Container:SBB2:2",
                "Destination": "System:SBB1:1",
                "Label": "__Aggregation__",
            },
        ]
        rels = Relations(relations)
        self.assertDictEqual(
            rels.system_organization_matrix(),
            {
                (("Enterprise", "SBB2"), ("System", "SBB1")): "owns",
                (("Enterprise", "SBB4"), ("System", "SBB3")): "owns",
                (("Enterprise", "SBB2"), ("System", "SBB3")): "uses",
            },
        )
