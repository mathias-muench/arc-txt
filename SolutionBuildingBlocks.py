import unittest


class SolutionBuildingBlocks:
    def __init__(self, sbb_list):
        self.sbb_list = {}
        for i in sbb_list:
            row = {}
            for j in i.keys():
                row[j] = i[j]
            id = (i["Type"], i["Name"], i["Version"])
            self.sbb_list[id] = row


class TestSolutionBuildingBlocks(unittest.TestCase):
    sbb_list = [
        {
            "Name": "sbb1",
            "Type": "Boundary",
            "Version": "1",
            "Label": "sbb_label1",
            "Description": "sbb1 description",
        },
        {
            "Name": "sbb2",
            "Type": "Enterprise",
            "Version": "1",
            "Label": "sbb_label2",
            "Description": "sbb2 description",
        },
        {
            "Name": "sbb3",
            "Type": "System",
            "Version": "1",
            "Label": "sbb_label3",
            "Description": "sbb3 description",
        },
        {
            "Name": "sbb4",
            "Type": "Person",
            "Version": "1",
            "Label": "sbb_label4",
            "Description": "sbb4 description",
        },
    ]

    def setUp(self):
        self.solution_building_blocks = SolutionBuildingBlocks(__class__.sbb_list)

    def test_sbb_list(self):
        self.maxDiff = None
        self.assertEqual(
            self.solution_building_blocks.sbb_list,
            {
                ("Boundary", "sbb1", "1"): {
                    "Name": "sbb1",
                    "Type": "Boundary",
                    "Version": "1",
                    "Label": "sbb_label1",
                    "Description": "sbb1 description",
                },
                ("Enterprise", "sbb2", "1"): {
                    "Name": "sbb2",
                    "Type": "Enterprise",
                    "Version": "1",
                    "Label": "sbb_label2",
                    "Description": "sbb2 description",
                },
                ("System", "sbb3", "1"): {
                    "Name": "sbb3",
                    "Type": "System",
                    "Version": "1",
                    "Label": "sbb_label3",
                    "Description": "sbb3 description",
                },
                ("Person", "sbb4", "1"): {
                    "Name": "sbb4",
                    "Type": "Person",
                    "Version": "1",
                    "Label": "sbb_label4",
                    "Description": "sbb4 description",
                },
            },
        )
