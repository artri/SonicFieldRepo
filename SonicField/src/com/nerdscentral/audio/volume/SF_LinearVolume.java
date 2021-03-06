/* For Copyright and License see LICENSE.txt and COPYING.txt in the root directory */
package com.nerdscentral.audio.volume;

import java.util.List;

import com.nerdscentral.audio.core.SFSignal;
import com.nerdscentral.audio.core.SFSingleTranslator;
import com.nerdscentral.sython.Caster;
import com.nerdscentral.sython.SFPL_Operator;
import com.nerdscentral.sython.SFPL_RuntimeException;

/**
 * ?s1,-3:sf.ExponentialVolume !s1_normal... forwards an SFData less 3 db ...
 * 
 * @author AlexTu
 * 
 */

public class SF_LinearVolume implements SFPL_Operator
{
    public static class Translator extends SFSingleTranslator
    {

        private final double volumeInner;

        Translator(SFSignal input, double volumeIn)
        {
            super(input);
            volumeInner = volumeIn;
        }

        @Override
        public double getSample(int index)
        {
            return getInputSample(index) * volumeInner;
        }

    }

    /**
     * 
     */
    private static final long serialVersionUID = 1L;

    @Override
    public Object Interpret(final Object input) throws SFPL_RuntimeException
    {
        List<Object> inList = Caster.makeBunch(input);
        SFSignal data = Caster.makeSFSignal(inList.get(0));
        double scale = Caster.makeDouble(inList.get(1));
        return new Translator(data, scale);
    }

    @Override
    public String Word()
    {
        return Messages.getString("SF_LinearVolume.0"); //$NON-NLS-1$
    }

}