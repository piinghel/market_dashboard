import streamlit as st
from pages.page1 import run_page1
from pages.page2 import run_page2

def main():
    
    st.sidebar.title("Menu")
    option = st.sidebar.selectbox(
        'Choose page',
         ('general overview', 'correlations'))

    if option == "general overview":
        run_page1()
    
    elif option == "correlations":
        run_page2()
        
if __name__ == "__main__":
    st.beta_set_page_config(layout="wide")
    main()
 