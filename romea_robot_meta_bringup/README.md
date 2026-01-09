# 1) Overview #

The romea_lidar_meta_bringup package provides: 

 - **Launch files** able to launch ros2 receiver drivers according a meta-description file provided by user (see next section for LIDAR meta-description file overview), only one driver is supported for the moment :

   - [sick_scan](https://github.com/SICKAG/sick_scan_xd)

   You can launch a LIDAR driver from the command line using: 

    ```console
    ros2 launch romea_lidar_meta_bringup lidar_driver.launch.py robot_namespace:=robot meta_description_file_path:=/path_to_file/meta_description_file.yaml
    ```

   where :

   - *robot_namespace* is the name of the robot 
   - *meta_description_file_path* is the absolute path of meta-description file    

 - A **Python module** able to load and parse LIDAR meta-description file as well as to create URDF description of the LIDAR sensor according a given meta-description.

 - A **ROS2 python executable** able to create LIDAR URDF description via command line according a given meta-description file  :

  ```console
  ros2 run romea_lidar_meta_bringup urdf_description.py robot_namespace:robot meta_description_file_path:/path_to_file/meta_description_file.yaml > lidar.urdf`
  ```

   where :

   - *robot_namespace* is the name of the robot 
   - *meta_description_file_path* is the absolute path of meta-description file    

   This URDF  can be directly concatened with mobile base and other sensor URDFs to create a complete URDF description of the robot.  

   
# 2) LIDAR meta-description #

The LIDAR meta-description is a YAML file consisting of five items: 

- **name**: The name assigned to the LIDAR sensor by the user.
- **driver**: Configuration of the ROS2 driver to operate the LIDAR (detailed in section 4).
- **configuration**: Describes basic specifications of the LIDAR sensor (type, model, rate, etc.).
- **geometry**: Specifies the LIDAR's location and orientation on the robot (used in the URDF).
- **records**: Defines which topics should be recorded during experiments or simulations. Remappings ensure the LIDAR topics have consistent names across drivers and simulation.

Example :
```yaml
name: "lidar"  # name of the lidar
driver: #driver configuration
  pkg: sick_scan #ros2 driver package name
  executable: sick_generic_caller # node to be launched
  parameters: # node parameters
  	ip: "192.168.1.112" #device ip
  	port: 2112 #communication port
configuration: # lidar configuration
  type: sick  # lidar type
  model: lms151 # lidar model
  rate: 50 # hz (optional according lidar model)
  resolution: 0.5  # deg (optional according lidar model)
geometry: #geometry configuration
  parent_link: "base_link" # name of parent link where is located the LIDAR senor
  xyz: [2.02, 0.0, 0.34] # its position in meters
  rpy: [0.0, 0.0, 0.0] # its orienation in degrees
records: #record configuration
  scan: true  # scan topic will be recorded in bag
  cloud: false # cloud topic wil not be recorded in bag
```

# 4) Supported LIDAR models

The following LIDAR models are currently supported by the package:

|  type  |   model    |
| :----: | :--------: |
| sick   |  lmsxx     |
| sick   |  tim5xx    |

You can find detailed specifications of each supported model in the romea_driver_description package's config directory.

# 5) Supported LIDAR ROS2 drivers

As of now, only the [sick_scan](https://github.com/SICKAG/sick_scan_xd) driver is supported. You can configure the driver section in the meta-description file like this:

- **Sick scan**:

```yaml
  pkg: sick_scan #ros2 driver package name
  executable: sick_generic_caller # node to be launched
  parameters: # node parameters
  	ip: "192.168.1.112" #device ip
  	port: 2112 #communication port

```

 A dedicated Python launch file is provided for each driver in the launch directory. When you launch the imu.launch.py file, the corresponding driver node will automatically launch, using the parameters defined by the user. Thanks to remapping defined inside each driver launch files, the data provided by drivers are always publish in the same topics called:

- scan(sensor_msgs/LaserScan)
- cloud(sensor_msgs/PointCloud2)
