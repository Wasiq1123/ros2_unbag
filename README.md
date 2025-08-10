
````markdown
# ROS2 Bag Export and CSV Merger

## Overview

This project helps you record ROS2 bag data, export topic data into CSV files, and then merge fragmented CSV files per topic into single consolidated CSV files for easier analysis.

---

## Setup and Usage

### 1. Create ROS2 Workspace and Clone Repository

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/Wasiq1123/ros2_unbag.git
````

---

### 2. Build the Package

Go to the root of your workspace and build:

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash   # Replace 'humble' with your ROS2 distro if different
colcon build --packages-select ros2_bag_exporter
source install/setup.bash
```

---

### 3. Record ROS2 Bag Data

In a new terminal, source ROS and run the bag recording command:

```bash
source /opt/ros/humble/setup.bash
ros2 bag record /topic_name_1 /topic_name_2 ... 
# Replace with actual topic names you want to record
```

The bag files (`.db3`) will be saved in your current directory or a specified path.

---

### 4. Modify the Exporter Configuration

Edit the configuration file `ros2_bag_exporter/config/exporter_config.yaml`:

* Set `bag_path` to the full path of your recorded `.db3` bag file.
* Adjust `output_dir` to your desired output folder for exported CSV files.
* Modify `topics` with the topics you want to export and their message types.

Example:

```yaml
bag_path: "/home/user/ros2_ws/bags/my_bagfile.db3"
output_dir: "/home/user/ros2_ws/ros2_bag_exports"
storage_id: "sqlite3"
topics:
  - name: "/odom"
    type: "Odometry"
    sample_interval: 1
  - name: "/imu"
    type: "IMU"
    sample_interval: 100
  - name: "/camera/color/image_raw"
    type: "Image"
    encoding: "rgb8"
    sample_interval: 5
```

---

### 5. Run the Exporter

Execute the exporter node to export CSV files per timestamp:

```bash
ros2 run ros2_bag_exporter bag_exporter
```

This will generate multiple CSV files per topic inside the specified output directory, often split by timestamps.

---

### 6. Merge CSV Files per Topic

To merge all fragmented CSV files per topic into one consolidated CSV file, run the Python script:

```bash
python3 merge_nested_csvs.py /path/to/exporter/output_dir /path/to/merged_output_dir
```

* Replace `/path/to/exporter/output_dir` with the same `output_dir` from your `exporter_config.yaml`.
* Replace `/path/to/merged_output_dir` with the folder where you want the combined CSV files to be saved.

---

## Acknowledgements

The configuration file format and initial exporting tool are cloned and adapted from the excellent repository [ros2\_bag\_exporter](https://github.com/Geekgineer/ros2_bag_exporter/blob/main/config/exporter_config.yaml).
Special thanks to [Geekgineer](https://github.com/Geekgineer) for developing and maintaining this valuable resource. For further details, please refer to the README file in the original repository.

---

## Summary

* Record ROS2 bags of your topics.
* Export bag data into CSV files (one per timestamp).
* Use the merger script to combine all CSV files per topic into single files for easier analysis.

---

## Requirements

* ROS 2 Humble (or compatible)
* Python 3 with `pandas` installed:

  ```bash
  pip install pandas
  ```
