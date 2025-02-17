import streamlit as st
import xlwt
import os
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import tempfile
import requests

st.set_page_config(layout="wide")

# CSS to center the elements
st.markdown(
    """
    <style>
    .center {
        display: flex;
        justify-content: center;
        text-align: center;
    }
        </style>
    """,
    unsafe_allow_html=True
)

# Centering the headers
st.markdown("<h2 class='center' style='color:rgb(80, 200, 120);'>An EsteStyle Streamlit Page<br>Where Python Wiz Meets Data Viz!</h2>", unsafe_allow_html=True)
st.markdown("<h2 class='center'></h1>", unsafe_allow_html=True)

st.markdown("<img src='https://1drv.ms/i/s!ArWyPNkF5S-foZspwsary83MhqEWiA?embed=1&width=307&height=307' width='300' style='display: block; margin: 0 auto;'>" , unsafe_allow_html=True)

st.markdown("<h2 class='center'> </h1>", unsafe_allow_html=True)

st.markdown("<h2 class='center' style='color: rgb(80, 200, 120);'>Activity Text File to Excel File<br>Conversion App</h2>", unsafe_allow_html=True)

st.markdown("<h2 class='center'> </h1>", unsafe_allow_html=True)

st.markdown("<h3 class='center' style='color: gold;'>- Originally created at the University of Colorado Denver 🦬</h2>" , unsafe_allow_html=True)
st.markdown("<h3 class='center' style='color: gold;'>- In the Greenwood Laboratory for the Neuroscience of Exercise 🏃‍♀️</h2>", unsafe_allow_html=True)
st.markdown("<h3 class='center' style='color: rgb(80, 200, 120);'>- By Esteban C Loetz 👨‍💻</h2>" , unsafe_allow_html=True)

st.markdown("<h1 class='center'> </h1>", unsafe_allow_html=True)
    
def LOCOTxt2ExlScript(text_file_path, count, output_path):
    SubjectNumbr = int(count)

    # Creation of a text file listing all data without any spaces
    output=""
    with open(text_file_path) as f:
        for line in f:
            if not line.isspace():
                output+=line
    f = open("output.txt", "w")
    f.write(output)

    subj_ID_anchor      = 21
    chbr_ID_anchor      = 16
    grp_ID_anchor       = 23
    date_ID_anchor      = 26
    dist_trav_anchor    = 32
    tot_dist_loc_anchor = 60
    line_shift_per_subj = 0
    x                   = 1

    book = xlwt.Workbook()
    sheet1 = book.add_sheet('sheet1')
    sheet1.write(0,0, text_file_path)
    sheet1.write(1,0, 'RunDate')
    sheet1.write(1,1, 'SubjID')
    sheet1.write(1,2, 'BoxID')
    sheet1.write(1,3, 'GrpID')
    sheet1.write(1,16,'TotDist')

    for col in range(4,16,1):
        binnum = str(col - 3)
        sheet1.write(1,col,'Bin'+binnum)

    for SubjectNumbr in range(1,SubjectNumbr+1):
        
        x                   += 1
        Group_ID            = grp_ID_anchor       + line_shift_per_subj
        Start_Date          = date_ID_anchor      + line_shift_per_subj
        Chamber_Number      = chbr_ID_anchor      + line_shift_per_subj
        Subject_ID_line     = subj_ID_anchor      + line_shift_per_subj
        First_Dist_Trav_Val = dist_trav_anchor    + line_shift_per_subj
        Tot_Dist_Loc        = tot_dist_loc_anchor + line_shift_per_subj
        line_shift_per_subj += 71
        s                   = 0

        # Bin creation for 60min of locomotion behavior. 12 5min Bins = 60min.
        bins = 12
        anc_bin = First_Dist_Trav_Val+bins

        # Reading of the previously created 'output' datafile.
        with open('output.txt') as medtxtfile:
            content = medtxtfile.readlines()

        # List of lines containing distance traveled.
        specific_lines_dist_trav_shift = []
        
        # for loop appending distance traveled data to above list.
        for line in range(First_Dist_Trav_Val, anc_bin):
            line += s
            specific_lines_dist_trav_shift.append(line)

        # Function to remove empty spaces separating data.
        def remove_space(slicedp1):
            return "".join(slicedp1.split())

        # Prints the subject number above 5min bin data in terminal
        print(str(SubjectNumbr)+ " sum of dist. trav. (cm per 5min)")
        
        # List of sliced line sections containing distance traveled data.
        five_min_time_bin_List = []
        
        # for loop appending distance traveled data slices to above list.
        for pos, A_num in enumerate(content):
            A_num = A_num.rstrip()
            if pos in specific_lines_dist_trav_shift:
                sicedp1 = A_num [0:9]
                slcflt = (float(remove_space(sicedp1)))
                five_min_time_bin_List.append(slcflt)
                # Prints dist trav slices to terminal
                print(slcflt)
        
        # for loop writing distance traveled data slices to Excel cells.
        for i, e in enumerate(five_min_time_bin_List,start=4):
            sheet1.write(x,i,e)

        # Creation of subject variable associated information 
        # identifying which lines and where to slice each
        # & writing info to Excel cells.
        RunDate_line = content[Start_Date]
        RDS = slice(30,41)
        sheet1.write(x,0,RunDate_line[RDS])

        SubjID_line = content[Subject_ID_line]
        IDS = slice(30,38)
        sheet1.write(x,1,SubjID_line[IDS])

        GroupID_line = content[Group_ID]
        GRS = slice(30,38)
        sheet1.write(x,3,GroupID_line[GRS])

        Box_line = content[Chamber_Number]
        BS = slice(30,38)
        sheet1.write(x,2,Box_line[BS])

        TotDist_line = (content[Tot_Dist_Loc])
        TD = (slice(21,32))
        sheet1.write(x,16,float(TotDist_line[TD]))

    # Save the workbook to a file
    book.save(output_path)
    return output_path
    
