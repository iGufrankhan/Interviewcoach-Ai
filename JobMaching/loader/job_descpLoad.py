from utils.apierror import APIError


class JobDescriptionLoader:

    def load_job_description(self, description: str) -> str:
        """Load and return the job description as-is (lowercase)"""
        if not description or not description.strip():
            raise APIError(
                status_code=400,
                message="Job description cannot be empty",
                error_code="EMPTY_DESCRIPTION"
            )
        return description.lower()