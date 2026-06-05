from src.ui.app.documents.page import render as render_documents
from src.ui.app.home.page import render as render_home
from src.ui.app.runs.page import render as render_runs
from src.ui.app.settings.page import render as render_settings
from src.ui.shared.layout import bootstrap_app
from src.ui.shared.navigation import render_navigation
from src.ui.shared.state import init_session_state


PAGES = {
    "Home": render_home,
    "Documents": render_documents,
    "Runs": render_runs,
    "Settings": render_settings,
}


def main() -> None:
    init_session_state()
    bootstrap_app()
    page_name = render_navigation()
    PAGES[page_name]()


if __name__ == "__main__":
    main()
