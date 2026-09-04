
# Check the full output and staged_files
print("output keys:", list(result.keys()))
print("\noutput field:", result.get("output", "")[:500])
print("\nfiles_written:", result.get("files_written"))
print("\nstaged_files:", result.get("staged_files"))
print("\noutput_saved_to:", result.get("output_saved_to"))
print("\nstaged_from_workspace:", result.get("staged_from_workspace"))
