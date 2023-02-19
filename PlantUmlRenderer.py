import unittest
from jinja2 import Environment, FileSystemLoader
from SolutionBuildingBlocks import SolutionBuildingBlocks
from Relations import Relations
from ArcGaps import ArcGaps
import os
from semantic_version import Version, SimpleSpec


class PlantUmlRenderer:
    def __init__(
        self,
        diagram,
        solution_building_blocks,
        relations: Relations,
        gaps: ArcGaps = None,
    ):
        self.diagram = diagram
        self._solution_building_blocks = solution_building_blocks
        self._relations = relations
        self.gaps = gaps
        self._env = Environment(
            loader=FileSystemLoader(os.path.dirname(os.path.abspath(__file__))),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self._env.filters["get_sbb"] = self.get_sbb

    @staticmethod
    def get_sbb(value, id) -> tuple:
        versions = [
            Version(i[2]) for i in value if i[0] == id[0] and i[1] == id[1]
        ]
        v = SimpleSpec(id[2]).select(versions)
        return value[(id[0], id[1], str(v))] if v else None

    def _render_sbbs(self):
        _tags = dict()
        if self.gaps:
            for i in self.gaps.sbb_gaps():
                _tags[i] = "gap"
        return self._env.get_template("sbbs.j2").render(
            diagram=self.diagram,
            sbbs=self._solution_building_blocks.sbb_list,
            used=self._relations.used_sbbs(),
            tags=_tags,
        )

    def _render_views(self):
        _tags = dict()
        if self.gaps:
            for i in self.gaps.rel_gaps():
                _tags[i] = "gap"
        return self._env.get_template("views.j2").render(
            diagram=self.diagram,
            views=self._relations.rels,
            tags=_tags,
        )

    def render_iuml(self):
        return self._render_sbbs() + self._render_views()

    def render_puml(self, wrapper="wrapper.j2"):
        return self._env.get_template(wrapper).render(text=self.render_iuml())


class TestPlantUmlRenderer(unittest.TestCase):
    sbb_list = [
        {
            "Name": "sbb1",
            "Type": "Boundary",
            "Version": "1.0.0",
            "Label": "sbb_label1",
            "Description": "sbb1 description",
            "Parent": "",
        },
        {
            "Name": "sbb2",
            "Type": "Enterprise",
            "Version": "1.0.0",
            "Label": "sbb_label2",
            "Description": "sbb2 description",
            "Parent": "sbb1:1.0.0",
        },
        {
            "Name": "sbb3",
            "Type": "System",
            "Version": "1.0.0",
            "Label": "sbb_label3",
            "Description": "sbb3 description",
            "Parent": "sbb2:1.0.0",
        },
        {
            "Name": "sbb3",
            "Type": "System",
            "Version": "2.0.0",
            "Label": "sbb_label3",
            "Description": "sbb3 description",
            "Parent": "sbb2:1.0.0",
        },
        {
            "Name": "sbb4",
            "Type": "Person",
            "Version": "1.0.0",
            "Label": "sbb_label4",
            "Description": "sbb4 description",
            "Parent": "",
        },
    ]

    views = [
        {
            "Source": "Person:sbb4:>0",
            "Destination": "System:sbb3:>1",
            "Label": "view_label1",
        }
    ]

    def setUp(self):
        self.maxDiff = None
        sbbs = SolutionBuildingBlocks(__class__.sbb_list)
        rels = Relations(__class__.views)
        self.renderer = PlantUmlRenderer("landscape", sbbs, rels)

    def test_render_sbbs(self):
        self.assertEqual(
            self.renderer._render_sbbs(),
            """
Person(Person_sbb4, "sbb_label4", $descr="sbb4 description", $tags="")

Boundary(Boundary_sbb1, "sbb_label1") {
Enterprise_Boundary(Enterprise_sbb2, "sbb_label2") {
System(System_sbb3, "sbb_label3", $descr="sbb3 description", $tags="")
}
}

""",
        )

    def test_render_views(self):
        self.assertEqual(
            self.renderer._render_views(),
            """Rel(Person_sbb4, System_sbb3, "view_label1", $tags="")
""",
        )
