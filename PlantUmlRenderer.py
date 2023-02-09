import unittest
import jinja2
from SolutionBuildingBlocks import SolutionBuildingBlocks


class PlantUmlRenderer:
    _sbbs_template = """
{% set boundaries = {
"Enterprise": "Enterprise_Boundary",
}
%}
{% macro open(id) %}
{% if id %}
{% set sbb = sbbs[id] %}
{{ open(sbb.Parent) -}}
{{ boundaries[sbb.Type] }}({{ id }}, "{{ sbb.Label }}") {
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
{{ sbb.Type }}({{ id }}, "{{ sbb.Label }}", "{{ sbb.Description }}")
{{ close(sbb.Parent) }}
{% endfor %}
"""

    _views_template = """
{% for view in views %}
Rel(\
{{ view.SType ~ '_' ~ view.SName  }},\
{{ view.DType ~ '_' ~ view.DName }},\
"{{ view.Label }}"\
)
{% endfor %}
"""

    _puml = """@startuml
!include <C4/C4_Context>

{% set used_sbbs = [] %}
{% for i in rels %}
{% for id in [ i.SType ~ '_' ~ i.SName, i.DType ~ '_' ~ i.DName ]  %}
{% if id not in used_sbbs %}
{% set sbb = sbbs[id] %}
{% if sbb.Enterprise != "" %}
Enterprise_Boundary({{ sbb.Enterprise }}, "{{ sbbs[sbb.Enterprise].Label }}") {
{% endif %}
{{ sbb.Type }}({{ id }}, "{{ sbb.Label }}", "{{ sbb.Description }}")
{% if sbb.Enterprise != "" %}
}
{% endif %}
{{ used_sbbs.append(id) or "" }}
{% endif %}
{% endfor %}
Rel(\
    {{ i.SType ~ '_' ~ i.SName  }},\
    {{ i.DType ~ '_' ~ i.DName }},\
    "{{ i.Label }}", "{{ i[view] }}"\
)

{% endfor %}

'LAYOUT_LANDSCAPE()
SHOW_LEGEND()
@enduml"""

    def __init__(self, solution_building_blocks, architecture_views: list):
        self._solution_building_blocks = solution_building_blocks
        self._architecture_views = architecture_views
        self._used = ["Person_customer", "System_banking_system"]
        self._env = jinja2.Environment(trim_blocks=True, lstrip_blocks=True)

    def _render_sbbs(self):
        template = self._env.from_string(__class__._sbbs_template)
        return template.render(
            sbbs=self._solution_building_blocks.sbb_list,
            used=self._used
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

    views = [
        {
            "SType": "Person",
            "SName": "sbb4",
            "Desination": "System_sbb3",
            "DType": "System",
            "DName": "sbb3",
            "Label": "view_label1",
        }
    ]

    def test_render_sbbs(self):
        sbbs = SolutionBuildingBlocks(__class__.sbb_list)
        renderer = PlantUmlRenderer(sbbs, __class__.views)
        self.assertEqual(
            renderer._render_sbbs(),
            """
Person(Person_sbb4, "sbb_label4", "sbb4 description")

Enterprise_Boundary(Enterprise_Boundary_sbb1, "sbb_label1") {
Boundary(Boundary_sbb2, "sbb_label2") {
System(System_sbb3, "sbb_label3", "sbb3 description")
}
}

""",
        )

    def test_render_views(self):
        views = self.views
        renderer = PlantUmlRenderer(views, __class__.views)
        self.assertEqual(
            renderer._render_views(),
            """
Rel(Person_sbb4,System_sbb3,"view_label1")
""",
        )
