import unittest
import jinja2
from SolutionBuildingBlocks import SolutionBuildingBlocks


class PlantUmlRenderer:
    _sbbs_template = """
{% for id, sbb in sbbs.items() %}
{{ sbb.Type }}({{ id }}, "{{ sbb.Label }}", "{{ sbb.Description }}")
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
        return template.render(sbbs=self._solution_building_blocks.get_sbb_list())


class TestPlantUmlRenderer(unittest.TestCase):
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

    def test_render_sbbs(self):
        sbbs = SolutionBuildingBlocks(__class__.sbb_list)
        renderer = PlantUmlRenderer(sbbs)
        self.assertEqual(
            renderer._render_sbbs(),
            """
sbb_type1(sbb_type1_sbb1, "sbb_label1", "sbb1 description")
sbb_type2(sbb_type2_sbb2, "sbb_label2", "sbb2 description")
""",
        )
