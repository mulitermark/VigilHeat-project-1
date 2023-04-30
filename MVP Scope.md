# MVP User Stories

The MVP will consider the following User Stories.

## High Priority

- As a retail manager, I want to monitor customer flow during peak hours, so I can identify patterns in customer behavior and make informed decisions about store layout and staffing.
- As a retail manager, I want to predict when peak hours are most likely to occur, so I can plan staff schedules and store resources accordingly.
- As a retail manager, I want to receive real-time alerts when queues exceed a certain length, so I can open additional checkout lanes and reduce customer waiting times.

## Medium Priority

- As a retail manager, I want to analyze the efficiency of different checkout lane configurations during peak hours, so I can implement the most effective layout to handle high customer traffic.
- As a retail manager, I want to review the efficiency of staff performance during peak hours, so I can identify areas for improvement and provide targeted training.

## Low Priority

- As a retail manager, I want to track customer satisfaction levels during peak hours, so I can ensure that our store is meeting customer expectations despite increased traffic.

Therefore, this will be focused on people detection for creating a heatmap with the position of people and counting people in the checkout line, as well as a chart of the number of people detected per hour.

# MVP Technical Tasks

Based on the user stories, the following technical tasks should be included in the MVP:

1. Object detection: Use computer vision and machine learning techniques to detect and recognize different objects in the retail store environment. Input: Images or video feeds of the store environment. Output: A list of detected objects with their positions.
2. People detection and real-time display of customer count: Use computer vision and machine learning techniques to detect and track people in the retail store environment and display the real-time customer count on the user interface. Input: Images or video feeds of the store environment. Output: A list of detected people with their positions and a real-time display of the customer count.
3. Peak hour prediction: Analyze historical customer flow data to predict when peak hours are most likely to occur. Input: Historical customer flow data. Output: A prediction of the most likely peak hours for staff and resource scheduling.
4. Checkout line detection: Use the people detection results to identify and track people who are waiting in the checkout line and open a new checkout line when the number of people exceeds a certain threshold. Input: A list of detected people with their positions. Output: A real-time alert and the opening of a new checkout line.
5. Heatmap creation: Use computer vision and machine learning techniques to detect and track people in the retail store environment, and create a heatmap of the customer flow during peak hours. Input: Images or video feeds of the store environment. Output: A graphical representation of the heatmap, showing areas of the store with the highest customer traffic and patterns of movement, with color variations to indicate the density of people in different areas. 
6. Live video play: Display the live video feed of the retail store environment on the user interface. Input: Live video feed from cameras installed in the store. Output: A live video feed display on the user interface.
7. Customer satisfaction survey: Conduct a survey to gather feedback from customers on their shopping experience. Input: Survey questionnaire. Output: Customer feedback data that can be analyzed for insights.

# Task-Based Work Breakdown

## Overview

```uml
@startuml
!theme vibrant
title MVP Task-Based Work Breakdown

|Main Flow|
start
:Get live video feed from cameras installed in the store;
fork
:Object and people detection;
fork
:Object detection;
fork again
:People detection;
fork
:Peak hour prediction;
fork again
:Checkout line detection;
fork again
:Heatmap creation;
end fork
end fork
end fork
:Live video play;
stop
@enduml
```

<img src="MVP%20Scope/image-20230430223443746.png" alt="image-20230430223443746" style="zoom:50%;" />

## Task breakdown

### Object Detection

Object detection is a computer vision task that involves detecting and localizing objects in an image or video. Here are some detailed steps to implement object detection in the context of the MVP:

Training Phase:

1. Choose an appropriate Object Detection model: There are many pre-trained Object Detection models available, such as YOLO, SSD, Faster R-CNN, etc. Choose the model that best fits the requirements of the MVP in terms of accuracy, speed, and hardware compatibility.
2. Fine-tune the model: Fine-tune the pre-trained model on a dataset that is specific to the retail store environment. This is important to ensure that the model can detect the objects that are relevant to the MVP, such as shopping carts, shelves, displays, etc.
3. Data augmentation: Augment the dataset to increase the number of training samples, and improve the robustness of the Object Detection model. Data augmentation techniques include rotation, translation, scaling, flipping, and adding noise to the images.
4. Train the Object Detection model: Train the Object Detection model using the augmented and annotated dataset, using a suitable optimization algorithm such as stochastic gradient descent.
5. Model evaluation: Evaluate the trained Object Detection model on a held-out validation dataset, to measure its accuracy and performance.

