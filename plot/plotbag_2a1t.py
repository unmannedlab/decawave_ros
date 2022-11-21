import rosbag
from decawave_ros.msg import uwb_distance
bag = rosbag.Bag('/home/usl/1a1t_t0moving_accuracy_indoor.bag')
# Initialize some empty lists for storing the data
dist_a0t0 = []
dist_a1t0 = []
time_a0t0 = []
time_a1t0 = []

def ax_plot(ax, x, y , title):
    ax.plot(x,y, linestyle="-", color='green', linewidth = 3)
    ax.set_xlabel('Time/s')
    ax.set_ylabel('Distance/m') 
    ax.set_title(title)

for topic,msg,t in bag.read_messages(topics=['/Decawave']):
    if msg.anc==0 and msg.tag==0:
        time_a0t0.append(t.to_sec())
        dist_a0t0.append(msg.dist)
    if msg.anc==1 and msg.tag==0:
        time_a1t0.append(t.to_sec())
        dist_a1t0.append(msg.dist)

bag.close()
# Plot
import matplotlib.pyplot as plt
  
# Define X and Y variable data
plt.figure(figsize=(15, 12))
plt.subplots_adjust(hspace=0.5)
ax1=plt.subplot(1,2,1)
ax_plot(ax1,time_a0t0,dist_a0t0,title='Anchor0-Tag0')
ax2=plt.subplot(1,2,2)
ax_plot(ax2,time_a1t0,dist_a1t0,title='Anchor1-Tag0')

plt.suptitle('Distance_1a1t_t0moving_accuracy_indoor')
plt.savefig('./outdoor/Distance_1a1t_t0moving_accuracy_indoor.png')
plt.show()
