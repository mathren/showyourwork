from helpers import (
    TemporaryShowyourworkRepository,
    ShowyourworkRepositoryActions,
)
from showyourwork import exceptions
import pytest


class TestFallbackRules(
    TemporaryShowyourworkRepository, ShowyourworkRepositoryActions
):
    """Test the fallback rules that inform the user about missing article dependencies."""

    # No need to test this on CI
    local_build_only = True

    def build_local(self):
        # Build a blank article
        super().build_local()

        # Add a figure environment to the tex file w/ a script command,
        # but don't actually create the script. The build should fail
        # with an informative message.
        self.add_figure_environment()
        try:
            super().build_local()
        except Exception as e:
            if (
                not "No rule to generate src/tex/figures/test_figure.pdf"
                in str(e)
            ):
                raise Exception(f"Incorrect exception message: {str(e)}")
        else:
            raise Exception(
                "Expected failure, but article build step succeeded."
            )

        # Now add the script. The build should succeed
        self.add_figure_script()
        super().build_local()


@pytest.mark.xfail(reason="This is a Snakemake 'feature'.")
class TestDeletedScript(
    TemporaryShowyourworkRepository, ShowyourworkRepositoryActions
):
    """Test the behavior of the workflow when the user deletes a figure script."""

    # No need to test this on CI
    local_build_only = True

    def build_local(self):
        # Add a figure script
        self.add_figure_script()

        # Add a figure environment to the tex file
        self.add_figure_environment()

        # The build should pass
        super().build_local()

        # Delete the figure script. The build should now fail.
        (self.cwd / "src" / "scripts" / "test_figure.py").unlink()
        try:
            super().build_local()
        except Exception as e:
            if (
                not "No rule to generate src/tex/figures/test_figure.pdf"
                in str(e)
            ):
                raise Exception(f"Incorrect exception message: {str(e)}")
        else:
            raise Exception(
                "Expected failure, but article build step succeeded."
            )