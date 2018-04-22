#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as font_manager

fontpath = '/home/sarah/.fonts/cmunss.ttf'

prop = font_manager.FontProperties(fname=fontpath)
mpl.rcParams['font.family'] = prop.get_name()


# freqdif: 78386968 
niter = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
niter2 = [0, 1, 2, 3]
norm1= [32475928, 25392492, 19320528, 14462173, 11263933, 10371235, 10477612, 10634981, 10760000, 10680567, 10628854, 10559621, 10391489]
norm2= [32475928, 23425132, 28284798, 26716290]
norm3= [32475928, 27446940, 23236344, 20663992, 18737512, 17107040, 15649435, 14493308, 13569843, 12907267, 12425467,12109981, 11745056]
norm1[:] = [x / 10371235.0 for x in norm1]
norm2[:] = [x / 10371235.0 for x in norm2]
norm3[:] = [x / 10371235.0 for x in norm3]
#norm2[:] = [x / 110486663.0 for x in norm2]
#norm3[:] = [x / 110486663.0 for x in norm3]
#norm3[:] = [x / 10069987.0 for x in norm3]

plt.figure(figsize=(9.60,5.40), dpi=1000)
l1 = plt.scatter(niter,norm1)
l2 = plt.scatter(niter2,norm2, marker='x', color='g')
l3 = plt.scatter(niter,norm3, marker='*', color='y')

plt.legend((l1, l2, l3),('Good c','Too large c', 'Too small c'))
plt.plot([-1, 14], [1, 1],'r--')
plt.xlim(-0.2, 12.2)
plt.ylim(0, 3.5)
plt.xlabel("Iterations")
#plt.ylabel(r'$\Vert\mathbf{F}($smoothed$) -  \mathbf{F}($legacy$) \Vert$')
plt.ylabel(r'$\Vert\mathbf{F}(S_R * d_h) -  \mathbf{F}(d_l) \Vert$')


#\Vert \textbf{F}(\text{smoothed}) - \textbf{F}(\text{legacy}) \Vert

#plt.title('"Correct" C')
#plt.title('Convergence')
#plt.savefig('l1l2.pdf', format='pdf', bbox_inches='tight')
plt.savefig('scalar.pdf', format='pdf', bbox_inches='tight')
