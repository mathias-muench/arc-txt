import unittest


class SolutionBuildingBlocks:
    def __init__(self, sbb_list):
        self.sbb_list = {}
        for row in sbb_list:
            id = row["Type"] + "_" + row["Name"]
            self.sbb_list[id] = row

    def get_sbb_list(self):
        return self.sbb_list

    def get_sbb_tree(self):
        tree = {}
        for x, y in [(k, v["Parent"]) for k, v in self.sbb_list.items()]:
            if y in tree:
                tree[y].append(x)
            else:
                tree[y] = [x]
        return tree

    def _tree_walk(self, tree):
        for key, value in tree.items():
            if isinstance(value, dict):
                print(key + " {")
                self._tree_walk(value)
                print("}")


class TestSolutionBuildingBlocks(unittest.TestCase):
    sbb_list = [
        {
            "Name": "sbb1",
            "Type": "sbb_type1",
            "Label": "sbb_label1",
            "Description": "sbb1 description",
            "Parent": "",
        },
        {
            "Name": "sbb2",
            "Type": "sbb_type2",
            "Label": "sbb_label2",
            "Description": "sbb2 description",
            "Parent": "sbb_type1_sbb1",
        },
        {
            "Name": "sbb3",
            "Type": "sbb_type3",
            "Label": "sbb_label3",
            "Description": "sbb3 description",
            "Parent": "sbb_type2_sbb2",
        },
        {
            "Name": "sbb4",
            "Type": "sbb_type4",
            "Label": "sbb_label4",
            "Description": "sbb4 description",
            "Parent": "",
        },
    ]

    sbb_tree = {
        "": ["sbb_type1_sbb1", "sbb_type4_sbb4"],
        "sbb_type1_sbb1": ["sbb_type2_sbb2"],
        "sbb_type2_sbb2": ["sbb_type3_sbb3"],
    }

    def setUp(self):
        self.solution_building_blocks = SolutionBuildingBlocks(__class__.sbb_list)

    def test_get_sbb_list(self):
        self.assertEqual(
            self.solution_building_blocks.get_sbb_list(),
            {
                "sbb_type1_sbb1": {
                    "Name": "sbb1",
                    "Type": "sbb_type1",
                    "Label": "sbb_label1",
                    "Description": "sbb1 description",
                    "Parent": "",
                },
                "sbb_type2_sbb2": {
                    "Name": "sbb2",
                    "Type": "sbb_type2",
                    "Label": "sbb_label2",
                    "Description": "sbb2 description",
                    "Parent": "sbb_type1_sbb1",
                },
                "sbb_type3_sbb3": {
                    "Name": "sbb3",
                    "Type": "sbb_type3",
                    "Label": "sbb_label3",
                    "Description": "sbb3 description",
                    "Parent": "sbb_type2_sbb2",
                },
                "sbb_type4_sbb4": {
                    "Name": "sbb4",
                    "Type": "sbb_type4",
                    "Label": "sbb_label4",
                    "Description": "sbb4 description",
                    "Parent": "",
                },
            },
        )

    def test_get_sbb_tree(self):
        self.assertEqual(
            self.solution_building_blocks.get_sbb_tree(),
            __class__.sbb_tree,
        )

    def test__tree_walk(self):
        self.assertEqual(
            self.solution_building_blocks._tree_walk(
                tree=self.solution_building_blocks.get_sbb_tree()
            ),
            [
                ("sbb_type1_sbb1", "open"),
                ("sbb_type2_sbb2", "print"),
                ("sbb_type1_sbb1", "close"),
                ("sbb_type3_sbb3", "print"),
            ],
        )
