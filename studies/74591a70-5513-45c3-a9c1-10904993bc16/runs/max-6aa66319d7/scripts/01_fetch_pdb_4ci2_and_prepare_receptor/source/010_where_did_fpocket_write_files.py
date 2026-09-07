
# where did fpocket write its files?
print("files_written:", fp.get("files_written", [])[:5])
print("staged_files:", fp.get("staged_files", [])[:5])
print("staged_from_workspace:", fp.get("staged_from_workspace"))
print("path_rewrites:", fp.get("path_rewrites"))
print("output snippet:", str(fp.get("output",""))[:400])
print("summary:", str(fp.get("summary",""))[:600])
