"""
====> LMS Migrator <====

This tool duplicates an existing course (exported according to IMS Common
Cartridge 1.1 standards) and revises activity due dates according to user
specifications in a properly formatted new_syllabus.xlsx file.

Warning: Use this tool with caution. Not responsible for loss of data!

This script requires the following modules and their dependencies:
    - openpyxl, which is responsible for reading new_syllabus.xlsx
    - BeautifulSoup 4, which facilitates searching through the XML data exported
      by the LMS
"""

# ==== INDICATE VERSION NUMBER ==== 
version = "1.1.0"


# ==== IMPORT THE REQUIRED MODULES ==== 

import openpyxl as opxl          # Reads the Excel-formatted syllabus.
from bs4 import BeautifulSoup    # For parsing XML course metadata.
from shutil import copytree      # Copies old course content to new folder.
from shutil import rmtree        # For deleting files after completion.
import os                        # Used for gathering working directory info.
import datetime                  # Handle basic date / time manipulations.
from zipfile import ZipFile      # Compression for .imscc archive files.
from sys import exit             # Handles script termination
import tkinter as tk             # Builds graphical interface
from tkinter import filedialog   # Manages graphical file open/save boxes.
from tkinter import scrolledtext as st  # Scrolling text for progress updates.
from inspect import cleandoc     # Cleans up multi-line text for GUI display.

    

# ==== BEGIN DEFINING FUNCTIONS ==== 
# The functions in this section are responsible for updating the course info

def compress_new_course():
    """
    This function accepts generates the new semester's course cartridge.
    It returns nothing.
    """
    
    global filepath_new, filepath_root
    
    # Update the progress window with the status. 
    msg_compress_crs = "Building the modified Common Cartridge file."
    gui_progress_update(msg_compress_crs)
    
    # Make a list of relative paths to all files within new_course, including
    # within subdirectories.
    files_to_bundle = []
    for root, directories, files in os.walk(filepath_root + "new_course"):
        for filename in files:
            filepath = os.path.join(root, filename)
            files_to_bundle.append(filepath)
    
    with ZipFile(filepath_new, mode = "w") as new_course_zip:
        for file in files_to_bundle:
            new_course_zip.write(file)
    
    return


def extract_prev_course():
    """
    This function accepts the filename of the previous semester's exported
    course cartridge. It decompresses it to a new directory, old_course.
    It returns nothing.
    """
    
    global filepath_root, filepath_old

    # Update the progress window with the status.     
    msg_extract_prev = "Extracting the previous term's Common Cartridge file."
    gui_progress_update(msg_extract_prev)

    # Make a new directory, old_course. If it already exists, empty it.
    rmtree(filepath_root + "old_course", ignore_errors = True)
    os.mkdir(filepath_root + "old_course")
    
    # Unpack the common cartridge file.
    with ZipFile(filepath_old, mode = "r") as old_course_zip:
        old_course_zip.extractall(path = filepath_root + "old_course")

    return


