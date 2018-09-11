#!/usr/bin/env python3
"""
Copyright 2018 Technische Universität Ilmenau

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import sys
import os

p1203_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'itu-p1203'))

if os.path.isdir(p1203_path):
    sys.path.insert(0, p1203_path)

from itu_p1203 import log
from itu_p1203 import utils
from itu_p1203.errors import P1203StandaloneError
from itu_p1203.p1203Pv import P1203Pv

logger = log.setup_custom_logger('main')

class P1203Pv_codec_extended(P1203Pv):

    # non-standard codec mapping
    COEFFS_VP9 = [-0.04129014, 0.30953836, 0.32314399, 0.5284358]
    COEFFS_H265 = [-0.05196039, 0.39430046, 0.17486221, 0.50008018]
    _show_warning = True

    def __init__(self, segments, display_res="1920x1080", stream_id=None):
        super().__init__(segments, display_res, stream_id)

    def model_callback(self, output_sample_timestamp, frames):
        super().model_callback(output_sample_timestamp, frames)
        score = self.o22[-1]
        output_sample_index = [i for i, f in enumerate(frames) if f["dts"] < output_sample_timestamp][-1]

        # only get the relevant frames from the chunk
        frames = utils.get_chunk(frames, output_sample_index, type="video")

        # non-standard codec mapping
        codec_list = list(set([f["codec"] for f in frames]))
        if len(codec_list) > 1:
            raise P1203StandaloneError("Codec switching between frames in measurement window detected.")
        elif codec_list[0] != "h264":
            def correction_func(x, a, b, c, d):
                return a * x * x * x + b * x * x + c * x + d
            if codec_list[0] in ["hevc", "h265"]:
                coeffs = self.COEFFS_H265
            elif codec_list[0] == "vp9":
                coeffs = self.COEFFS_VP9
            else:
                logger.error("Unsupported codec in measurement window: {}".format(codec_list[0]))
            # compensate score
            score = max(1, min(correction_func(score, *coeffs), 5))

        # print({"before": self.o22[-1], "after": score})
        self.o22[-1] = score

        self.o22.append(score)

    def check_codec(self):
        """ extends the supported codecs
        """
        codecs = list(set([s["codec"] for s in self.segments]))
        for c in codecs:
            if c not in ["h264", "h265", "hevc", "vp9"]:
                raise P1203StandaloneError("Unsupported codec: {}".format(c))
            elif c != "h264":
                if self._show_warning:
                    logger.warning("Non-standard codec used. O22 Output will not be ITU-T P.1203 compliant.")
            if self.mode != 0 and c != "h264":
                raise P1203StandaloneError("Non-standard codec calculation only possible with Mode 0.")


if __name__ == '__main__':
    print("this is just a module")
