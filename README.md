# Road-sign-robot

A robot controlled by a road sign classification algorithm. This repository implements a system that uses a Convolutional Neural Network (CNN) to recognize road signs in real-time.

## Project Files

- **pi.py**: Main script for operating the robot.
- **pi2.py**: Secondary script for testing 
- **SignRec-CNN.h5**: Pre-trained CNN model used for road sign recognition.
- **README.md**: This documentation file.

## Requirements

- Python 3.x
- Essential Python packages (e.g., TensorFlow/Keras, OpenCV, NumPy):
  ```sh
  pip install tensorflow opencv-python numpy
  ```

## Usage

Run the main script:
```sh
python pi.py
```

Or, run the secondary script:
```sh
python pi2.py
```

Ensure that the [SignRec-CNN.h5](./SignRec-CNN.h5) model file is present in the repository.

## Configuration

You might need to modify parameters in [pi.py](./pi.py) or [pi2.py](./pi2.py) to match your hardware setup and operational requirements.

