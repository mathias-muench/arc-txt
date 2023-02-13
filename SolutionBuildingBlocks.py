import unittest


class SolutionBuildingBlocks:
    def __init__(self, sbb_list):
        parent_map = {
            "Person": "Enterprise",
            "System": "Enterprise",
            "Enterprise": "Boundary",
            "Boundary": "Boundary",
        }
        self.sbb_list = {}
        for row in sbb_list:
            row["Parent"] = (
                (parent_map[row["Type"]], row["Parent"]) if row["Parent"] else ""
            )
            id = (row["Type"], row["Name"])
            self.sbb_list[id] = row


class TestSolutionBuildingBlocks(unittest.TestCase):
    sbb_list = [
        {
            "Name": "sbb1",
            "Type": "Boundary",
            "Label": "sbb_label1",
            "Description": "sbb1 description",
            "Parent": "",
        },
        {
            "Name": "sbb2",
            "Type": "Boundary",
            "Label": "sbb_label2",
            "Description": "sbb2 description",
            "Parent": "sbb1",
        },
        {
            "Name": "sbb3",
            "Type": "System",
            "Label": "sbb_label3",
            "Description": "sbb3 description",
            "Parent": "sbb2",
        },
        {
            "Name": "sbb4",
            "Type": "Person",
            "Label": "sbb_label4",
            "Description": "sbb4 description",
            "Parent": "",
        },
    ]

    def setUp(self):
        self.solution_building_blocks = SolutionBuildingBlocks(__class__.sbb_list)

    def test_sbb_list(self):
        self.maxDiff = None
        self.assertEqual(
            self.solution_building_blocks.sbb_list,
            {
                ("Boundary", "sbb1"): {
                    "Name": "sbb1",
                    "Type": "Boundary",
                    "Label": "sbb_label1",
                    "Description": "sbb1 description",
                    "Parent": "",
                },
                ("Boundary", "sbb2"): {
                    "Name": "sbb2",
                    "Type": "Boundary",
                    "Label": "sbb_label2",
                    "Description": "sbb2 description",
                    "Parent": ("Boundary", "sbb1"),
                },
                ("System", "sbb3"): {
                    "Name": "sbb3",
                    "Type": "System",
                    "Label": "sbb_label3",
                    "Description": "sbb3 description",
                    "Parent": ("Enterprise", "sbb2"),
                },
                ("Person", "sbb4"): {
                    "Name": "sbb4",
                    "Type": "Person",
                    "Label": "sbb_label4",
                    "Description": "sbb4 description",
                    "Parent": "",
                },
            },
        )
