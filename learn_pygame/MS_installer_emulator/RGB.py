from random import choice
import copy
from string import printable


def random_MS_RGB() -> tuple:
    """return a random MicroSoft(R) style color"""
    return choice([
        # 微软logo
        (0xF6, 0x53, 0x14),  # 红
        (0x7C, 0xBB, 0x00),  # 绿
        (0x00, 0xA1, 0xF1),  # 蓝
        (0xFF, 0xBB, 0x00),  # 黄
        # 主页
        (0xE5, 0x14, 0x00),  # 亮红
        (0xBA, 0x14, 0x1A),  # 暗红
        (0xEC, 0x00, 0x8C),  # 粉
        # 微软产品
        (0x00, 0xA0, 0xE9),  # Skype蓝
        (0xF7, 0xAF, 0x32),  # Bing黄
        (0x68, 0x21, 0x7A),  # VS紫
        (0x76, 0xB7, 0x00),  # Xbox绿
        (0x00, 0xBC, 0xF2),  # Windows蓝
        (0x00, 0xCC, 0xFF),  # Windows主页按钮
        (0xEB, 0x3C, 0x00),  # Office红
        (0x00, 0x18, 0x8F),  # Word蓝
        (0x00, 0x72, 0x33),  # Excel绿
        (0xDD, 0x59, 0x00),  # PPT橙
        (0x69, 0x22, 0x7B),  # OneNote紫
        (0x00, 0x72, 0xC6),  # Outlook蓝
    ])


class SequentialText(object):
    @classmethod
    def calculate_string_length(cls, str) -> float:
        _counter = 0
        for c in str:
            if c in printable:
                _counter += 1
            else:
                _counter += 2
        return _counter / 2

    L = [
        "青，出于蓝而胜于蓝。冰，水为之而寒于水。",
        "windows 正在更新，请勿关闭计算机。",
        "嗨，别来无恙啊！",
        "一切即将准备就绪",
        "这可能需要几分钟",
        "我们希望一切准备就绪。",



    ]

    def __init__(self):
        mapped_L = list(map(lambda x: (x, self.calculate_string_length(x)), self.L))

        def _():
            i = 0
            length = len(mapped_L)
            while True:
                if i == length:
                    i = 0
                yield mapped_L[i]
                i += 1

        self._f = _()

    def next(self) -> tuple:
        """return sequential text."""
        return self._f.__next__()


class _Counter(object):
    """step counter
        :param num_change:
    """

    def __init__(self, num_change):
        self._step = self._max_step = num_change

    def next(self, *args, **kwargs):
        if self._step == self._max_step:
            self._max_step_callback()
            self._step = 0
        self._step += 1
        return self._step_callback(*args, **kwargs)

    def _step_callback(self, *args, **kwargs):
        raise NotImplementedError()

    def _max_step_callback(self):
        raise NotImplementedError()


_current_target_bgc = None
_current_bgc = None
_bgc_steps = None


class ProgressiveBackgroundColor(_Counter):
    def __init__(self, num_change):
        super().__init__(num_change)
        self._current_color = random_MS_RGB()
        self._target_color = random_MS_RGB()

        # tell foreground how may steps per bgc change
        global _bgc_steps
        _bgc_steps = num_change
        # end

    def _step_callback(self):
        return self._f.__next__()

    def _max_step_callback(self):
        self._f = self._()
        self._current_color = self._target_color
        self._target_color = random_MS_RGB()

        # tell foreground the current bgc and the target bgd
        global _current_target_bgc, _current_bgc
        _current_bgc = copy.deepcopy(self._current_color)
        _current_target_bgc = copy.deepcopy(self._target_color)
        # end

    def _(self):
        for x in range(self._max_step):
            y = [-1, -1, -1]
            for i in range(3):
                ai = self._current_color[i]
                ki = (self._target_color[i] - self._current_color[i]) / self._max_step
                y[i] = int(ai + ki * x)
            yield y


class ProgressiveForegroundFontParams(_Counter):
    def __init__(self, num_change: int, screen_resolution: tuple, character_size: int):
        super().__init__(num_change)
        # color parameters configuration
        self._C_start = None
        self._C_max = (255, 255, 255)
        self._C_end = None
        self._S1 = int(self._max_step / 8 * 1)
        self._S2 = int(self._max_step / 8 * 6)  # self._S2 must be greater than the total frames(*max_step*) in bgc!!!
        self._S3 = int(self._max_step / 8 * 6.5)
        # font position parameters configuration
        self._character_size = character_size
        self._screen_resolution = screen_resolution

        self._text_generator = SequentialText()
        self._param_dict = {
            "color": None,
            "pos": None,
            "text": None,
            "disappear": None
        }

    def _step_callback(self, *args, **kwargs):
        self._step_callback_params = args
        return self._f.__next__()

    def _max_step_callback(self):
        self._f = self._()
        self._param_dict["text"] = self._text_generator.next()

    def _(self):
        y = self._param_dict["color"] = [-1, -1, -1]

        for x in range(0, self._max_step):
            # set color
            if x < self._S1:
                if x == 0:
                    self._C_start = self._step_callback_params[0]
                for i in range(3):
                    y[i] = ((self._C_max[i] - self._C_start[i]) / self._S1) * x + self._C_start[i]
            elif x < self._S2:
                for i in range(3):
                    y[i] = self._C_max[i]
            elif x == self._S2:
                target = [-1, -1, -1]
                ratio = ((self._max_step - _bgc_steps) - (self._max_step - self._S3)) / _bgc_steps
                for i in range(3):
                    distance = _current_target_bgc[i] - _current_bgc[i]
                    bias = distance * ratio
                    target[i] = bias + _current_bgc[i]
                    target[i] = int(target[i])
                self._C_end = tuple(target)
            elif x < self._S3:
                for i in range(3):
                    y[i] = ((self._C_max[i] - self._C_end[i]) / (self._S2 - self._S3)) * x + self._C_max[i] - \
                           self._S2 * ((self._C_max[i] - self._C_end[i]) / (self._S2 - self._S3))

            # set x_pos
            num_char_left = int(self._screen_resolution[0] / self._character_size) - self._param_dict["text"][1]
            self._param_dict["pos"] = (
                int(num_char_left / 2 * self._character_size),
                int(self._screen_resolution[1] / 2 - self._character_size * 0.7)
            )

            # set disappear
            self._param_dict["disappear"] = True if x > self._S3 else False

            # return values
            yield self._param_dict
