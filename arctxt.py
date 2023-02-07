import csv
import jinja2
import subprocess
import webbrowser
import glob
from pathlib import Path

puml = """
@startuml
!include <C4/C4_Context>

{% for id, sbb in sbbs.items() %}
!procedure ${{ id }}()
{% if sbb.Enterprise != "" %}
Enterprise_Boundary({{ sbb.Enterprise }}, "{{ sbbs[sbb.Enterprise].Label }}") {
{% endif %}
{{ sbb.Type }}({{ id }}, "{{ sbb.Label }}", "{{ sbb.Description }}")
{% if sbb.Enterprise != "" %}
}
{% endif %}
!endprocedure

{% endfor %}

{% set used_sbbs = [] %}
{% for i in rels %}
{% for id in [ i.SType ~ '_' ~ i.SName, i.DType ~ '_' ~ i.DName ]  %}
{% if id not in used_sbbs %}
${{ id }}()
{{ used_sbbs.append(id) or "" }}
{% endif %}
{% endfor %}
Rel({{ i.SType ~ '_' ~ i.SName  }}, {{ i.DType ~ '_' ~ i.DName }}, "{{ i.Label }}", "{{ i[view] }}")

{% endfor %}

'LAYOUT_LANDSCAPE()
SHOW_LEGEND()
@enduml
"""

with open("sbb.tsv", "r") as tsv_file:
    sbbs = dict()
    for row in csv.DictReader(tsv_file, dialect="excel-tab"):
        id = row["Type"] + "_" + row["Name"]
        sbbs[id] = row

views = map(lambda f: Path(f).stem, glob.glob("*-*.tsv"))
for view in views:
    with open(f"{view}.tsv", "r") as tsv_file:
        rels = list(csv.DictReader(tsv_file, dialect="excel-tab"))

    env = jinja2.Environment(trim_blocks=True, lstrip_blocks=True)
    template = env.from_string(puml)
    with open(f"{view}.puml", "w") as puml_file:
        puml_file.write(template.render(sbbs=sbbs, rels=rels, view="Authentication"))

    for format in []:
        subprocess.run(
            [
                "java",
                "-jar",
                "/home/mun5grb/.local/share/java/plantuml.jar",
                "--charset UTF-8",
                "plantuml",
                f"-t{format}",
                f"{view}.puml",
            ]
        )

    # webbrowser.open_new(f"{view}.svg")

