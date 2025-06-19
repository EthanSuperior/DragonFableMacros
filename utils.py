from api_lib import API


class UTILS:
    @staticmethod
    def ToRatio(area):
        pos = API.WindowPosition()
        reg = API.GetGameSize()
        convert = lambda i, val: (val - (reg[i % 2] + pos[i % 2])) / (reg[i % 2 + 2] - reg[i % 2])
        return tuple(round(convert(i, val), 3) for i, val in enumerate(area))

    @staticmethod
    def ToAbsolute(ratio):
        pos = API.WindowPosition()
        reg = API.GetGameSize()
        convert = lambda i, val: pos[i % 2] + reg[i % 2] + val * (reg[i % 2 + 2] - reg[i % 2])
        return tuple(round(convert(i, val)) for i, val in enumerate(ratio))

    @staticmethod
    def ToRelative(ratio):
        reg = API.GetGameSize()
        convert = lambda i, val: reg[i % 2] + val * (reg[i % 2 + 2] - reg[i % 2])
        return tuple(round(convert(i, val)) for i, val in enumerate(ratio))

    @staticmethod
    def MidPt(area):
        if len(area) == 2:
            return round(area[0] + ((area[1] - area[0]) / 2), 3)
        return (
            round(area[0] + (area[2] - area[0]) / 2, 3),
            round(area[1] + (area[3] - area[1]) / 2, 3),
        )

    @staticmethod
    def OrientateArea(area):
        return (
            min(area[0], area[2]),
            min(area[1], area[3]),
            max(area[0], area[2]),
            max(area[1], area[3]),
        )

    @staticmethod
    def EvenOutArea(area):
        cX, cY = UTILS.MidPt(area)
        xDi = max(cX - area[0], area[2] - cX)
        yDi = max(cY - area[1], area[3] - cY)
        return round(cX - xDi, 3), round(cY - yDi, 3), round(cX + xDi, 3), round(cY + yDi, 3)

    @staticmethod
    def EnsureList(paths):
        return [paths] if isinstance(paths, str) else list(paths)

    @staticmethod
    def AreaFromPath(path):
        coords_str = path.split("#")[-1].split(")")[0].strip("(")
        return tuple(map(float, coords_str.split(",")))

    @staticmethod
    def AddBuffer(area, padding):
        return (
            max(0.0, area[0] - padding),
            max(0.0, area[1] - padding),
            min(1.0, area[2] + padding),
            min(1.0, area[3] + padding),
        )

    @staticmethod
    def GetSize(area):
        return (area[2] - area[0]), (area[3] - area[1])
