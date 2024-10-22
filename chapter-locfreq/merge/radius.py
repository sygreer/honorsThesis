from rsf.proj import *

def radius(high, low,               # initial high and low frequency images
           niter,                   # number of corrections
           c,                       # 'step length' for radius corrections. Can 
                                    #       be type int or float for constant c 
                                    #       or type array for changing c.
           bias=-15, clip=30,       # bias and clip for display
           rect1=40, rect2=80,      # radius for local frequency calculation
           maxrad=1000,             # maximum allowed radius
           theor=True,              # use theoretical smoothing radius
           scale=9,                 # scale for theoretical smoothing radius
           initial=10,              # initial value for contant smoothing radius 
           minval=0, maxval=25,     # min and max local frequency for display
           titlehigh="Hires",
           titlelow="Legacy"):

    if type(c) is float or type(c) is int:
        c = [c]*niter

    # plot image
    def seisplot(name):
        return 'grey title="%s"'%name
    
    # local frequency
    locfreq = '''iphase order=10 rect1=%d rect2=%d hertz=y complex=y | 
                 put label="Frequency" unit=Hz'''%(rect1,rect2)

    def locfreqplot(name):
        return 'grey mean=y color=j scalebar=y title="%s" '%name

    # difference in local frequencies
    freqdif = 'add scale=-1,1 ${SOURCES[1]} | put label=Frequency'

    def freqdifplot(num):
        return '''grey allpos=y color=j scalebar=y mean=y 
                  title="Difference in Local Frequencies %s" 
                  clip=%d bias=%d minval=%d 
                  maxval=%d''' %(num,clip,bias,minval,maxval) 

    # plot spectral content  
    specplot = '''cat axis=2 ${SOURCES[1]} | 
                 scale axis=1 | window max1=180 |
                 graph title="Normalized Spectra" label2="Amplitude" unit2=""'''

    # plot smothing radius
    def rectplot(name):
        return '''grey color=j mean=y title="%s" scalebar=y barlabel=Radius 
                  barunit=samples'''%name

    # smooth with radius
    smooth = 'nsmooth1 rect=${SOURCES[1]}'

    ############################################################################

    # plot images
    Result(high, seisplot(titlehigh))
    Result(low, seisplot(titlelow))

    # initial local frequency
    Flow('high-freq',high,locfreq)
    Result('high-freq',locfreqplot('%s Local Frequency'%titlehigh))

    Flow('low-freq',low,locfreq)
    Result('low-freq',locfreqplot('%s Local Frequency'%titlelow))

    # initial difference in local frequency
    Flow('freqdif','low-freq high-freq',freqdif)
    Result('freqdif',freqdifplot(''))

    # initial smoothing radius
    if (theor):
        from math import pi
        Flow('rect0','low-freq high-freq','''math f1=${SOURCES[1]} 
        output="sqrt(%g*(1/(input*input)-1/(f1*f1)))/%g"'''%(scale,2*pi*0.001))
    else:
        Flow('rect0','low-freq','math output=%f'%initial)

    Result('rect0',rectplot("Smoothing Radius 0"))

    # smoothing using intial smoothing radius guess
    Flow('high-smooth0','%s rect0' % high,smooth)
    Result('high-smooth0', seisplot("%s Smooth 0"%titlehigh))

    # frequency spectra
    Flow('high-spec',high,'spectra all=y')
    Flow('low-spec',low,'spectra all=y')
    Flow('high-smooth-spec0','high-smooth0','spectra all=y')
    Result('nspectra','high-spec low-spec',specplot)
    Result('high-smooth-spec0','high-smooth-spec0 low-spec',specplot)
    
    Flow('high-smooth-freq0','high-smooth0',locfreq)
    Result('high-smooth-freq0',
            locfreqplot("%s Local Frequency Smoothed %d" %(titlehigh,0)))
           
    Flow('freqdif-filt0','low-freq high-smooth-freq0',freqdif) 
    Result('freqdif-filt0',freqdifplot('0')) 

    prog=Program('radius.c') 
    for i in range(1, niter+1): 
        j = i-1

        # update smoothing radius
        Flow('rect%d'%i,'rect%d freqdif-filt%d %s'%(j,j,prog[0]),
             './${SOURCES[2]} freq=${SOURCES[1]} c=%f'%c[j])
        Result('rect%d'%i,rectplot("Smoothing Radius %d")%i)
        
        # smooth image with radius
        Flow('high-smooth%d'%i,'%s rect%d'%(high,i),smooth)
        Result('high-smooth%d'%i, seisplot('%s Smooth %d'%(titlehigh,i)))

        # smoothed spectra
        Flow('high-smooth-spec%d'%i,'high-smooth%d'%i,'spectra all=y')
        Result('high-smooth-spec%d'%i,'high-smooth-spec%d low-spec'%i,specplot)
        
        # smoothed local frequency
        Flow('high-smooth-freq%d'%i,'high-smooth%d'%i,locfreq)
        Result('high-smooth-freq%d'%i,
               locfreqplot('%s Local Frequency Smoothed %d'%(titlehigh,i)))

        # frequency residual
        Flow('freqdif-filt%d'%i,'low-freq high-smooth-freq%d'%i,freqdif)
        Result('freqdif-filt%d'%i,freqdifplot(str(i)))
        
