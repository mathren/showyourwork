"""
This script is executed from within the ``zenodo`` rule
to upload/download files from Zenodo.

"""
import sys
from pathlib import Path

# Hack to import our custom functions
sys.path.insert(0, str(Path(__file__).parents[1] / "helpers"))
from helpers.zenodo import upload_simulation, download_simulation

# Upload or download the file
if snakemake.params["action"] == "upload":

    upload_simulation(
        snakemake.params["file_name"],
        snakemake.params["deposit_id"],
        snakemake.params["deposit_title"],
        snakemake.params["deposit_description"],
        snakemake.params["deposit_creators"],
        sandbox=snakemake.params["sandbox"],
        token_name=snakemake.params["token_name"],
        sandbox_token_name=snakemake.params["sandbox_token_name"],
        file_path=snakemake.params["file_path"],
        repo_url=snakemake.params["repo_url"],
        script=snakemake.params["script"],
    )

else:

    download_simulation(
        snakemake.params["file_name"],
        snakemake.params["deposit_id"],
        sandbox=snakemake.params["sandbox"],
        token_name=snakemake.params["token_name"],
        sandbox_token_name=snakemake.params["sandbox_token_name"],
        file_path=snakemake.params["file_path"],
    )
