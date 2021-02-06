# LMS Migrator
A tool for educators. Easily update due dates from previous terms' Common Cartridge file.

## Who is this for?
LMS Migrator is designed for educators who have better things to do than click a million buttons to update their online classrooms.

## What does it do?
LMS Migrator looks for a previous term's course content, which you can export and download from your LMS as a Common Cartridge (.imscc) file.

The script unpacks the contens of your old course, updating basic metadata like assignment names, availability dates, and due dates according to what you specify in a stripped-down syllabus. It then re-bundles the updated course as a new Common Cartridge file, which is ready for you to upload back to your LMS.

It features a simple, user-friendly interface:
![Screenshot of LMS Migrator window on Mac OSX](webassets/osx_1-1-1_screenshot.png?raw=true)

## Is it compatable with my LMS?
Right now, LMS Migrator has only been tested with the [Canvas LMS](https://www.instructure.com/canvas/) using Common Cartridge version 1.1.0. It *ought* to work with other LMS platforms such as [Blackboard](https://www.blackboard.com/teaching-learning/learning-management), too, but it has not been tested yet. **please give LMS Migrator a try using other LMS platforms and [reach out](#reaching-out) to let us know how it works.**

## Installation
Download *lms_migrator.py* and the template *new_syllabus.xlsx* to a directory of your choice on your computer. Make sure that you have Python 3 and the required supporting modules (below) installed, too.

Unfortunately, there is no stand-alone version of LMS Migrator available; it must be executed via Python.

## But really, how do I install it?

The vanilla installation directions above under "Installation" are the bare-basics. Here are some more detailed directions.

1. *Determine if your computer has Python 3 installed.* This will provide the interpreter that's required to run LMS Migrator.
	* You can do that by opening a terminal or command line and typing `python3`, followed by the enter key.
	* If Python isn't installed, you will receive an error message. It may include instructions for installing Python 3 on your computer.
	* If you don't receive an error, that means Python is already on your computer! Simply enter `quit()` to exit out of Python again.
2. *Install the supporting programs.* LMS Migrator requires the help of a few other Python-based tools to work. You can easily install them by copying/pasting the code below into your terminal / command line prompt. To ensure compatability, we'll specify the exact versions of these tools that were used in developing LMS Migrator. If you already have any of these installed, other versions will likely work, too.
```
pip3 install beautifulsoup4==4.9.3 lxml==4.5.0 openpyxl==3.0.5
```
3. *That's it!* If you didn't receive any error messages along the way, you should be all set. See the directions under *How do I use it?* to continue.

## How do I use it?
Make sure the program and its requirements are installed (see [*Installation*](#installation) and [*But really, how do I install it?*](#but-really-how-do-i-install-it).
1. It's recommended to make a new folder on your computer to keep things tidy & make sure your files are safe. You can call it anything you want, but let's use `lms_migrator` for clarity. **Important:** Always back up your course files before using LMS Migrator!
2. Your new folder needs to have two files in it:
	* The Common Cartridge export (.imscc file) from your previous semester's course, which you can download from your LMS.
		* Although you can use any file name you want, it may make your workflow more straightforward to rename the file you download from your LMS to *old_course.imscc*.
		* Not sure how to export your course? Click for directions using [Canvas](https://community.canvaslms.com/t5/Instructor-Guide/How-do-I-export-a-Canvas-course/ta-p/785) or [Blackboard](https://help.blackboard.com/Learn/Administrator/Hosting/Course_Management/Common_Cartridge_Course_Packages#download-the-course-package_OTP-8).
		* If you given a choice, please select "IMS Common Cartridge v 1.1.0"; LMS Migrator has not yet been tested with other versions of the Common Cartridge format.
	* An Excel spreadsheet that contains a simplified syllabus. **Be sure you follow the template that's provided in the `templates` folder above!**
		* Again, although you can use any file name you want, it might make your life easier to use something simple & clear like *new_syllabus.xlsx*.

3. Open a command line / terminal and navigate to the folder `lms_migrator` (or whatever you decided to name it) where LMS Migrator, your syllabus, and the old course materials are stored.
	* For example, if you're using Mac OS X and you downloaded LMS Migrator to a sub-folder on your desktop called `lms_migrator`, you could use the command `cd ~/my-user-name/Desktop/lms_migrator" to navigate to the correct folder. Be sure to replace "my-user-name" with your actual user name.

4. Type the following in exactly, or simply copy/paste it. `python3 lms_migrator.py`

5. Hit enter to run the program. Take note of any messages it displays.

6. Upload the updated Common Cartridge file to your LMS. **Important:** Always double-check that names, due dates, and other parameters were modified the way that you expected.

7. That's it! Feel free to reach out if you have any feedback!

## Didn't there used to be a stand-alone version?

Yes. For a beautiful, fleeting moment, stand-alone versions of LMS Migrator were available for Mac OS X and Ubuntu. However, we've encountered a yet-undetermined glitch between LMS Migrator and Pyinstaller, which was used to package the stand-alone versions of LMS Migrator. Until this bug can be found and resolved, please use the Python script version of LMS Migrator. Sorry for the headache.

## Reaching out
If you find LMS Migrator valuable, or if you're interested in contributing, please reach out to say so. Contact information is listed on [the author's GitHub page](https://github.com/jhirner).
