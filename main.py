import csv
from SolutionBuildingBlocks import SolutionBuildingBlocks
from PlantUmlRenderer import PlantUmlRenderer


def read_tsv(filename: str) -> list:
    with open(filename, "r") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return list(reader)


if __name__ == "__main__":
    sbbs = SolutionBuildingBlocks(read_tsv("sbbs.tsv"))
    view = list()
    for i in read_tsv("C4_Context Diagram Sample - bigbankplc-landscape.tsv"):
        view.append(
            {
                "Source": (i["SType"], i["SName"]),
                "Destination": (i["DType"], i["DName"]),
                "Label": i["Label"],
            }
        )

    renderer = PlantUmlRenderer(sbbs, view)
    print(renderer.render()),
