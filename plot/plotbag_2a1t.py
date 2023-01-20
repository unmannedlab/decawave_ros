import rosbag
from decawave_ros.msg import uwb_distance
import matplotlib.pyplot as plt

bag = rosbag.Bag('/home/usl/catkin_ws/2a1t_allmoving_outdoor.bag')
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
    if msg.tag==0:
        print(len(msg.dist_array))
        if len(msg.dist_array) == 2:
            if msg.dist_array[0].anc==0:
                time_a0t0.append(t.to_sec())
                dist_a0t0.append(msg.dist_array[0].dist)
            if msg.dist_array[1].anc==1:
                time_a1t0.append(t.to_sec())
                dist_a1t0.append(msg.dist_array[1].dist)
        if len(msg.dist_array) == 1:
            if msg.dist_array[0].anc==0:
                time_a0t0.append(t.to_sec())
                dist_a0t0.append(msg.dist_array[0].dist)
            elif msg.dist_array[0].anc==1:
                time_a1t0.append(t.to_sec())
                dist_a1t0.append(msg.dist_array[0].dist)
        if len(msg.dist_array) == 0:
            continue 

bag.close()

  
# Define X and Y variable data
plt.figure(figsize=(15, 12))
plt.subplots_adjust(hspace=0.5)
ax1=plt.subplot(1,2,1)
ax_plot(ax1,time_a0t0,dist_a0t0,title='Anchor0-Tag0')
ax2=plt.subplot(1,2,2)
ax_plot(ax2,time_a1t0,dist_a1t0,title='Anchor1-Tag0')

plt.suptitle('Distance_2a1t_allmoving_outdoor')
plt.savefig('./outdoor/Distance_2a1t_allmoving_outdoor.png')
plt.show()


