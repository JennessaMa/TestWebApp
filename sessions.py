from typing import Callable, TypeVar

from streamlit.report_thread import get_report_ctx
from streamlit.server.server import Server

T = TypeVar('T')

# noinspection PyProtectedMember
def get_state(setup_func: Callable[..., T], **kwargs) -> T:
    ctx = get_report_ctx()

    session = None
    session_infos = Server.get_current()._session_info_by_id.values()


    for session_info in session_infos:
        s = session_info.session
        if (not hasattr(s, '_main_dg') and s._uploaded_file_mgr == ctx.uploaded_file_mgr):
            session = s
        # if s._uploaded_file_mgr == ctx.uploaded_file_mgr:
        #     session = session_info.session

    if session is None:
        raise RuntimeError(
            "Oh noes. Couldn't get your Streamlit Session object"
            'Are you doing something fancy with threads?')

    # Got the session object! Now let's attach some state into it.

    if not getattr(session, '_custom_session_state', None):
        session._custom_session_state = setup_func(**kwargs)

    return session._custom_session_state
