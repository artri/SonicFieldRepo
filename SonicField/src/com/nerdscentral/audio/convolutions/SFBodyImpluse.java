package com.nerdscentral.audio.convolutions;

import java.util.ArrayList;
import java.util.List;

import com.nerdscentral.audio.SFConstants;
import com.nerdscentral.audio.SFData;
import com.nerdscentral.audio.SFSignal;
import com.nerdscentral.sython.Caster;
import com.nerdscentral.sython.SFPL_Context;
import com.nerdscentral.sython.SFPL_Operator;
import com.nerdscentral.sython.SFPL_RuntimeException;

public abstract class SFBodyImpluse implements SFPL_Operator
{

    private static final long serialVersionUID = 1L;

    abstract double[][] getData();

    public List<Object> getArrays() throws SFPL_RuntimeException
    {
        double[][] arrays = getData();
        int len = arrays[0].length;
        double rate = getRate() / SFConstants.SAMPLE_RATE;
        int outLen = (int) (len * (SFConstants.SAMPLE_RATE) / getRate());
        List<Object> ret = new ArrayList<>();
        for (double[] inData : arrays)
        {
            try (SFSignal signal = SFData.build(outLen); SFSignal in = SFData.build(inData);)
            {
                double pos = 0;
                for (int i = 0; i < outLen; ++i)
                {
                    signal.setSample(i, in.getSampleCubic(pos));
                    pos = pos + rate;
                }
                ret.add(Caster.prep4Ret(signal));
            }
        }
        return ret;
    }

    @SuppressWarnings("static-method")
    protected int getRate()
    {
        return 44100;
    }

    public SFBodyImpluse()
    {
        super();
    }

    @Override
    public Object Interpret(Object input, SFPL_Context context) throws SFPL_RuntimeException
    {
        return getArrays();
    }

}