import csv


def export_to_csv(headers: list[str], data: list[dict[str, str | float]]) -> str:
    file_path = "/tmp/export.csv"

    with open(file_path, "w") as fp:
        writer = csv.DictWriter(fp, delimiter=";", fieldnames=headers)
        writer.writeheader()
        for item in data:
            writer.writerow(item)

    return file_path
