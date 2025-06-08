import streamlit as st
import pages

# 페이지 함수
if st.session_state.page == "home":
    pages.main()
elif st.session_state.page == "game":
    pages.game_clicked_page()
elif st.session_state.page == "user":
    pages.user_clicked_page()
elif st.session_state.page == "exit":
    pages.exit_clicked_page()
elif st.session_state.page == "make_user":
    pages.make_user_page()
elif st.session_state.page == "exist_user":
    pages.exist_user_page()
elif st.session_state.page == "ready_game":
    pages.ready_game_page()
elif st.session_state.page == "rcp1":
    pages.rcp_game_page1()
elif st.session_state.page == "rcp2":
    pages.rcp_game_page2()
elif st.session_state.page == "rcp3":
    pages.rcp_game_page3()
elif st.session_state.page == "rcp4":
    pages.rcp_game_page4()
elif st.session_state.page == "user_info":
    pages.user_info_page()
