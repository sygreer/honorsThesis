#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as font_manager

fontpath = '/home/sarah/.fonts/cmunss.ttf'

prop = font_manager.FontProperties(fname=fontpath)
mpl.rcParams['font.family'] = prop.get_name()


# freqdif: 78386968 
niter = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
#niter = [0, 1, 2, 3, 4, 5]
norm1= [47484892, 33515692, 23253388, 16376629, 11599820, 10069987, 10116965,10258426,10321123,10282613,10289243,10398856,10446601]

#norm2=[78369720,60672360,33617148,20220940,13173313,10842506,10398470,10210745,10296503,10313730,10298821,10204044,10263224,10321556]
norm2=[60672360,33617148,20220940,13173313,10842506,10398470,10210745,10296503,10313730,10298821,10204044,10263224,10321556]
norm3= [32475928, 25392492, 19320528, 14462173, 11263933, 10371235, 10477612, 10634981, 10760000, 10680567, 10628854, 10559621, 10391489]
norm1[:] = [x / 10069987.0 for x in norm1]
norm2[:] = [x / 10069987.0 for x in norm2]
norm3[:] = [x / 10069987.0 for x in norm3]

plt.figure(figsize=(9.60,5.40), dpi=1000)
l1 = plt.scatter(niter,norm1)
l2 = plt.scatter(niter,norm2, marker='x', color='g')
l3 = plt.scatter(niter,norm3, marker='*', color='y')

plt.legend((l1, l2, l3),('Initial = constant 10','Initial = constant 1', 'Initial = theoretical radius'))
plt.plot([-1, 14], [1, 1],'r--')
plt.xlim(-0.2, 12.2)
plt.ylim(0, 6.5)
plt.xlabel("Iterations")
#plt.ylabel(r'$\Vert\mathbf{F}($smoothed$) -  \mathbf{F}($legacy$) \Vert$')
plt.ylabel(r'$\Vert\mathbf{F}(S_R * d_h) -  \mathbf{F}(d_l) \Vert$')


#\Vert \textbf{F}(\text{smoothed}) - \textbf{F}(\text{legacy}) \Vert

#plt.title('"Correct" C')
#plt.title('Convergence')
#plt.savefig('l1l2.pdf', format='pdf', bbox_inches='tight')
plt.savefig('all.pdf', format='pdf', bbox_inches='tight')
