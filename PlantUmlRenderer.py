import unittest
import jinja2
from SolutionBuildingBlocks import SolutionBuildingBlocks


class PlantUmlRenderer:
    _sbbs_template = """
{% set boundaries = {
"Enterprise": "Enterprise_Boundary",
"Boundary": "Boundary",
}
%}
{% macro open(id) %}
{% if id %}
{% set sbb = sbbs[id] %}
{{ open(sbb.Parent) -}}
{{ boundaries[sbb.Type] }}({{ "_".join(id) }}, "{{ sbb.Label }}") {
{% endif %}
{% endmacro -%}

{% macro close(id) %}
{% if id %}
{% set sbb = sbbs[id] %}
}
{{ close(sbb.Parent) -}}
{% endif %}
{% endmacro -%}

{% for id in used %}
{% set sbb = sbbs[id] %}
{{ open(sbb.Parent) -}}
{{ sbb.Type }}({{ "_".join(id) }}, "{{ sbb.Label }}", "{{ sbb.Description }}")
{{ close(sbb.Parent) }}
{% endfor %}
"""

    _views_template = """
{% for view in views %}
Rel(\
{{ "_".join(view.Source) }},\
{{ "_".join(view.Destination) }},\
"{{ view.Label }}"\
)
{% endfor %}
"""

    def _find_used_sbbs(self) -> list:
        used = list()
        for view in self._architecture_views:
            for i in ["Source", "Destination"]:
                if view[i] not in used:
                    used.append(view[i])
        return used

    def __init__(self, solution_building_blocks, architecture_views: list):
        self._solution_building_blocks = solution_building_blocks
        self._architecture_views = architecture_views
        self._used = self._find_used_sbbs()
        self._env = jinja2.Environment(trim_blocks=True, lstrip_blocks=True)

    def _render_sbbs(self):
        template = self._env.from_string(__class__._sbbs_template)
        return template.render(
            sbbs=self._solution_building_blocks.sbb_list, used=self._used
        )

    def _render_views(self):
        template = self._env.from_string(__class__._views_template)
        return template.render(
            views=self._architecture_views,
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
            "Source": ("Person", "sbb4"),
            "Destination": ("System", "banking_system"),
            "Label": "view_label1",
        }
    ]

    def setUp(self):
        self.maxDiff = None
        sbbs = SolutionBuildingBlocks(__class__.sbb_list)
        self.renderer = PlantUmlRenderer(sbbs, __class__.views)

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
            """
Rel(Person_sbb4,System_banking_system,"view_label1")
""",
        )
