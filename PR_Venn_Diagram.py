"""
Venn Diagrams on USPC versus CPC Patents Counts to Illustrate P, R, and F-Scores
Python 3.5, using Marcia's py35 environment.
"""
from matplotlib_venn import venn2, venn2_circles
from matplotlib import pyplot as plt
from pylab import savefig
import numpy as np

#Venn for 2012 Aircraft Power Plant Patents
v=venn2(subsets=(40,31,48), set_labels = ('CPC', 'USPC'))
#Below commented lines came from matplotlib-venn example for venn3. 
#plt.figure(figsize=(4,4))
#v.get_patch_by_id('100').set_alpha(1.0)
#v.get_patch_by_id('100').set_color('white')
#v.get_label_by_id('100').set_text('Unknown')
#v.get_label_by_id('A').set_text('Set "A"')
c = venn2_circles(subsets=(40,31,48), linestyle='dashed')
#c[0].set_lw(1.0)
#c[0].set_ls('dotted')

#I have a problem with location of my annotations. Need help understanding the cooredinates???
#plt.annotate('Total Patents Found\nUsing CPC = 88', xy=v.get_label_by_id('100').get_position() - np.array([0, 0.2]), xytext=(-70,-70),
#             ha='center', textcoords='offset points', bbox=dict(boxstyle='round,pad=0.5', fc='gray', alpha=0.1),
#             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5',color='gray'))
#plt.annotate('Total Patents Found\nUsing USPC = 79', xy=v.get_label_by_id('100').get_position() - np.array([-1.0, 0.2]), xytext=(70,-70),
#             ha='center', textcoords='offset points', bbox=dict(boxstyle='round,pad=0.5', fc='gray', alpha=0.1),
#             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5',color='gray'))
plt.title('2012 Aircraft Power Plant Patent Counts\n\n\n')
plt.annotate('Precision = 54%, Recall=61%, F-Score=58%\n(Assigns USPC as the Correct Set)', xy=v.get_label_by_id('100').get_position() - np.array([-1.0, 0.2]), xytext=(-100,150),
             ha='center', textcoords='offset points', bbox=dict(boxstyle='round,pad=0.5', fc='gray', alpha=0.1))

#Savefig is not working, returns an empty file and/or cuts off title and a bit of right text box.
#  I saved imaged directly from my console, by right clicking on image.
savefig('Power2012Venn24.png')
plt.show()
