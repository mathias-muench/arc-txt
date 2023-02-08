import unittest


class SolutionBuildingBlocks:
    def __init__(self, sbb_list):
        self.sbb_list = sbb_list

    def get_sbb_list(self):
        return self.sbb_list


class TestSolutionBuildingBlocks(unittest.TestCase):
    sbb_list = [
        {
            "Name": "sbb1",
            "Type": "sbb_type1",
            "Label": "sbb_label1",
            "Description": "sbb1 description",
        },
        {
            "Name": "sbb2",
            "Type": "sbb_type2",
            "Label": "sbb_label2",
            "Description": "sbb2 description",
        },
    ]

    def setUp(self):
        self.solution_building_blocks = SolutionBuildingBlocks(
            __class__.sbb_list
        )

    def test_get_sbb_list(self):
        self.assertEqual(
            self.solution_building_blocks.get_sbb_list(),
            self.sbb_list,
        )
