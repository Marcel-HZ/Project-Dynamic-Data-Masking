def merge_runs(paragraph) -> None:
    runs = paragraph.runs
    if not runs:
        return
    text = "".join(r.text for r in runs)
    runs[0].text = text
    for r in runs[1:]:
        r.text = ""
