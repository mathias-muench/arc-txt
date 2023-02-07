import csv
import jinja2
import subprocess
import webbrowser
import glob
from pathlib import Path

iuml = """
!global $levels = 0
!procedure $close_boundary()
!while $levels > 0
}
!$levels = $levels - 1
!endwhile
!endprocedure

{% for sbb in sbbs %}
{% set id = sbb.Type ~ "__" ~ sbb.Name %}
!function ${{ id }}()
!if ("{{ sbb.BType }}" != "")
%call_user_func("${{ sbb.BType }}__{{ sbb.BName }}")
!$levels = $levels + 1
!endif
{% if sbb.Type in ["Enterprise_Boundary", "System_Boundary"] %}
{{ sbb.Type }}({{ id }}, "{{ sbb.Label }}") {
{% else %}
{{ sbb.Type }}({{ id }}, "{{ sbb.Label }}", "{{ sbb.Description }}")
!if ("{{ sbb.BType }}" != "")
$close_boundary()
!endif
{% endif %}
!return {{ id }}
!endfunction
{% endfor %}
"""

with open("sbb.tsv", "r") as tsv_file:
    sbbs = csv.DictReader(tsv_file, dialect="excel-tab")
    e = jinja2.Environment()
    t = e.from_string(iuml)
    with open("sbb.iuml", "w") as iuml_file:
        iuml_file.write(t.render(sbbs=list(sbbs)))

puml = """
@startuml
!include <C4/C4_Context>
!include ./sbb.iuml

{% for i in rels %}
Rel(${{ i.SType ~ '__' ~ i.SName  }}(), ${{ i.DType ~ '__' ~ i.DName }}(), "{{ i.Label }}", "{{ i[view] }}")
{% endfor %}

'LAYOUT_LANDSCAPE()
SHOW_LEGEND()
@enduml
"""

views = map(lambda f: Path(f).stem, glob.glob("*-*.tsv"))
for view in views:
    with open(f"{view}.tsv", "r") as tsv_file:
        rels = csv.DictReader(tsv_file, dialect="excel-tab")
        e = jinja2.Environment()
        t = e.from_string(puml)
        with open(f"{view}.puml", "w") as puml_file:
            puml_file.write(t.render(rels=list(rels), view="Authentication"))

    for format in ["svg", "png"]:
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

    webbrowser.open_new(f"{view}.svg")

