class App(object):

    def __init__(self, app_path):
        assert app_path is not None
        self.app_path = app_path

        from androguard.core.bytecodes.apk import APK
        self.apk = APK(self.app_path)
        self.package_name = self.apk.get_package()
        self.main_activity = self.apk.get_main_activity()
        self.permissions = self.apk.get_permissions()
        self.activities = self.apk.get_activities()
        self.app_name = self.apk.get_app_name()
        print("Main activity:"+self.main_activity)
        print("Package name:"+self.package_name)

