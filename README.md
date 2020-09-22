# Human-Pose-Estimation
Detecting Human pose via images, Videos and camera

## Human Pose Estimation
### Process where it estimates the position of human and detects all the parts available.
### We use Posenet for detecting poses.
### Process: 
Model detects the person first and then it detects the joints and parts. Posenet detects total of 18 parts right from feet to eyes, ears, nose etc.
### Result:
 Results would be in three formats.
 1. Heat map: Heat map co-ordinates are generated
 2. draw humans: Skeleton part of human image is generated.
 3. inference: We will get class of bodyparts which contains the co-ordinates of each body part and confidence of the respective body part

 ## Note: tf-pose is the library used for pose estimation. IT doesn't support the latest version of tf (2X), rather supports the older version (1x) make sure older version is installed. Else when tf-pose is installing, it will automatically downgrade tf to older version. tf-pose is working on compactibility on newer versions.
