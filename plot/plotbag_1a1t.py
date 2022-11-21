import rosbag
from decawave_ros.msg import uwb_distance
import numpy as np
import statistics
import matplotlib.pyplot as plt

def ax_plot(ax, x, y , title):
    ax.plot(x,y, linestyle="-", color='green', linewidth = 3)
    ax.set_xlabel('Time/s')
    ax.set_ylabel('Distance/m') 
    ax.set_title(title)

bag_1m = rosbag.Bag('/home/usl/catkin_ws/src/decawave_ros/bagfile/indoor/1A1T/1a1t_t0moving_indoor_1m.bag')
bag_3m = rosbag.Bag('/home/usl/catkin_ws/src/decawave_ros/bagfile/indoor/1A1T/1a1t_t0moving_indoor_3m.bag')
bag_5m = rosbag.Bag('/home/usl/catkin_ws/src/decawave_ros/bagfile/indoor/1A1T/1a1t_t0moving_indoor_5m.bag')
bag_7m = rosbag.Bag('/home/usl/catkin_ws/src/decawave_ros/bagfile/indoor/1A1T/1a1t_t0moving_indoor_7m.bag')

bag_list = [bag_1m, bag_3m, bag_5m, bag_7m]
laser_measurements = [1.095, 2.865,5.0355,7.052]

plt.figure(figsize=(15, 12))
plt.subplots_adjust(hspace=0.5)

means = []
stds = []
for i in range(len(bag_list)):
    # Initialize some empty lists for storing the data
    dist_a0t0 = []
    time_a0t0 = []
    for topic,msg,t in bag_list[i].read_messages(topics=['/Decawave']):
        if msg.anc==0 and msg.tag==0:
            time_a0t0.append(t.to_sec())
            dist_a0t0.append(msg.dist)
    bag_list[i].close()

    dist_a0t0 = np.array(dist_a0t0)
    time_a0t0 = np.array(time_a0t0)
    gt = np.full_like(dist_a0t0, laser_measurements[i])
    error = dist_a0t0 - gt  #can be list for mean and stdev
    error_mean = sum(error) / len(error)
    error_mean = statistics.mean(error)
    means.append(error_mean) 
    error_std = statistics.stdev(error)
    stds.append(error_std)
    '''
    m, b = np.polyfit(time_a0t0, dist_a0t0, 1)
    # Plot
    ax=plt.subplot(2,3,i+1)
    ax.scatter(time_a0t0,dist_a0t0,color='yellow',linewidth=0.5, label = "UWB Raw Data")
    ax.plot(time_a0t0,gt,linestyle = '-',color = 'blue', label = "Laser Measurements")
    ax.plot(time_a0t0,m*time_a0t0+b,linestyle = '-',color = 'red', label = "UWB Measurements (LSE)")
    ax.set_xlabel('Time/s')
    ax.set_ylabel('Distance/m') 
    ax.set_title('1a1t_t0moving_indoor_{}m'.format(2*i+1))
    ax.legend()
    '''


ax = plt.subplot(1,1,1)
labels = ['1m', '3m', '5m', '7m']
x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars
rects1 = ax.bar(x - width/2, means, width,label='Mean')
rects2 = ax.bar(x + width/2, stds, width,label='Stdev')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Error/m')
ax.set_xlabel('Range/m')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_title('Error Means and Stdevs vs Ranges')
ax.legend()

def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.005*height,
                round(height,3),ha='center', va='bottom')
autolabel(rects1)
autolabel(rects2)

plt.suptitle("Distance Accuracy v.s. Range")
plt.savefig('./indoor/1a1t/Distance_1a1t_t0moving_indoor_meanstd.png')
plt.show()