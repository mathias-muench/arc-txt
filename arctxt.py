import csv
import jinja2
import subprocess
import webbrowser
import glob
from pathlib import Path

iuml = """
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
"""

with open("sbb.tsv", "r") as tsv_file:
    sbbs = dict()
    for row in csv.DictReader(tsv_file, dialect="excel-tab"):
        id = row["Type"] + "_" + row["Name"]
        sbbs[id] = row

    env = jinja2.Environment(trim_blocks=True, lstrip_blocks=True)
    template = env.from_string(iuml)
    with open("sbb.iuml", "w") as iuml_file:
        iuml_file.write(template.render(sbbs=sbbs))

puml = """
@startuml
!include <C4/C4_Context>
!include ./sbb.iuml

{% for i in rels %}
${{ i.SType ~ '_' ~ i.SName  }}()
${{ i.DType ~ '_' ~ i.DName }}()
Rel({{ i.SType ~ '_' ~ i.SName  }}, {{ i.DType ~ '_' ~ i.DName }}, "{{ i.Label }}", "{{ i[view] }}")
{% endfor %}

'LAYOUT_LANDSCAPE()
SHOW_LEGEND()
@enduml
"""

views = map(lambda f: Path(f).stem, glob.glob("*-*.tsv"))
for view in views:
    with open(f"{view}.tsv", "r") as tsv_file:
        rels = csv.DictReader(tsv_file, dialect="excel-tab")
        env = jinja2.Environment(trim_blocks=True, lstrip_blocks=True)
        template = env.from_string(puml)
        with open(f"{view}.puml", "w") as puml_file:
            puml_file.write(template.render(rels=list(rels), view="Authentication"))

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