Detection Phase:

1. Video Input: Obtain live video feed from cameras installed in the retail store, which will be processed frame by frame.
2. Image Pre-processing: Pre-process each frame of the video, including resizing, normalization, and cropping, to prepare it for input into the Object Detection model.
3. Object detection in real-time: Use the trained Object Detection model to detect and recognize different objects in real-time on the frames of the video. Use the output of the Object Detection model to provide a list of detected objects with their positions.
4. Integration with other MVP components: Integrate the Object Detection module with other MVP components, such as People Detection and Heatmap Creation, to provide a comprehensive understanding of the customer flow in the retail store environment.
5. Deployment and maintenance: Deploy the Object Detection module on the target hardware, and ensure that it is working as expected. Regularly update the Object Detection model with new data to improve its accuracy and performance.

### People detection

A similar task as object detection.

### Peak Hour Prediction

Peak hour prediction is a critical component of the MVP as it enables retail managers to effectively plan staff schedules and allocate resources. Here are some steps to implement peak hour prediction:

Training Phase:

1. Data Collection: Collect historical customer flow data over a period of time, ideally several months or a year.
2. Data Pre-processing: Clean and pre-process the customer flow data, including removing outliers and missing values, and aggregating the data into hourly or daily intervals.
3. Exploratory Data Analysis: Analyze the customer flow data to identify patterns and trends in customer behavior, such as peak hours, seasonal variations, and day of the week effects.
4. Feature Engineering: Create new features that capture relevant information about customer behavior, such as time of day, day of the week, and holiday periods.
5. Model Selection: Select an appropriate machine learning model to predict customer flow, such as time series models (e.g. ARIMA, SARIMA), regression models (e.g. linear regression, random forest), or neural network models (e.g. LSTM).
6. Model Training and Validation: Train the selected model on the pre-processed and engineered data, and validate the model's performance using cross-validation techniques.

Prediction Phase:

1. Obtain the current number of customers and current time.
2. Use the trained model to predict customer flow for the next half-day, and provide the predictions to the retail manager in a user-friendly format, such as a dashboard or report.
3. Integrate with other MVP components
4. Deployment and Maintenance

### Checkout Line Detection

Checkout line detection is a key feature of the MVP that enables retail managers to open new checkout lanes and reduce customer waiting times. Here are the detailed implementation steps for checkout line detection:

1. People detection: Use the people detection module to detect and track people in the retail store environment. Use the output of the object detection module to provide a list of detected objects with their positions.
2. Define the checkout line area: Define the area in the retail store where customers typically wait in line to checkout. This could be a physical area marked by tape or signage, or it could be a virtual area defined using computer vision techniques.
3. Check if people are in the checkout line area: Check the positions of the detected people against the defined checkout line area to determine if they are waiting in line. If a person is inside the checkout line area, they are considered to be waiting in line.
4. Count the number of people in the checkout line: Count the number of people who are waiting in line by analyzing the positions of the detected people in the checkout line area. If the number of people waiting in line exceeds a certain threshold, generate a real-time alert to open a new checkout lane.
5. Integrate with other MVP components
6. Deployment and maintenance

###  Heatmap creation

Heatmap creation is a key component of the MVP, which will help the retail manager to visualize the customer flow during peak hours. Here are some detailed steps to implement heatmap creation:

1. People detection
2. Heatmap generation: Create a heatmap of the customer flow during peak hours by analyzing the positions of the detected people. Use color variations to indicate the density of people in different areas. The areas with the highest customer traffic will appear in warmer colors, while areas with lower customer traffic will appear in cooler colors.
3. Integration with other MVP components
4. Visualization: Display the generated heatmap on the user interface, along with real-time customer count, checkout line information, and other relevant information. This will help the retail manager to identify areas of the store with the highest customer traffic and patterns of movement.
5. Deployment and maintenance