README.txt

Bolivian Real Estate Web Scraper

Set Up Instructions
1. Install FireFox
	- https://www.mozilla.org/en-US/firefox/new/

2. Install python
	1. Go to https://www.python.org/downloads/release/python-383/
	2. Scroll to the bottom, and choose your installer
	3. Assuming your system is 64-bit, click "Windows x86-64 executable installer"
	4. Open installer, make sure you click "Add Python 3.8 to PATH"
	5. Choose default installation
	6. https://www.youtube.com/watch?v=bnhQBUEpWlg also explains how to do this

3. Add geckodriver to your PATH
	1. Open https://github.com/mozilla/geckodriver/releases/tag/v0.26.0
	2. Scroll down and download the file labeled geckodriver-v#.##.#-win64.zip
	3. Extract the .zip to a desired destination (I have a folder C:\Drivers) 
	4. Copy the address of geckodriver
	5. Open up System Properties
	6. Click the Advanced tab, then select "Environment Variables..."
	7. Click the "Path" variable, and click Edit
	8. Click New and paste geckodriver address, then click OK

4. Open Scraper location and double-click to run scraper_setup.bat
	- Ensure no errors!

5. Create desktop shortcut for Bolivian_RE_Scraper.exe

6. Click Bolivian_RE_Scraper.exe shortcut to run