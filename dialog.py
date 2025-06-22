import os
import time
from gui_lib import GUI
from utils import UTILS
from glob import glob


# TODO ADD SUB DIALOGS!!!!
class _DialogImageAction:
    def __init__(self, owner, key):
        self.owner = owner
        self.key = str(key).lower()

    def __call__(self, *args, **kwargs):
        return self.owner.Action(self.key, *args, **kwargs)

    def __bool__(self):
        item = self.owner[self.key]
        return GUI.CheckImage(item) if item else False


class Dialog:
    def __init__(self, folder_dir: str, yes=None, no=None, close=None, aliases=None, parent=None):
        self._imgs = {}
        self._dialogs = {}
        self.parent = parent
        self.src = folder_dir
        if aliases is None:
            aliases = {}
        # print("" if parent is None else "\t", folder_dir)
        for filename in glob(f"{folder_dir}/*"):
            if os.path.isdir(filename):
                self[filename.split("\\")[-1].split("/")[-1]] = Dialog(filename, parent=self)
            elif filename.endswith(".png"):
                self[UTILS.ImgIdentifier(filename.split("#")[0])] = filename
        if yes:
            self._imgs["yes"] = self._imgs[yes]
        if no:
            self._imgs["no"] = self._imgs[no]
        if close:
            self._imgs["close"] = self._imgs[close]

        try:
            with open(f"{folder_dir}/aliases.txt", "r") as f:
                for line in f.readlines():
                    key, vals = line.split(":")
                    if key.lower() not in aliases:
                        aliases[key.lower()] = []
                    aliases[key.lower()].extend(vals[1:].strip().split())
        except FileNotFoundError:
            pass  # No 'aliasses' file found, skip it
        if aliases and isinstance(aliases, dict):
            for key, vals in aliases.items():
                key = key.lower()
                for val in [vals] if isinstance(vals, str) else list(vals):
                    val = val.strip().strip(",").lower()
                    self[val] = self[key]
        # TODO: If we are missing an 'in' option, maybe just treat it as a collection of images; howabout that?
        if "in" not in self._imgs:
            print(f"Dialog {folder_dir} missing 'in', you must add an in image or alias")

        # Assign Default Aliases: Close defaults to 1st Yes then No; Yes and No deafult to close
        if "close" not in self._imgs:
            if "yes" in self._imgs:
                self._imgs["close"] = self._imgs["yes"]
            elif "no" in self._imgs:
                self._imgs["close"] = self._imgs["no"]
        if "close" in self._imgs:
            if "yes" not in self._imgs:
                self._imgs["yes"] = self._imgs["close"]
            if "no" not in self._imgs:
                self._imgs["no"] = self._imgs["close"]

    def __bool__(self):
        return GUI.CheckImage(self["in"]) if self["in"] else False

    def __getattr__(self, name):
        if name.lower() in self._imgs:
            return _DialogImageAction(self, name)
        if name.lower() in self._dialogs:
            return self._dialogs[name.lower()]
        raise AttributeError(f"No option for '{name}', add the image or check your spelling")

    def Click(self, key, timeout=3, interval=0.01):
        self.Open()
        return GUI.ClickIf(self[key], timeout=timeout, interval=interval)

    def Action(self, name, close=True):
        self.Click(name)
        if close:
            self.Close()

    def _ActUntilInIs(self, val, act):
        # Wait until 'in' is val; clicking 'act' while we wait...
        startT = time.time()
        while time.time() - startT <= 3:
            if bool(self) == val:
                return True
            if GUI.CheckImage(self[act]):
                GUI.MouseClick(UTILS.MidPt(UTILS.AreaFromPath(self[act])))
                time.sleep(0.01)
            time.sleep(0.01)
        return GUI.CheckImage(self["in"]) == val

    def Open(self, recursive=True):
        if recursive and self.parent is not None and not GUI.CheckImage(self["in"]):
            self.parent.Open()
        return self._ActUntilInIs(True, "open")

    def Close(self, recursive=True):
        if recursive and self.parent is not None and GUI.CheckImage(self["in"]):
            return self._ActUntilInIs(False, "close") and self.parent.Close()
        return self._ActUntilInIs(False, "close")

    def Await(self):
        GUI.AwaitImg(self["in"])
        return self

    def __getitem__(self, key):
        # print(key, self._dialogs.keys(), self._imgs.keys())
        if str(key).lower() in self._dialogs:
            return self._dialogs[str(key).lower()]
        return self._imgs.get(str(key).lower(), "")

    def __setitem__(self, key, value):
        if isinstance(value, Dialog):
            # print(f"{'\t' if self.parent is None else '\t\t'}Dlg: {key} - {value}")
            self._dialogs[str(key).lower()] = value
        else:
            # print(f"{'\t' if self.parent is None else '\t\t'}Img: {key} - {value}")
            self._imgs[str(key).lower()] = value

    def __delitem__(self, key):
        if str(key).lower() in self._dialogs:
            del self._dialogs[str(key).lower()]
        else:
            self._imgs[str(key).lower()]

    def __call__(self, choice=True, *args, **kwds):
        if isinstance(choice, bool):
            return self.Action("yes" if choice else "no", *args, **kwds)
        else:
            return self.Action(choice, *args, **kwds)