def extract_metadata():
    """
    This function opens the user-generated syllabus file,.
    New course metadata are extracted, such as new homework/quiz titles, due
    dates, etc..
    It returns a completed course metadata dictionary, the structure of which
    is defined in a comment below.
    """

    global filepath_syl

    # Update the progress window with the status. 
    msg_extract_meta = "Reading the syllabus."
    gui_progress_update(msg_extract_meta)

    # Open the Excel workbook & read the worksheet named "syllabus"
    syllabus_wb = opxl.load_workbook(filepath_syl)
    syllabus_ws = syllabus_wb["syllabus"]

    # Note: syllabus_ws.values is a list generator, providing one tuple for
    # each data row present. The required format is derived from the format
    # of new_syllabus.xlsx: 
    #    ('Previous Semester Activity Title', 'New Semester Activity Title',
    #     'Available Date', 'Available Time', 'Due Date', 'Due Time',
    #     'Lock Date', 'Lock Time')

    # Extract all the syllabus data to a list of tuples, with one tuple for
    # each row in the Excel syllabus.
    syllabus_data = list(syllabus_ws.values)
        
    # Create the extracted_meta metadata dictionary, which will be populated
    # with individual learning activities. The previous semester's activity 
    # names are the keys in this dictionary, and the values are a subdictionary
    # of metadata for each learning activity, e.g.:
    # extracted_meta = {prev_semester_activity_title_1 :
    #                {"new_title" : new_title,
    #                "new_avail_datetime" : new_avail_datetime,
    #                "new_due_datetime" : new_due_datetime,
    #                "new_lock_datetime" : new_lock_datetime}
    extracted_meta = {}
        
    # Restructure the listed activity information from syllabus_data into the 
    # extracted_meta metadata dictionary.
    # Ignore the first list entry, which contains only the header row
    # information, such as "Activity Title", etc.

    for activity_number in range(1, len(syllabus_data)):
        # Read metatata out of the syllabus. This returns the raw tuple
        # generated by openpyxl upon reading the Excel data row.
        activity_meta = syllabus_data[activity_number]
        
        # Extract useful information from the raw tuple & restructure for the
        # dict.
        old_title = activity_meta[0]
        
        if activity_meta[2]:
            new_avail_datetime = datetime.datetime.combine(activity_meta[2],
                                                           activity_meta[3])
        else:
            new_avail_datetime = None
        
        if activity_meta[4]:
            new_due_datetime = datetime.datetime.combine(activity_meta[4],
                                                         activity_meta[5])
        else:
            new_due_datetime = None
        
        if activity_meta[6]:
            new_lock_datetime = datetime.datetime.combine(activity_meta[6],
                                                          activity_meta[7])
        else:
            new_lock_datetime = None

        # Add this activity's updated information to the extracted_meta
        # metadata dictionary.
        extracted_meta[old_title] = {"new_title" : activity_meta[1],
                                     "new_avail_datetime" : new_avail_datetime,
                                     "new_due_datetime" : new_due_datetime,
                                     "new_lock_datetime" : new_lock_datetime}
    
    # Print a status update.
    # print("Done.")
                                     
    return extracted_meta


def find_activities():
    """
    This function serves two closely related roles:
         - Copy the prior semester's course content from the old_course
           directory to the to new_course directory
         - Make a list of subdirectories within new_course (absolute paths) that
           are likely to contain learning activities (quizzes, homework, etc.).
    """
    
    global filepath_root
    
    # Update the progress window with the status. 
    msg_find_act = "Copying data from the previous term."
    gui_progress_update(msg_find_act)

    # Make a copy of the old course files.
    # Ultimately, we'll edit the due dates and related metadata within
    # new_course. Nothing is modified in old_course.
    copytree(filepath_root + "old_course", filepath_root + "new_course")

    # Generate a list of copied learning activities.
    # Scan the new_course directory. Learning activities (quizzes, assignments,
    # etc.) are stored in subdirectories with long, arbitrary alphanumeric names
    # (>20 characters). Generate a list (act_subdirs) of these
    # subdirectories. 
    # Exclude files (by checking that os.path.isdir is True. Also exclude
    # subdirectories that do not contain learning activities (e.g.:
    # course_settings) based upon the number of characters present.
    new_course_dir = filepath_root + "new_course/"
    act_subdirs = [new_course_dir + dir for dir in os.listdir(new_course_dir)
                    if (os.path.isdir("new_course/" + dir) and len(dir) > 20)
                  ]
    
    # Print a status update.
    # print("Done.")
    
    return act_subdirs


def format_datetime(local_dt):
    """
    This function accepts a local datetime object.
    It converts it to a UTC-based datetime object, then generates a string
    in the LMS's accepted date/time format, YYYY-MM-DDTHH:MM:SS, e.g:
    2020-09-14T14:00:00.
    """
    
    # Convert the local datetime into seconds from epoch, then into a UTC-
    # referenced datetime object.
    local_epoch_dt = float(local_dt.strftime("%s"))
    utc_dt = datetime.datetime.utcfromtimestamp(local_epoch_dt)
    
    # Generate a date/time string in the expected format.
    formatted_dt = utc_dt.strftime("%Y-%m-%dT%H:%M:%S")
    
    return formatted_dt


