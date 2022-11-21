import rosbag
from decawave_ros.msg import anchor, uwb_distance
import matplotlib.pyplot as plt
import numpy as np


import csv
import numpy as np
import json


with open("/home/alvika-usl/uwb_bag_files/RTLS_log_ROSS.txt") as f:
    reader = csv.reader(f, delimiter=":")
    data = list(reader)

tag_locs = []
for line in data:
    #print(line[2])
    if line[2] == 'LE':
        #print(line[6])
        tag_loc = json.loads(line[6])
        #print(type(tag_loc))
        tag_locs.append(tag_loc)
tag_locs = np.array(tag_locs)
#print(tag_locs)

#bag = rosbag.Bag('/home/alvika-usl/Downloads/decawave_ros/bagfile/indoor/3A1T/3a1t_t0moving.bag')
#bag = rosbag.Bag('/home/alvika-usl/Downloads/3a1t_t0moving_RTLS.bag')  #anchor_x = [0,1.7105,0] anchor_y = [0,0,2.088]
#bag = rosbag.Bag('/home/alvika-usl/Downloads/3a1t_3aontrollystationary_t0moving.bag')
#bag = rosbag.Bag('/home/alvika-usl/Downloads/4a1t_4amoving_t0moving_golfcart.bag')
bag = rosbag.Bag('/home/alvika-usl/uwb_bag_files/2022-11-17-16-28-30.bag')


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
    if (msg.tag==0 and len(msg.dist_array)==4):

        print("length",msg.dist_array)
        if msg.dist_array[0].anc==0:
            time_a0t0.append(t.to_sec())
            dist_a0t0.append(msg.dist_array[0].dist)
        if msg.dist_array[1].anc==1:
            time_a1t0.append(t.to_sec())
            dist_a1t0.append(msg.dist_array[1].dist)
        if msg.dist_array[2].anc==2:
            time_a2t0.append(t.to_sec())
            dist_a2t0.append(msg.dist_array[2].dist)
        
            

bag.close()

#smoothen distance data
print(dist_a2t0)
kernel_size = 10
kernel = np.ones(kernel_size) / kernel_size
dist_a0t0 = np.convolve(dist_a0t0, kernel, mode='same')
dist_a1t0 = np.convolve(dist_a1t0, kernel, mode='same')
dist_a2t0 = np.convolve(dist_a2t0, kernel, mode='same')
time_a0t0=[round(time_a0t0[i]-time_a0t0[0],2) for i in range(0,len(time_a0t0))]
time_a1t0=[round(time_a1t0[i]-time_a1t0[0],2) for i in range(0,len(time_a1t0))]
time_a2t0=[round(time_a2t0[i]-time_a2t0[0],2) for i in range(0,len(time_a2t0))]
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

plt.suptitle('Distance_3a1t_t0moving_indoor')
plt.savefig('./outdoor/Distance_3a1t_t0moving_indoor.png')
plt.show()

'''
anchor_x = [0,1.7105,0] #anchor coordinates in meters
anchor_y = [0,0,2.088]

anchor_x = [0,0.55,0.275] #anchor coordinates in meters
anchor_y = [0,0,0.27]


anchor_x=[0,2.3,0.01]  #golfcart no GPS
anchor_y=[0,-0.0041,1.37]
'''
anchor_x=[0,2.34,0.16]
anchor_y=[0,0,1.6]
anchor = list(zip(anchor_x, anchor_y))


#anc 0 :(2.6,2.07), anc 1 (2.6,0), anc2 (0,0) anc 3 (3.4,1.66)

#fig, ax = plt.figure()
'''
ax = plt.axes(xlim=(-500,4000),ylim=(-500,4000))
anchor = np.array(anchor)
ax.scatter(anchor[:,0], anchor[:,1], c='blue')
scatter = ax.scatter(0, 0, c='red')
'''

