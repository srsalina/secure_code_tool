# secure_code_tool

### Resolving Git History Issues

To resolve an issue with a large file accidentally committed to the repository (`venv/lib/python3.9/site-packages/torch/lib/libtorch_cpu.dylib`), we used `git-filter-repo` to remove the file from the history. Afterward, we force-pushed the cleaned history to GitHub. This successfully removed the large file while maintaining the integrity of the project's commit history.