def update_file_meta(abs_path_to_file):
    """
    This function accepts the absolute path to a file that has already been
    verified as containing learning activity metadata.
    It fills several roles:
         - Parse the XML file to determine the activity's <title> value.
         - Fetch new metadata for this activity from the course_metadata dict.
         - Update metadata in the XML file for 3 key tags: <available_at>,
           <due_at>, and <lock_at>.
    """
    
    global course_metadata, undefined_activities
    
    # Open the XML file and instantiate Beautiful Soup parsing.
    xml_file = open(abs_path_to_file, mode = "rt+", encoding = "utf-8")
    
    # Snag the first line, which contains the good-practice XML declaration.
    # Beautiful Soup erases it.
    xml_declaration = xml_file.readline()
    raw_xml = xml_file.read()
    soup = BeautifulSoup(raw_xml, "xml")
    
    # Get the learning activity's title from the previous semester. Use it to
    # look up the new metadata, which is stored as a subdict in the dictionary.
    # If no such entry is found, add it to a list (undefined_acts) to be
    # returned and ultimately printed to the user.
    prev_title = soup.title.string
    try:
        new_metadata = course_metadata[prev_title]
    except KeyError:
        undefined_activities.append(prev_title)
        return
    
    # If an modified title is specified, update it. Otherwise keep the previous
    # title.
    if new_metadata["new_title"]:
        soup.title.string = new_metadata["new_title"]
    else:
        pass
    
    # If new available, due, or lock times are specified, update them.
    # If not, delete the times that were copied over from the previous
    # semester.
    if new_metadata["new_avail_datetime"]:
        unlock_at_str = format_datetime(new_metadata["new_avail_datetime"])
    else:
        unlock_at_str = ""
        
    if new_metadata["new_due_datetime"]:
        due_at_str = format_datetime(new_metadata["new_due_datetime"])
    else:
        due_at_str = ""

    if new_metadata["new_lock_datetime"]:
        lock_at_str = format_datetime(new_metadata["new_lock_datetime"])
    else:
        lock_at_str = ""

    # Update the XML tags with new values.
    soup.unlock_at.string = unlock_at_str
    soup.due_at.string = due_at_str
    soup.lock_at.string = lock_at_str
    
    # Write the updated XML back to the file. Note that, weirdly, the soup
    # object is a list that always contains exactly 1 entry -- that is, 
    # a "tag" object containing updated XML code. Need to convert it to string.
    xml_file.truncate(0)
    xml_file.seek(0)
    # Give the XML declaration back.
    xml_file.write(xml_declaration)
    xml_file.write(str(soup.contents[0]))
    xml_file.close()
    
    return

    
def update_manager():
    """
    This function is executed after the user clicks the "update my course"
    and after the gui_check_ready() function confirms the requirements have
    been met.
    It manages the course updating process, calling the other non-user-facing
    functions as needed.
    """
    
    global course_metadata, undefined_activities
    
    # Unpack the contents of the previous semester's exported course cartridge.
    extract_prev_course()
    
    # Call the find_activities() function to copy the previous semester's course
    # data and generate a list of subdirectories (absolute paths) that contain
    # learning activities.
    activity_subdirs = find_activities()

    # Call the extract_metadata() function to read new syllabus information from
    # the new syllabus Excel file into the course_metadata dictionary.
    course_metadata = extract_metadata()

    # Use counters to track how many activities have been processed.
    # The undefined_activities list will capture any old learning activities
    # that cannot be exactly matched in new_syllabus.xlsx.
    modified_counts = 0
    undefined_activities = []

    # Update the progress window with the status. 
    msg_update_meta = "Updating the new course according to the syllabus."
    gui_progress_update(msg_update_meta)
    
    # Iterate over all the subdirectories containing learning activities.
    for subdir in activity_subdirs:
    
        # Check for metadata XML files. If present, call the update_file_meta()
        # function to replace titles, due dates, etc., with the user
        # specifications.
        meta_file_list = ["assignment_settings.xml", "assessment_meta.xml"]
        for meta_file in meta_file_list:
            if meta_file in os.listdir(subdir):
                update_file_meta(subdir + "/" + meta_file)
                modified_counts += 1
            else:
                pass
        
    # Compress the new_course folder into a .imscc (standard zip) file ready
    # to be uploaded to the LMS.
    compress_new_course()

    # For the sake of good housekeeping, delete the two directories we made.
    rmtree(filepath_root + "old_course", ignore_errors = True)
    rmtree(filepath_root + "new_course", ignore_errors = True)

    # Print a message alerting the user if any learning activities were found
    # that could not be matched to the new syllabus.
    if len(undefined_activities) > 0:
        undefined_activities.sort()
        
        msg_undef_act = """
        Found _{}_ learning activities in the old course data that were not
        defined in the syllabus.
        These were included in the new Common Cartridge file without modification:"""
        gui_progress_update(msg_undef_act.format(len(undefined_activities)))
      
        for unmatched_activity in undefined_activities:
            msg_undef_list = "\t" + unmatched_activity
            gui_progress_update(msg_undef_list,
                                leading_lbs = 1,
                                
                                cleanup = False)

    # Update the progress window to indicate that everything is done.
    msg_complete = """
    Migration complete. Your updated course was saved at the file location
    shown in the main window.
    
    It is ready to be uploaded to your LMS.
    
    Be sure to review the status messages above for any potential errors.
    
    You may now close the program.
    
    Thanks for using LMS Migrator. Have a nice life."""
    gui_progress_update(msg_complete)