def trilaterate(anchor_x, anchor_y, anchor1, anchor2, anchor3):
    """
    @brief: Trilaterate Tag location
    @param: anchor_x - List of anchor coordinates along the X-axis
            anchor_y - List of anchor coordinates along the Y-axis
            anchor1 - Distance to the 1st Anchor
            anchor2 - Distance to the 2nd Anchor
            anchor3 - Distance to the 3rd Anchor
    @ret:   tag_coordinates - Tag Coordinates in a numpy array.
    """
    r1_sq = pow(anchor1,2)
    r2_sq = pow(anchor2,2)
    r3_sq = pow(anchor3,2)

    # Solve a linear matrix equation where x,y is the Tag coordinate:
    # Ax + By = C
    # Dx + Ey = F
    A = (-2*anchor_x[0]) + (2*anchor_x[1])
    B = (-2*anchor_y[0]) + (2*anchor_y[1])
    C = r1_sq - r2_sq - pow(anchor_x[0],2) + pow(anchor_x[1],2) - pow(anchor_y[0],2) + pow(anchor_y[1],2) 
    D = (-2*anchor_x[1]) + (2*anchor_x[2])
    E = (-2*anchor_y[1]) + (2*anchor_y[2])
    F = r2_sq - r3_sq - pow(anchor_x[1],2) + pow(anchor_x[2],2) - pow(anchor_y[1],2) + pow(anchor_y[2],2) 

    a = np.array([[A, B], [D, E]])
    b = np.array([C, F])
    tag_coordinates = np.linalg.solve(a, b)
    # print("Tag Coordinate:", tag_coordinates)
    return tag_coordinates

previous_value = [(0,0)]
value = 0
samples_to_count = 3
count = 0
total = np.array((0,0))
tag_loc=[]


def update(previous_value,node1,node2,node3):

    tag = trilaterate(anchor_x, anchor_y, node1, node2, node3)
    # print("Tag Coordinate:", tag)
    

    global count
    global samples_to_count
    global total
    #to smoothen distance data in real time to be replaced by kalman later. For now just smoothen all distance data in advance
    if count < samples_to_count: 
            total = total + tag
            count += 1
    if count == samples_to_count:
        total /= samples_to_count
        #scatter.set_offsets(total)
        # print("Tag: ", total)
        total = np.array((0,0))
        count = 0
    
        

    return tag   


ax=plt.axis([-35,35,-35,35])
pos_x_coors=[]
pos_y_coors=[]
for i in range(0,len(dist_a0t0)):
    tag=update(previous_value,dist_a0t0[i],dist_a1t0[i],dist_a2t0[i])
    previous_value = tag
    pos_x_coors.append(tag[0])
    pos_y_coors.append(tag[1])



for i in range(0,len(pos_x_coors)):
    #print((pos_x_coors[i]-pos_x[i])/1000,"pos_x",(pos_y_coors[i]-pos_y[i])/1000,"pos_y")
    
    plt.plot(pos_x_coors[i], pos_y_coors[i], color='green', linestyle='dashed', 
     marker='o',
     markerfacecolor='blue', 
     markersize=3)
    #plt.axis([0,7,0,7])
    #plt.hold(True)
    plt.pause(0.01)
plt.show()

print(np.size(tag_locs))   
#anim = FuncAnimation(fig, update, interval = 0.0000001, fargs= previous_value, blit = True)


'''
for i in range(0,len(tag_locs)):
    #print((pos_x_coors[i]-pos_x[i])/1000,"pos_x",(pos_y_coors[i]-pos_y[i])/1000,"pos_y")
    
    plt.plot(tag_locs[i][0], tag_locs[i][1], color='green', linestyle='dashed', 
     marker='o',
     markerfacecolor='blue', 
     markersize=3)
    #plt.axis([0,7,0,7])
    #plt.hold(True)
    plt.pause(0.01)
plt.show()
'''
ax=plt.plot(pos_x_coors, pos_y_coors, color='r', label='Location : Range data (Trilateration)')
ax=plt.plot(tag_locs[:,0], tag_locs[:,1], color='g', label='Location : Decawave RTLS')
 
# Naming the x-axis, y-axis and the whole graph
plt.xlabel("x (m)",fontsize=16)
plt.ylabel("y (m)",fontsize=16)
plt.title("Tag Location in meters",fontsize=16)
  
# Adding legend, which helps us recognize the curve according to it's color
plt.legend(prop={"size":16})
#leg = ax.legend(prop={"size":16})
  
# To load the display window
plt.show()
#print(tag_locs)