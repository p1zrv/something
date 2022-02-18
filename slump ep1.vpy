from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
import vapoursynth as vs
import atomchtools as at
import havsfunc
import rekt
import kagefunc


source = core.dgdecodenv.DGSource(r"ep1.dgi").std.Trim(0,44277)
source = core.std.Crop(source,6,0,0,0)
source = rekt.rektlvls(source,colnum=[0,1,711,712,713],colval=[-4,10,10,-5,5])
tivted = core.tivtc.TFM(source)
tivted = core.tivtc.TDecimate(tivted)

maa = havsfunc.santiag(tivted, fw=tivted.width*2, fh=tivted.height*2, nsize=0, nns=4, qual=2)
maa = core.resize.Spline36(maa, tivted.width, tivted.height)

def smthfunc(clip: vs.VideoNode) -> vs.VideoNode:
    clip16 = core.fmtc.bitdepth(clip, bits=16)
    debl = havsfunc.Deblock_QED(clip16, quant1=18, quant2=20, aOff1=1, bOff1=2, aOff2=1, bOff2=2, uv=3)
    dft = core.dfttest.DFTTest(debl, sigma=3, tbsize=3, opt=3, planes=[0,1,2])
    addgra = kagefunc.adaptive_grain(dft, 0.4, luma_scaling=16)
    Mask = at.retinex_edgemask(clip16, sigma=0.7, draft=False, opencl=True)
    filtered = core.std.MaskedMerge(addgra, clip16, Mask, planes=[0,1,2], first_plane=True)
    clip_dendeb = core.fmtc.bitdepth(filtered, bits=10)
    return clip_dendeb

smthfilter = smthfunc(maa)
smthfilter.set_output()

# tivted.set_output(1)
# maa.set_output(2)
# smthfilter.set_output(3)
# source.set_output(8)
# source1.set_output(9)
