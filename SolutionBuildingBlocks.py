import unittest


class SolutionBuildingBlocks:
    def __init__(self, sbb_list):
        self.sbb_list = {}
        for row in sbb_list:
            if row["Type"] == "System":
                row["Parent"] = "Enterprise_" + row["Parent"]
            id = row["Type"] + "_" + row["Name"]
            self.sbb_list[id] = row

class TestSolutionBuildingBlocks(unittest.TestCase):
    sbb_list = [
        {
            "Name": "sbb1",
            "Type": "Enterprise_Boundary",
            "Label": "sbb_label1",
            "Description": "sbb1 description",
            "Parent": "",
        },
        {
            "Name": "sbb2",
            "Type": "Boundary",
            "Label": "sbb_label2",
            "Description": "sbb2 description",
            "Parent": "Enterprise_Boundary_sbb1",
        },
        {
            "Name": "sbb3",
            "Type": "System",
            "Label": "sbb_label3",
            "Description": "sbb3 description",
            "Parent": "Boundary_sbb2",
        },
        {
            "Name": "sbb4",
            "Type": "Person",
            "Label": "sbb_label4",
            "Description": "sbb4 description",
            "Parent": "",
        },
    ]

    sbb_tree = {
        "": ["Enterprise_Boundary_sbb1", "Person_sbb4"],
        "Enterprise_Boundary_sbb1": ["Boundary_sbb2"],
        "Boundary_sbb2": ["System_sbb3"],
    }

    def setUp(self):
        self.solution_building_blocks = SolutionBuildingBlocks(__class__.sbb_list)

    def test_sbb_list(self):
        self.assertEqual(
            self.solution_building_blocks.sbb_list,
            {
                "Enterprise_Boundary_sbb1": {
                    "Name": "sbb1",
                    "Type": "Enterprise_Boundary",
                    "Label": "sbb_label1",
                    "Description": "sbb1 description",
                    "Parent": "",
                },
                "Boundary_sbb2": {
                    "Name": "sbb2",
                    "Type": "Boundary",
                    "Label": "sbb_label2",
                    "Description": "sbb2 description",
                    "Parent": "Enterprise_Boundary_sbb1",
                },
                "System_sbb3": {
                    "Name": "sbb3",
                    "Type": "System",
                    "Label": "sbb_label3",
                    "Description": "sbb3 description",
                    "Parent": "Boundary_sbb2",
                },
                "Person_sbb4": {
                    "Name": "sbb4",
                    "Type": "Person",
                    "Label": "sbb_label4",
                    "Description": "sbb4 description",
                    "Parent": "",
                },
            },
        )
