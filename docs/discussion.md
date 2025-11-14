## Discussion of Parameters
As can be seen in the `/code/` folder, for the three controllers
the speed `V` is defined in the same way.

```python
if abs_err < 30:
    v = 8 
elif abs_err < 60:
    v = 3 
elif abs_err < 200:
    v = 2
elif abs_err < 250:
    v = 1
```

V is a variable speed defined with a step function that reduces the speed
as the error increases. The idea behind this is that if the car is aligned with
the line in a stable way, for example on a straight segment, we can increase the speed without losing
much stability. But if the error is larger, we are interested in going slower so that the car has
time to realign with the straight.

![alt text](screenshots/Recta1.png)

However, this has the downside that, on a curve, it may momentarily align with the line
and produce a sudden acceleration that destabilizes the trajectory. The function V has been defined
taking into account the shape of the track and the other defined parameters, tuned by trial and error.

![alt text](screenshots/Curva1.png)

The parameters defined for the angular velocity are:

| Constant  |  Value   |
|-----------|----------|
| kp        |   0.008  |
| ki        | 0.000005 |
| kd        |   0.003  |

The angular velocity W is defined as follows:

```python
HAL.setW(P+I+D)
```
In the following section the three variables P, I, D and the types
of controllers implemented will be explained.

## Explanation of Controller Types
**P: proportional control action**

Provides a response proportional to the error. In the code it has been implemented as follows:

```python
P = kp*err
```

**I: integral control action**

Provides a response proportional to the accumulated error until the error is close to 0 (the accumulated error is reset).
In the code it is considered that if `abs_err < 45` then `err` is close to 0.

```python
if abs_err < 45:
    I = 0
       else:
    I = I + ki*err
```
**D: derivative control action**

Provides a response proportional to the rate of change of the error with respect to time.

```python
D = kd*(err-err_ant)
```

**P_Controller:** Only `P` acts.

**PI_Controller:** Only `P` and `I` acts.

**PID_Controller:** All variables act (`P`, `I`, `D`).

## Explanation of Error Computation
The error used to align the robot with the line is based on the centroid. The centroid is the point that represents the “average position” of the detected contour/object. In this case, the centroid of the line is obtained. A color mask (HSV) is created to isolate the red line. Working on a binary mask and extracting contours is more efficient than processing the whole image.

```python
img = HAL.getImage()
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
red_mask = cv2.inRange(hsv, (0,125,125), (30,255,255))
contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
M = cv2.moments(contours[0])
if M["m00"] != 0:
    cX = M["m10"] / M["m00"]
    cY = M["m10"] / M["m00"]
else:
    cX, cY = 0, 0
```

To calculate the error, the x-coordinate of the centroid is taken and subtracted from the center of the image (x = 320 for width 640) to obtain the lateral deviation that feeds the controller.

```python
err = 320 - cX
```
## Discussion of Methods
Next, we will discuss the advantages and disadvantages of the three implemented controllers
based on the measured times.

| Controlador | Tiempo (s) |
|-------------|------------|
| P           | 123,05     |
| PD          | 119,17     |
| PID         | 124,23     |

**PD provides greater stability on this track:** 
The derivative action attenuates oscillations and improves the response to changes (mainly curves), which reduces the total time compared to P alone.

**PID shows more instability here due to the integral action:** 
The accumulation of error can induce excessive corrections in the curves (because of the integral term), causing overshoot and worse times compared to P and PD.