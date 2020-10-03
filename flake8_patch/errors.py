from flake8_plugin_utils import Error


class AssignmentError(Error):
    code = "PAT001"
    message = (
        "assignment to imported name '{name}' might lead to flaky tests, "
        "use patch instead"
    )
