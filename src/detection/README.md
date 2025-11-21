# Detection Module

This module contains all hand detection ROS2 nodes and YOLO detection logic for the RealSense camera integration.

## Directory Structure

```
detection/
├── nodes/                      # ROS2 detection nodes
│   ├── predict_node.py        # Hand detection node using YOLO
│   └── listen_node.py         # Camera listener/debug node
├── detection/                 # YOLO hand detection system
│   ├── yolo.py               # YOLO detection model wrapper
│   ├── configs/              # YOLO model configuration files
│   │   ├── cross-hands.cfg
│   │   ├── cross-hands-tiny.cfg
│   │   ├── cross-hands-tiny-prn.cfg
│   │   └── cross-hands-yolov4-tiny.cfg
│   └── models/               # YOLO model weights
│       └── cross-hands-tiny-prn.weights
├── utils/                     # Utility functions (reserved for future use)
└── README.md
```

## Running the Detection Module

### Prerequisites
Ensure your environment is set up with ROS2 and required dependencies:
```bash
# From the workspace root
source install/setup.bash
```

### Launch Detection Pipeline (Recommended)
Start RealSense camera and hand detection together using the centralized launch configuration:
```bash
ros2 launch robot_launch detection.launch.py
```

This launches both the RealSense camera (with RGB and depth enabled) and the hand detection node in one command.

For more launch configurations and how to create new ones, see [robot_launch/README.md](../robot_launch/README.md).

### Alternative: Run Detection Node Manually
If you prefer to start the camera separately:

1. Start the RealSense camera:
```bash
ros2 launch realsense2_camera rs_launch.py enable_color:=true enable_depth:=true
```

2. In another terminal, run the hand detection node:
```bash
ros2 run detection predict_node
```

The node:
- Subscribes to `/camera/camera/color/image_raw` for RGB frames
- Subscribes to `/camera/camera/depth/image_rect_raw` for depth frames
- Subscribes to `/camera/camera/color/camera_info` for camera intrinsics
- Publishes hand location to `/camera/camera/hand_loc` as a `geometry_msgs/Point`

### Run Debug Listener Node
To monitor camera topics without running detection:
```bash
ros2 run detection listen_node
```

## YOLO Hand Detection

### Model Information
- **Model**: YOLOv3 Tiny with PRN (Pyramid Residual Networks)
- **Input Size**: 640x427 (upscaled to 640x480)
- **Output**: Hand bounding boxes with confidence scores
- **Performance**: Optimized for real-time inference on modest hardware

### Model Variants Available
1. **cross-hands-tiny-prn.weights** (19 MB) - Default, fast inference
2. **cross-hands-tiny.weights** (34 MB) - Better accuracy
3. **cross-hands-yolov4-tiny.weights** (23 MB) - Alternative architecture
4. **cross-hands.weights** (235 MB) - Full model, slower but most accurate

### Switching Models
Edit `predict_node.py` and modify the model loading section:
```python
detection_dir = Path(__file__).parent.parent / 'detection'
config_file = str(detection_dir / 'configs' / 'cross-hands-tiny.cfg')  # Change config
weights_file = str(detection_dir / 'models' / 'cross-hands-tiny.weights')  # Change weights
```

## Node Details

### predict_node.py
Custom node that integrates RealSense camera with YOLO hand detection.

**Subscriptions:**
- `/camera/camera/color/image_raw` (sensor_msgs/Image) - RGB color frames
- `/camera/camera/depth/image_rect_raw` (sensor_msgs/Image) - Depth frames
- `/camera/camera/color/camera_info` (sensor_msgs/CameraInfo) - Camera parameters

**Publications:**
- `/camera/camera/hand_loc` (geometry_msgs/Point) - 3D hand location in camera frame

**Features:**
- Real-time hand detection in RGB images
- 3D hand position calculation using depth data
- Camera calibration matrix support
- Configurable detection confidence and NMS thresholds

### listen_node.py
Debug node for monitoring camera output without running detection.

## Configuration

### Detection Confidence
The YOLO detector has configurable confidence and threshold parameters. Modify in `yolo.py`:
```python
YOLO(config, model, labels, size=416, confidence=0.5, threshold=0.3)
```
- `confidence`: Detection confidence threshold (0-1)
- `threshold`: Non-Maximum Suppression (NMS) threshold (0-1)

## Troubleshooting

### Model files not found
Ensure the model weights and config files exist:
```bash
ls -la src/detection/detection/configs/
ls -la src/detection/detection/models/
```

### Topic names don't match
The node subscribes to RealSense camera topics. Verify topics are publishing:
```bash
ros2 topic list | grep camera
```

### Memory issues
If running on limited hardware:
1. Use the tiny model variant (cross-hands-tiny-prn)
2. Reduce image resolution
3. Increase the timer period in `predict_node.py`

## Future Improvements
- Add more detection models to `utils/`
- Implement model switching via parameters
- Add performance benchmarking tools
- Support multiple camera inputs
- Add hand pose estimation

## References
- YOLOv3 Hand Detection: https://github.com/cansik/yolo-hand-detection
- RealSense ROS2 Wrapper: https://github.com/IntelRealSense/realsense-ros
- ROS2 Documentation: https://docs.ros.org/en/humble/
