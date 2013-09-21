def source_for_autocomplete(source, marker="/*POINT*/"):
    for row, line in enumerate(source.split("\n"), start=1):
        if marker in line:
            col = line.index(marker) + 1
            return (row, col), source.replace(marker, "")