def graph_means_sem(excel_name):
    # Load data from Excel
    data = pd.read_excel(excel_name, header=1)

    # Calculate mean and SEM for each bin
    bins = ['Bin1', 'Bin2', 'Bin3', 'Bin4', 'Bin5', 'Bin6', 'Bin7', 'Bin8', 'Bin9', 'Bin10', 'Bin11', 'Bin12']
    average_activity = data[bins].mean()
    sem_activity = data[bins].sem()

    # Plot the bar chart with error bars
    plt.figure(figsize=(10, 8))
    average_activity.plot(kind='bar', yerr=sem_activity, color='skyblue', ecolor='grey', capsize=3)
    plt.title('Mean Locomotor Activity Over Time & SEM')
    plt.xlabel('5min Time Bins')
    plt.ylabel('Mean Distance Traveled (cm)')

    # Use Streamlit to display the plot
    st.pyplot(plt)

    df = data
    # Create the plot
    plt.figure(figsize=(10, 8))
    for rat_id in df['SubjID'].unique():
        rat_data = df[df['SubjID'] == rat_id]
        plt.plot(bins, rat_data[bins].values[0], marker='o', label=f'SubjID {rat_id}')

    # Set plot title and labels
    plt.title('Total Bin Distances for All Individual SubjIDs')
    plt.xlabel('5min Time Bins')
    plt.ylabel('Distance Traveled (cm)')
    plt.legend()

    # Display the plot in Streamlit
    st.pyplot(plt)

def is_valid_file(uploaded_file):
    if uploaded_file is not None:
        return True
    else:
        return False

####### Logic for Streamlit UX ######

# File uploader in Streamlit
uploaded_file = st.file_uploader("Select the Med Associates output text(.txt) file\n" 
            "to be copied and converted to an Excel file", type="txt")

# Check if file has been uploaded and update session state
if 'file_uploaded' not in st.session_state:
    st.session_state.file_uploaded = False

if uploaded_file is not None:
    st.session_state.file_uploaded = True

# Process the file if it's valid
if st.session_state.file_uploaded:
    if is_valid_file(uploaded_file):
        text_data = uploaded_file.read().decode("utf-8")
        st.write(":green[File uploaded and validated successfully]")

        # Count the occurrences of 'Activity Summary' to generate total processing interations
        count = text_data.count('Activity Summary')

        # Output occurences to verify subj number with user
        st.write(f"The number of subjects detected in this file is :blue[{count}]")

        # Save the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
            temp_file.write(text_data.encode("utf-8"))
            temp_file_path = temp_file.name

        st.write("Note: the generated Excel file will be saved into the original Text file's directory")

    else:
        st.error("A selected file path is incorrect or has been left empty.")

    # Create a button to activate data processing
    if st.button(":green[Press to convert the Text file into an Excel file]"):
        output_path = os.path.join("grand_spanking_new_processed_data.xls")
        # Call the data processing function
        saved_file_path = LOCOTxt2ExlScript(temp_file_path, count, output_path)
        
        st.write(f"File has been saved to: :blue[{saved_file_path}]")

        graph_means_sem(saved_file_path)

else:
    st.info("Please upload a file.")
st.title("")
if st.button("View example input Text file, output Excel file & Verification plots"):
    # URL to the example text file on OneDrive
    example_file_url = "https://1drv.ms/t/s!ArWyPNkF5S-foaQKpqRMurktxTDObg?e=Ngck4Y"

    # Download the contents of the text file
    response = requests.get(example_file_url)
    file_content = response.text

    # Display the contents in a text area
    st.text_area("Example Input Text File", file_content, height=300)

    # Path to the example Excel file
    example_excel_path = r"X:\Code_Projects\Streamlit\Loco_txt_Converter\grand_spanking_new_processed_data.xls"

    # Load the data from the Excel file, skipping the first row
    df = pd.read_excel(example_excel_path, header=1, index_col=None)

    # Display the cleaned data as a table in Streamlit without the default index column
    st.write("Example Excel File Data:")
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Assuming 'uploaded_file' is the file you want to process
    uploaded_file = example_file_url

    # Since 'uploaded_file' is actually a file URL, you should re-read its content
    response = requests.get(uploaded_file)
    text_data = response.text

    # Display success message
    st.write(":green[File uploaded and validated successfully]")

    # Count the occurrences of 'Activity Summary' to generate total processing interations
    count = text_data.count('Activity Summary')

    # Output occurences to verify subj number with user
    st.write(f"The number of subjects detected in this file is :blue[{count}]")

    # Save the uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
        temp_file.write(text_data.encode("utf-8"))
        temp_file_path = temp_file.name

    st.write("Note: the generated Excel file will be saved into the original Text file's directory")

    output_path = os.path.join("grand_spanking_new_processed_data.xls")
    # Call the data processing function
    saved_file_path = LOCOTxt2ExlScript(temp_file_path, count, output_path)
        
    st.write(f"File has been saved to: :blue[{saved_file_path}]")

    graph_means_sem(saved_file_path)
