import streamlit as st
from db_connection import recommend_professors, find_research_partners, send_collaboration_request


def show_professor_recommendations():
    st.subheader("🔬 Professor Recommendations")

    user = st.session_state.get("user")
    if not user or not user.get("research_interests"):
        st.warning("Please complete your profile with research interests to get recommendations.")
        return

    professors = recommend_professors(user["research_interests"])

    if not professors:
        st.info("No matching professors found. Update your research interests for better recommendations.")
        return

    st.write("Based on your research interests, here are professors you might want to collaborate with:")

    for i, prof in enumerate(professors):
        with st.container():
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"### 👨‍🏫 {prof['name']}")
                st.write(f"🏛️ **Department:** {prof['department']}")
                st.write(f"🔬 **Research Interests:** {prof['research_interests']}")

            with col2:
                st.metric("Match", f"{prof['compatibility']}%")
                if st.button(f"Request Collaboration", key=f"rec_req_{prof['user_id']}"):
                    success = send_collaboration_request(user["user_id"], prof['user_id'])
                    if success:
                        st.success(f"✅ Collaboration request sent to {prof['name']}!")
                    else:
                        st.info("You've already sent a request to this professor.")

            st.divider()


def show_research_partners():
    st.subheader("👥 Find Research Partners")

    user = st.session_state.get("user")
    if not user or not user.get("research_interests") or not user.get("department"):
        st.warning("Please complete your profile with department and research interests to find partners.")
        return

    partners = find_research_partners(user["user_id"], user["department"], user["research_interests"])

    if not partners:
        st.info("No matching student partners found. Try updating your research interests.")
        return

    st.write("These students have similar research interests and might be great research partners:")

    for i, partner in enumerate(partners):
        with st.container():
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"### 🎓 {partner['name']}")
                st.write(f"🏛️ **Department:** {partner['department']}")
                st.write(f"🔬 **Research Interests:** {partner['research_interests']}")
                st.write(f"📈 **Experience Level:** {partner['experience_level'].capitalize()}")

            with col2:
                st.metric("Match", f"{partner['compatibility']}%")

            st.divider()