# Codec Extension for ITU-T P.1203
You should clone the official ITU-T P.1203 in this directory:
```
git clone https://github.com/itu-p1203/itu-p1203.git
```

As next step, you should be able to use the extension, with e.g. the `./calculate.py` script in a similar manner like the original itu-p1203 standalone version.


## Non-Standard Codec Mapping

In order to be able to use this software with other codecs than the P.1203-specified H.264, the software implements a custom mapping function for H.265/HEVC and VP9-encoded streams when using Mode 0. **Note:** When using other codecs than H.264, the resulting values will not be compliant to the official standard. In the future, further updates to the mapping function may be supplied by the authors based on more extensive testing.

The proposed mapping uses a third-order polynomial function:

    y = a*x^3 + b*x^2 + c*x + d

where `y` is the compensated MOS and `x` is the original MOS. The coefficients (`a` through `d`) are the following:

    COEFFS_VP9 = [-0.04129014, 0.30953836, 0.32314399, 0.5284358]
    COEFFS_H265 = [-0.05196039, 0.39430046, 0.17486221, 0.50008018]

To derive the function, a set of six 10 s video-only sequences with various spatiotemporal complexity was chosen, encoded at different bitrates (from 200–40000 kBit/s) and resolutions (from 360p to 2160p) with the `libvpx-vp9` and `libx265` encoders. The encoders were set to use two-pass encoding. The quality of each sequence was calculated with [VMAF](https://github.com/Netflix/vmaf) version 0.6.1 and mapped linearly to a MOS scale from 1–5. The mapping was then derived based on averaging the sequence scores; it has an RMSE of < 0.034.

The relationship between the VMAF scores for these clips, averaged over all sources, are shown in the below figure:

![](doc/mapping.png)

## Acknowledgement

If you use this software in your research, you must:

1. Include the link to this repository
2. Cite the following publication:

   A. Raake, M.-N. Garcia, W. Robitza, P. List, S. Göring, and B. Feiten, “A bitstream-based, scalable video-quality model for HTTP adaptive streaming: ITU-T P.1203.1,” in Ninth International Conference on Quality of Multimedia Experience (QoMEX), (Erfurt), 2017.

        @inproceedings{Raake2017,
        address = {Erfurt},
        author = {Raake, Alexander and Garcia, Marie-Neige and Robitza, Werner and List, Peter and Göring, Steve and Feiten, Bernhard},
        booktitle = {Ninth International Conference on Quality of Multimedia Experience (QoMEX)},
        doi = {10.1109/QoMEX.2017.7965631},
        isbn = {978-1-5386-4024-1},
        month = {May},
        publisher = {IEEE},
        title = {{A bitstream-based, scalable video-quality model for HTTP adaptive streaming: ITU-T P.1203.1}},
        url = {http://ieeexplore.ieee.org/document/7965631/},
        year = {2017}
        }

Development of this software has been partly funded by the European Union’s Horizon 2020 research and innovation programme under the Marie Skłodowska-Curie grant agreement No 643072, Project [QoE-Net](http://www.qoenet-itn.eu/).

## License

Copyright 2017-2018 Deutsche Telekom AG, Technische Universität Berlin, Technische Universität Ilmenau, LM Ericsson

Permission is hereby granted, free of charge, to use the software for non-commercial research purposes.

Any other use of the software, including commercial use, merging, publishing, distributing, sublicensing, and/or selling copies of the Software, is forbidden.

For a commercial license, you must contact the respective rights holders of the standards ITU-T Rec. P.1203, ITU-T Rec. P.1203.1, ITU-T Rec. P.1203.2, and ITU-T Rec. P.1203.3. See https://www.itu.int/en/ITU-T/ipr/Pages/default.aspx for more information.

NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY THIS LICENSE. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Authors

Main developers:

* Steve Göring, Technische Universität Ilmenau
* Werner Robitza, Deutsche Telekom AG

Contributors:

* Marie-Neige Garcia, Technische Universität Berlin
* Alexander Raake, Technische Universität Ilmenau
* Marcel Schmalzl, Technische Universität Ilmenau
* Peter List, Deutsche Telekom AG
* Bernhard Feiten, Deutsche Telekom AG
* Ulf Wüstenhagen, Deutsche Telekom AG
* Jörgen Gustafsson, LM Ericsson
* Gunnar Heikkilä, LM Ericsson
* David Lindegren, LM Ericsson
* Junaid Shaikh, LM Ericsson
