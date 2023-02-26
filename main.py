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
    with open("baseline.puml", "w") as f:
        f.write(base.render(PlantUmlRenderer("landscape", sbbs)))
    rels = Relations(read_tsv("C4_Context Diagram Sample - bigbankplc-landscape.tsv"))
    gaps = ArcGaps(base, rels)
    with open("C4_Context Diagram Sample - bigbankplc-landscape.puml", "w") as f:
        f.write(rels.render(PlantUmlRenderer("landscape", sbbs, gaps)))
    rels = Relations(read_tsv("C4_Container Diagram Sample - bigbankplc.tsv"))
    with open("C4_Container Diagram Sample - bigbankplc.puml", "w") as f:
        f.write(rels.render(PlantUmlRenderer("landscape", sbbs, gaps)))
