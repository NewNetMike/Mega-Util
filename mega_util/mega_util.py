import mega_util


class MegaUtil:
    @staticmethod
    def export_directory(email, password, directory, megacmd=None):
        mega_util.export_dir(email, password, directory, megacmd)

    @staticmethod
    def direct_download():
        mega_util.direct_dl()