# ==== BEGIN DEFINING GUI-RELATED FUNCTIONS ==== 
# The functions in this section are ancillary to the under-the-hood operation
# of LMS Migrator. 
# They operate the GUI.

def gui_build_layout():
    """
    This GUI-related function builds the main program window. It is called
    to initiate the GUI.
    """
    
    global ent_old, ent_new, ent_syl, bkup_conf, version
    
    # Build the root window. Resize it and give it a title.
    root = tk.Tk()
    #root.geometry("700x100")
    root.title("LMS Migrator " + version)

    # Add a selector for the old course .IMSCC file.
    # It consists of a button that lauches an 'open' window, and a label
    # that displays the currently selected path.
    frm_oldcourse = tk.Frame()

    btn_old = tk.Button(
                    master = frm_oldcourse,
                    width = 20,
                    text = "Select prior course",
                    command = gui_pick_source
                    )                                
    btn_old.pack(side = "left")

    ent_old = tk.Entry(
                  master = frm_oldcourse,
                  width = 75)
                  
    ent_old.pack(side = "left")

    frm_oldcourse.pack()
    
    # Add a selector for the new syllabus Excel file.
    # It consists of a button that lauches an 'open' window, and a label
    # that displays the currently selected path.
    frm_syl = tk.Frame()

    btn_syl = tk.Button(
                    master = frm_syl,
                    width = 20,
                    text = "Select Excel syllabus",
                    command = gui_pick_syllabus
                    )                                
    btn_syl.pack(side = "left")

    ent_syl = tk.Entry(
                  master = frm_syl,
                  width = 75)
                  
    ent_syl.pack(side = "left")

    frm_syl.pack()
    
    # Add a selector for the new course .IMSCC file.
    # It consists of a button that lauches an 'save' window, and a label
    # that displays the currently selected path.
    frm_newcourse = tk.Frame()

    btn_new = tk.Button(
                    master = frm_newcourse,
                    width = 20,
                    text = "Save new course to...",
                    command = gui_pick_dest
                    )                                
    btn_new.pack(side = "left")

    ent_new = tk.Entry(
                  master = frm_newcourse,
                  width = 75)
                  
    ent_new.pack(side = "left")

    frm_newcourse.pack()
    
    # Add a checkbox for users to confirm their local Common Cartridge file
    # is backed up somewhere. Then a "go!" button.
    frm_validation = tk.Frame()
    
    bkup_conf = tk.IntVar()
    bkup_box = tk.Checkbutton(master = frm_validation,
                text = "I have a backup copy of my Common Cartridge file.",
                variable = bkup_conf
                )
    bkup_box.pack()
    
    btn_run = tk.Button(
                        master = frm_validation,
                        width = 20,
                        text = "Update my course!",
                        command = gui_check_ready
                        )
    btn_run.pack()
    
    frm_validation.pack()

    return root


def gui_check_ready():
    """
    This GUI-related function is called when a user clicks on the "Update
    my course!" button.
    It ensures that the user has marked the checkbox indicating that they
    have a backup of their old course files. It also confirms that both
    source and destination .imscc file paths have been selected. (It does
    not, however, verify the paths -- only that a value is present.)
    """
    
    global bkup_conf, filepath_old, filepath_new, filepath_syl
    
    if bkup_conf.get() == 0:
        # Uh-oh. A backup might not be present. Warn the user.
        warn1_txt = """Hold up a second.
        
        Please make sure you have a backup of your old course data,
        either on your local computer (for example, as
        old_course_backup.imscc), or that it's still available for you
        to download again from your LMS.
        
        On the off chance that something goes wrong here, you don't want
        to lose all your old course content!"""
        
        gui_warn(warn1_txt)
        return
        
    elif (
          not filepath_old
          or not filepath_new
          or not filepath_syl
          or filepath_old == filepath_new
         ):
        # Uh-oh. One or more file paths are missing. That won't do.
        warn2_txt = """Hold up a second.
        
        Please make sure you've selected all three required files:
         * the prior term's Common Cartridge file to duplicate.
         * the syllabus.
         * the new term's Common Cartridge file to save.
        """

        gui_warn(warn2_txt)
        return

    else:
        # The user confirmed they've backed up their files, and file paths
        # for the old course and new course IMSCC files have been entered.
        # It's time to open the progress window & run the updater.
        gui_progress_start()
        
        msg_start = "Starting to update the course. Please be patient."
        gui_progress_update(msg_start)
        
        update_manager()
    
    return


