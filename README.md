# PBFDroid

PBFDroid is an automated GUI testing tool to support the application of our property-based fuzzing approach, which can detect data manipulation errors effectively.


### Download

```
git clone https://github.com/functional-fuzzing-android-apps/home.git
```

### Environment

If your system has the following support, you can run PBFDroid normally
- Android SDK: API 26+
- Python 3.7
We use some libraries provided by python, you can add them as prompted, for example:
```
pip install langid
```
You need to create an emulator before running PBFDroid. See [this link](https://stackoverflow.com/questions/43275238/how-to-set-system-images-path-when-creating-an-android-avd) for how to create avd using [avdmanager](https://developer.android.com/studio/command-line/avdmanager).
The following sample command can help you create an emulator, which will help you to start using PBFDroid quickly：
```
sdkmanager "system-images;android-26;google_apis;x86"
avdmanager create avd --force --name Android8.0 --package 'system-images;android-26;google_apis;x86' --abi google_apis/x86 --sdcard 512M --device "pixel_xl"
```
Next, you can start a emulator with the following commands:
```
emulator -avd Android8.0 -read-only -port 5554 
```

### Run

#### Detect DMEs
If you have downloaded our project and configured the environment, you only need to enter "download_path/home" to execute our sample app with the following command:
```
python code/start.py -app_path app/anymemo.apk -json_name _anymemo -device_serial emulator-5554 -root_path download_path/home -choice 1 -testcase_count 50 -event_num 400 -max_time 57600 -result_path output
```

#### Record DMF
You can start the help module for defining DMF with the following command:
```
python code/start.py -root_path dmf/ -choice 2 -app_path app/APPNAME.apk -json_name _activitydiary -device_serial emulator-5554
```

# Directory Structure

    home
       |
       |--- code:                           The source code of PBFDroid
       |--- app:                            Apk files of 12 open source apps used in our experiment
       |--- dmf:                            The folder where the defined DMFs are stored
       |
