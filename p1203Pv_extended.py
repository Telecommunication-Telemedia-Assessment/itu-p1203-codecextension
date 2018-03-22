#!/usr/bin/env python3
"""
Copyright 2017-2018 Deutsche Telekom AG, Technische Universität Berlin, Technische
Universität Ilmenau, LM Ericsson

Permission is hereby granted, free of charge, to use the software for research
purposes.

Any other use of the software, including commercial use, merging, publishing,
distributing, sublicensing, and/or selling copies of the Software, is
forbidden. For a commercial license, please contact the respective rights
holders of the standards ITU-T Rec. P.1203, ITU-T Rec. P.1203.1, ITU-T Rec.
P.1203.2, and ITU-T Rec. P.1203.3. See https://www.itu.int/en/ITU-T/ipr/Pages/default.aspx
for more information.

NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY THIS LICENSE.
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
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/itu-p1203/')

from itu_p1203 import log
from itu_p1203 import utils
from itu_p1203.errors import P1203StandaloneError
from itu_p1203.p1203Pv import P1203Pv

logger = log.setup_custom_logger('main')


class P1203Pv_codec_extended(P1203Pv):

    # non-standard codec mapping
    COEFFS_VP9 = [-0.04129014, 0.30953836, 0.32314399, 0.5284358]
    COEFFS_H265 = [-0.05196039, 0.39430046, 0.17486221, 0.50008018]

    def __init__(self, segments, display_res="1920x1080", stream_id=None):
        super().__init__(segments, display_res="1920x1080", stream_id=None)

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

        print({"before": self.o22[-1], "after": score})
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
                logger.warning("Non-standard codec used. O22 Output will not be ITU-T P.1203 compliant.")
            if self.mode != 0 and c != "h264":
                raise P1203StandaloneError("Non-standard codec calculation only possible with Mode 0.")


if __name__ == '__main__':
    print("this is just a module")
