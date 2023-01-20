import rosbag
from decawave_ros.msg import uwb_distance
import matplotlib.pyplot as plt

bag = rosbag.Bag('/home/usl/catkin_ws/3a1t_3aontrollystationary_t0moving.bag')
# Initialize some empty lists for storing the data
dist_a0t0 = []
dist_a1t0 = []
dist_a2t0 = []
time_a0t0 = []
time_a1t0 = []
time_a2t0 = []

def ax_plot(ax, x, y , title):
    ax.plot(x,y, linestyle="-", color='green', linewidth = 3)
    ax.set_xlabel('Time/s')
    ax.set_ylabel('Distance/m') 
    ax.set_title(title)

for topic,msg,t in bag.read_messages(topics=['/Decawave']):
    #print(msg)
    if msg.tag==0:
        print(len(msg.dist_array))
        if len(msg.dist_array) == 3:
            if msg.dist_array[0].anc==0:
                time_a0t0.append(t.to_sec())
                dist_a0t0.append(msg.dist_array[0].dist)
            if msg.dist_array[1].anc==1:
                time_a1t0.append(t.to_sec())
                dist_a1t0.append(msg.dist_array[1].dist)
            if msg.dist_array[2].anc==2:
                time_a2t0.append(t.to_sec())
                dist_a2t0.append(msg.dist_array[2].dist)
        if len(msg.dist_array) == 2:
            print(msg)
            if msg.dist_array[0].anc==0:
                time_a0t0.append(t.to_sec())
                dist_a0t0.append(msg.dist_array[0].dist)
                if msg.dist_array[1].anc==1:
                    time_a1t0.append(t.to_sec())
                    dist_a1t0.append(msg.dist_array[1].dist)
                if msg.dist_array[1].anc==2:
                    time_a2t0.append(t.to_sec())
                    dist_a2t0.append(msg.dist_array[1].dist)
            elif msg.dist_array[0].anc==1:
                time_a1t0.append(t.to_sec())
                dist_a1t0.append(msg.dist_array[0].dist)
                time_a2t0.append(t.to_sec())
                dist_a2t0.append(msg.dist_array[1].dist)
        if len(msg.dist_array) == 1:
            if msg.dist_array[0].anc==0:
                time_a0t0.append(t.to_sec())
                dist_a0t0.append(msg.dist_array[0].dist)
            if msg.dist_array[0].anc==1:
                time_a1t0.append(t.to_sec())
                dist_a1t0.append(msg.dist_array[0].dist)
            if msg.dist_array[0].anc==2:
                time_a2t0.append(t.to_sec())
                dist_a2t0.append(msg.dist_array[0].dist)
        if len(msg.dist_array) == 0:
            continue 
bag.close()
# Plot
# Define X and Y variable data
plt.figure(figsize=(15, 12))
plt.subplots_adjust(hspace=0.5)
ax1=plt.subplot(2,2,1)
ax_plot(ax1,time_a0t0,dist_a0t0,title='Anchor0-Tag0')
ax2=plt.subplot(2,2,2)
ax_plot(ax2,time_a1t0,dist_a1t0,title='Anchor1-Tag0')
ax3=plt.subplot(2,2,3)
ax_plot(ax3,time_a2t0,dist_a2t0,title='Anchor2-Tag0')

plt.suptitle('Distance_3a1t_3atrollystationary_t0moving_indoor')
plt.savefig('./indoor/Distance_3a1t_3atrollystationary_t0moving_indoor.png')
plt.show()
