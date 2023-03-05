import unittest
from jinja2 import Environment, FileSystemLoader
from SolutionBuildingBlocks import SolutionBuildingBlocks
from Relations import Relations
from ArcGaps import ArcGaps
import os


class Renderer:
    def render(self, rels):
        pass


class MatrixRenderer(Renderer):
    def __init__(self, solution_building_blocks):
        self._solution_building_blocks = solution_building_blocks

    def render(self, rels: Relations):
        e = [
                self._solution_building_blocks.sbb_list[i]["Label"]
                for i in rels.elements.values()
                if self._solution_building_blocks.sbb_list[i]["Type"] == "System"
            ]
        e.sort()
        for i in e:
            print(i)


class PlantUmlRenderer(Renderer):
    def __init__(
        self,
        diagram,
        solution_building_blocks,
        gaps: ArcGaps = None,
        wrapper="wrapper.j2",
    ):
        self.diagram = diagram
        self._solution_building_blocks = solution_building_blocks
        self.gaps = gaps
        self.wrapper = wrapper
        self._env = Environment(
            loader=FileSystemLoader(os.path.dirname(os.path.abspath(__file__))),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def _render_sbbs(self, rels: Relations):
        return self._env.get_template("sbbs.j2").render(
            diagram=self.diagram,
            techn="Authentication",
            sbbs=self._solution_building_blocks.sbb_list,
            relations=rels.relations,
            elements=rels.elements,
            aggregates=rels.aggregates,
            associations=sorted(rels.associations),
            aggregations=sorted(rels.aggregations),
            sbb_tags={i: "gap" for i in self.gaps.sbb_gaps()} if self.gaps else None,
            rel_tags={i: "gap" for i in self.gaps.rel_gaps()} if self.gaps else None,
        )

    def render(self, rels) -> str:
        text = self._render_sbbs(rels)
        return (
            self._env.get_template(self.wrapper).render(text=text)
            if self.wrapper
            else text
        )


class TestPlantUmlRenderer(unittest.TestCase):
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
            "Name": "sbb3",
            "Type": "System",
            "Version": "2",
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

    views = [
        {
            "Source": "Person:sbb4:1",
            "Destination": "System:sbb3:2",
            "Label": "view_label1",
        },
        {
            "Source": "System:sbb3:2",
            "Destination": "Enterprise:sbb2:1",
            "Label": "__Aggregation__",
        },
        {
            "Source": "Enterprise:sbb2:1",
            "Destination": "Boundary:sbb1:1",
            "Label": "__Aggregation__",
        },
    ]

    def test_render(self):
        self.maxDiff = None
        rels = Relations(__class__.views)
        sbbs = SolutionBuildingBlocks(__class__.sbb_list)
        renderer = PlantUmlRenderer("landscape", sbbs, wrapper=None)
        self.assertEqual(
            rels.render(renderer),
            """
Person(Person_sbb4, "sbb_label4", $descr="sbb4 description", $tags="")

Boundary(Boundary_sbb1, "sbb_label1") {
Enterprise_Boundary(Enterprise_sbb2, "sbb_label2") {
System(System_sbb3, "sbb_label3", $descr="sbb3 description", $tags="")
}
}


Rel(Person_sbb4, System_sbb3, "view_label1", $techn="", $tags="")
""",
        )