def gui_pick_dest():
    """
    This GUI-related function is called when a user clicks the button to
    select where the new, modified .imscc file should be saved.
    """
    
    global filepath_old
    global filepath_new
    global ent_old
    
    filepath_new = filedialog.asksaveasfilename(
        title = "Save the new Common Cartridge file",
        filetypes = (("Common Cartridge files", "*.imscc"),)
        )
    ent_new.delete(0, tk.END)    
    ent_new.insert(0, filepath_new)
    
    return


def gui_pick_source():
    """
    This GUI-related function is called when a user clicks the button to
    select the previous term's .imscc file.
    It opens the 'open file' dialog box. Once a file is selected, it also
    updates the file path that is displayed in the GUI, and it suggests
    that the new modified file be named new_course.imscc in the same path.
    """

    global filepath_old
    global filepath_root
    global filepath_new
    global ent_old
    
    filepath_old = filedialog.askopenfilename(
        title = "Select the prior Common Cartridge file",
        filetypes = (("Common Cartridge files", "*.imscc"),)
        )
    ent_old.delete(0, tk.END)
    ent_old.insert(0, filepath_old)
    
    filepath_root = filepath_old[:filepath_old.rfind("/")+1]
    filepath_new = filepath_root + "new_course.imscc"
    ent_new.delete(0, tk.END)
    ent_new.insert(0, filepath_new)
    
    return


def gui_pick_syllabus():
    """
    This GUI-related function is called when a user clicks the button to
    select the new Excel syllabus file.
    It opens the 'open file' dialog box. Once a file is selected, it also
    updates the file path that is displayed in the GUI.
    """

    global filepath_syl
    global ent_syl
    
    filepath_syl = filedialog.askopenfilename(
        title = "Select the new syllabus",
        filetypes = (("Microsoft Excel files", "*.xlsx"),)
        )
    ent_syl.delete(0, tk.END)
    ent_syl.insert(0, filepath_syl)

    return


def gui_progress_start():
    """
    This function creates a pop-up progress window.
    A
    """

    global progress_msgs, progress_win
    
    # Create the progress window
    progress_win = tk.Tk()
    progress_win.title("Migration progress...")
    progress_win.geometry("300x500")
    
    progress_msgs = st.ScrolledText(master = progress_win, wrap = tk.WORD)
    
    # Keep the progress window as read-only.
    progress_msgs.configure(state = "disabled")
    
    progress_msgs.pack(side = "top", fill = tk.BOTH, expand = True)
    
    # Here, we need to use win.update() instead of win.mainloop(), as the latter
    # will prevent the remainder of the migration startup code from executing.
    progress_win.update()

    return
    
    
def gui_progress_update(message, leading_lbs = 2, cleanup = True):
    """
    This GUI-related function updates the pop-up progress window with
    various messages generated by other functions as the course content
    is migrated & updated.
    It accepts the message to print (a string). Optionally, it also accepts
    the number of leading line breaks to insert before the message,
    (an integer, default 2). Finally, it also accepts the optional cleanup
    parameter to remove tabs, line breaks, etc.
    """
    
    global progress_msgs, progress_win
    # Toggle the progress window to writable, print the message, and toggle
    # back to read-only.
    progress_msgs.configure(state = "normal")
    for count in range (0, leading_lbs):
        progress_msgs.insert(tk.INSERT, "\n")
    
    # Logic for built-in cleanup of tabs, line breaks, etc.
    if cleanup:
        progress_msgs.insert(tk.INSERT, cleandoc(message))
    else:
        progress_msgs.insert(tk.INSERT, message)
        
    progress_msgs.configure(state = "disabled")
    
    progress_win.update()
    
    return
    

def gui_warn(warning):
    """
    This GUI-related function is called to issue a pop-up warning window
    to the user.
    It accepts the warning message to display (a string).
    """
    
    warn_window = tk.Tk()
    warn_window.title("Slow your roll.")
    warn_window.geometry("400x200")
    
    msg_warn = tk.Message(master = warn_window, text = cleandoc(warning))
    
    msg_warn.pack(expand = True)
    warn_window.mainloop()
    
    return



# The following code is executed immediately upon calling lms_migrator.py

filepath_old, filepath_new, filepath_syl = None, None, None

root_window = gui_build_layout()
root_window.mainloop()
