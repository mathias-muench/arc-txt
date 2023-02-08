import unittest
import jinja2
from SolutionBuildingBlocks import SolutionBuildingBlocks


class PlantUmlRenderer:
    _sbbs_template = """
{% macro open(id) %}
{% if id %}
{% set sbb = sbbs[id] %}
{{ open(sbb.Parent) -}}
{{ sbb.Type }}({{ id }}, "{{ sbb.Label }}") {
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
!procedure ${{ id }}()
{{ open(sbb.Parent) -}}
{{ sbb.Type }}({{ id }}, "{{ sbb.Label }}", "{{ sbb.Description }}")
{{ close(sbb.Parent) -}}
!endprocedure

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
Rel({{ i.SType ~ '_' ~ i.SName  }}, {{ i.DType ~ '_' ~ i.DName }}, "{{ i.Label }}", "{{ i[view] }}")

{% endfor %}

'LAYOUT_LANDSCAPE()
SHOW_LEGEND()
@enduml"""

    def __init__(self, solution_building_blocks):
        self._solution_building_blocks = solution_building_blocks
        self._env = jinja2.Environment(trim_blocks=True, lstrip_blocks=True)

    def _render_sbbs(self):
        template = self._env.from_string(__class__._sbbs_template)
        return template.render(
            sbbs=self._solution_building_blocks.sbb_list,
            aggr=self._solution_building_blocks.get_sbb_aggr(),
            used=["Person_sbb4", "System_sbb3"]
        )


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

    def test_render_sbbs(self):
        sbbs = SolutionBuildingBlocks(__class__.sbb_list)
        renderer = PlantUmlRenderer(sbbs)
        print(renderer._render_sbbs()),
        return
        self.assertEqual(
            renderer._render_sbbs(),
            """
!procedure Enterprise_Boundary_sbb1()
Enterprise_Boundary(Enterprise_Boundary_sbb1, "sbb_label1", "sbb1 description")
!endprocedure

!procedure Boundary_sbb2()
Boundary(Boundary_sbb2, "sbb_label2", "sbb2 description")
!endprocedure

""",
        )
