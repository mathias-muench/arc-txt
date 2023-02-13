import csv

from PlantUmlRenderer import PlantUmlRenderer
from Relations import Relations
from SolutionBuildingBlocks import SolutionBuildingBlocks
from ArcGaps import ArcGaps


def read_tsv(filename: str) -> list:
    with open(filename, "r") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return list(reader)


if __name__ == "__main__":
    sbbs = SolutionBuildingBlocks(read_tsv("sbbs.tsv"))
    base = Relations(read_tsv("baseline.tsv"))
    rels = Relations(read_tsv("C4_Context Diagram Sample - bigbankplc-landscape.tsv"))
    gaps = ArcGaps(base, rels)
    renderer = PlantUmlRenderer("landscape", sbbs, rels, gaps)
    with open("C4_Context Diagram Sample - bigbankplc-landscape.puml", "w") as f:
        f.write(renderer.render_puml())
    rels = Relations(read_tsv("C4_Container Diagram Sample - bigbankplc.tsv"))
    renderer = PlantUmlRenderer("container", sbbs, rels, gaps)
    with open("C4_Container Diagram Sample - bigbankplc.puml", "w") as f:
        f.write(renderer.render_puml())
