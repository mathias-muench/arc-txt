import csv
from SolutionBuildingBlocks import SolutionBuildingBlocks
from PlantUmlRenderer import PlantUmlRenderer


def read_tsv(filename: str) -> list:
    with open(filename, "r") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return list(reader)


if __name__ == "__main__":
    sbbs = SolutionBuildingBlocks(read_tsv("sbbs.tsv"))
    view = read_tsv("C4_Context Diagram Sample - bigbankplc-landscape.tsv")
    renderer = PlantUmlRenderer(sbbs, view)
    print(renderer.render()),
