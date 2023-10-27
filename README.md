# Replication Package

This repository contains all the artifacts (including the source code of PBFDroid, the APK files of all app subjects, and the defined DMF specifications for all app subjects) in our study.

## Directory Structure

    home
       |
       |--- code:                           The source code of PBFDroid
           |
           |--- start.py:                       The entry of PBFDroid, which accepts the tool parameters
           |--- fuzzing.py:                     The main module of our property-based fuzzing approach
           |--- record.py:                      The main module of DMF instantiator
           |
       |--- app:                            The apk files of 17 open source apps used in our experiment
       |--- dmf:                            The defined DMF specifications for all the apps
       |

## PBFDroid

PBFDroid is an automated GUI testing tool to support the application of our property-based fuzzing approach, which can effectively find data manipulation errors.


### Download

```
git clone https://github.com/property-based-fuzzing/home.git
```

### Environment

If your system has the following support, you can directly run PBFDroid 
- Android SDK: API 26+
- Python 3.7
We use some python libraries, you can install them as prompted, for example:
```
pip install langid
```
You need to create an emulator before running PBFDroid. See [this link](https://stackoverflow.com/questions/43275238/how-to-set-system-images-path-when-creating-an-android-avd) to find out how to create avd using [avdmanager](https://developer.android.com/studio/command-line/avdmanager).
The following sample command illustrates how to create an emulator：
```
sdkmanager "system-images;android-26;google_apis;x86"
avdmanager create avd --force --name Android8.0 --package 'system-images;android-26;google_apis;x86' --abi google_apis/x86 --sdcard 512M --device "pixel_xl"
```
Next, you can start an emulator with the following commands:
```
emulator -avd Android8.0 -read-only -port 5554 
```

### Run

#### Detect DMEs ([video tutorial](https://1drv.ms/f/s!AinXMMnLw-UDmWB_83VqFoaMWVzu?e=POiJTf))
If you have downloaded our project and configured the environment, you only need to enter "download_path/home" to execute our sample app with the following command:
```
python code/start.py -app_path app/anymemo.apk -json_name _anymemo -device_serial emulator-5554 -root_path download_path/home -choice 1 -event_num 400 -max_time 57600 -result_path output
```
Here, 
* `-app_path` path of the app under test (AUT). 
* `-json_name` name of the folder that stores the AUT's DMFs
* `-root_path` up-level directory of the folder that stores all DMFs
* `-choice` 1: run property-based fuzzing to detect DMEs, 2: record DMFs
* `-event_num` number of events in each test
* `-max_time` allocates the running time of PBFDroid (in seconds)

#### Record DMF ([video tutorial](https://1drv.ms/f/s!AinXMMnLw-UDmWB_83VqFoaMWVzu?e=POiJTf))
You can start the DMF instantiator module for defining DMF with the following command:
```
python code/start.py -root_path dmf/ -choice 2 -app_path app/APPNAME.apk -json_name _activitydiary -device_serial emulator-5554
```

### User manual

Before conducting user study, we created a user manual for PBFDroid, you can find it [here](https://sy8pzmhmun.feishu.cn/docx/EIEsdCDFKoBIz1x17uuc2DyqnNc?from=from_copylink)).
