import unittest
from jinja2 import Environment, FileSystemLoader
from SolutionBuildingBlocks import SolutionBuildingBlocks
from Relations import Relations
import os


class PlantUmlRenderer:
    def _find_used_sbbs(self) -> list:
        used = list()
        for view in self.relations.rels:
            for i in ["Source", "Destination"]:
                if view[i] not in used:
                    used.append(view[i])
        return used

    def __init__(self, solution_building_blocks, relations: Relations):
        self._solution_building_blocks = solution_building_blocks
        self.relations = relations
        self._used = self._find_used_sbbs()
        self._tags = {("System", "banking_system"): "gap"}
        self._env = Environment(
            loader=FileSystemLoader(os.path.dirname(os.path.abspath(__file__))),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def _render_sbbs(self):
        return self._env.get_template("sbbs.j2").render(
            sbbs=self._solution_building_blocks.sbb_list,
            used=self._used,
            tags=self._tags,
        )

    def _render_views(self):
        return self._env.get_template("views.j2").render(
            views=self.relations.rels,
        )

    def render(self):
        return self._render_sbbs() + self._render_views()


class TestPlantUmlRenderer(unittest.TestCase):
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
            "Type": "Enterprise",
            "Label": "sbb_label2",
            "Description": "sbb2 description",
            "Parent": "sbb1",
        },
        {
            "Name": "banking_system",
            "Type": "System",
            "Label": "sbb_label3",
            "Description": "banking_system description",
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

    views = [
        {
            "SType": "Person",
            "SName": "sbb4",
            "DType": "System",
            "DName": "banking_system",
            "Label": "view_label1",
        }
    ]

    def setUp(self):
        self.maxDiff = None
        sbbs = SolutionBuildingBlocks(__class__.sbb_list)
        rels = Relations(__class__.views)
        self.renderer = PlantUmlRenderer(sbbs, rels)

    def test_render_sbbs(self):
        self.assertEqual(
            self.renderer._render_sbbs(),
            """
Person(Person_sbb4, "sbb_label4", "sbb4 description")

Boundary(Boundary_sbb1, "sbb_label1") {
Enterprise_Boundary(Enterprise_sbb2, "sbb_label2") {
System(System_banking_system, "sbb_label3", "banking_system description")
}
}

""",
        )

    def test_render_views(self):
        self.assertEqual(
            self.renderer._render_views(),
            """Rel(Person_sbb4, System_banking_system, "view_label1")
""",
        )
