import mega_util

class MegaUtil:
    @staticmethod
    def export_directory(email, password, directory, megacmd=None, save=None):
        return mega_util.export_dir(email, password, directory, megacmd, save)

    @staticmethod
    def direct_download(megalink, savedir, chromedriverpath, options=None):
        return mega_util.direct_dl(megalink, savedir, chromedriverpath, options)