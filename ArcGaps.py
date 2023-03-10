import unittest
from Relations import Relations


class ArcGaps:
    def __init__(self, baseline: Relations, target: Relations):
        self.baseline: Relations = baseline
        self.target: Relations = target

    def building_block_gaps(self, kind) -> dict:
        b = { k: v for k, v in {**self.baseline.elements, **self.baseline.aggregates}.items() if k[0] == kind }
        t = { k: v for k, v in {**self.target.elements, **self.target.aggregates}.items() if k[0] == kind }

        m = set()
        c = set()
        e = set()
        n = set()
        for i in b.keys() | t.keys():
            if i in b and i in t:
                if b[i] == t[i]:
                    m.add(i)
                else:
                    c.add(i)
            elif i in b:
                e.add(i)
            else:
                n.add(i)

        return { "Match": sorted(m), "Change": sorted(c), "Eliminated": sorted(e), "New": sorted(n) }

    def new_building_blocks(self) -> set:
        b = self.baseline.elements.keys() | self.baseline.aggregates.keys()
        t = self.target.elements.keys() | self.target.aggregates.keys()
        return t - b

    def changed_building_blocks(self) -> set:
        b = {**self.baseline.elements, **self.baseline.aggregates}
        t = {**self.target.elements, **self.target.aggregates}
        return {
            i for i in t.keys() & b.keys() if b[i] != t[i]
        }

    def new_relations(self) -> set:
        b = self.baseline.aggregations | self.baseline.associations
        t = self.target.aggregations | self.target.associations
        return t - b

    def changed_relations(self) -> set:
        b = self.baseline.aggregations | self.baseline.associations
        t = self.target.aggregations | self.target.associations
        return {
            i for i in t & b if self.baseline.relations[i] != self.target.relations[i]
        }


class TestArcGaps(unittest.TestCase):
    baseline_rels = [
        {
            "Source": "Person:sbb4:0",
            "Destination": "System:banking_system:0",
            "Label": "view_label1a",
        }
    ]
    target_rels = [
        {
            "Source": "Person:sbb4:0",
            "Destination": "System:banking_system:1",
            "Label": "view_label1b",
        },
        {
            "Source": "Person:sbb4:0",
            "Destination": "System:ATM:0",
            "Label": "view_label2",
        },
    ]

    def setUp(self):
        self.maxDiff = None
        baseline = Relations(__class__.baseline_rels)
        target = Relations(__class__.target_rels)
        self.gaps = ArcGaps(baseline, target)

    def test_new_building_blocks(self):
        self.assertSetEqual(
            self.gaps.new_building_blocks(),
            {("System", "ATM")}
        )

    def test_changed_building_blocks(self):
        self.assertSetEqual(
            self.gaps.changed_building_blocks(),
            {("System", "banking_system")}
        )

    def test_new_relations(self):
        self.assertSetEqual(
            self.gaps.new_relations(),
            set(
                [
                    (("Person", "sbb4"), ("System", "ATM")),
                ]
            ),
        )

    def test_changed_relations(self):
        self.assertSetEqual(
            self.gaps.changed_relations(),
            set(
                [
                    (("Person", "sbb4"), ("System", "banking_system")),
                ]
            ),
        )

    def test_building_block_gaps(self):
        self.assertDictEqual(
            self.gaps.building_block_gaps("System"),
            dict()
        )
