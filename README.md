# ML-Workflow-For-Scones-Unlimited-On-Amazon-SageMaker
Using AWS Sagemaker to build an image classification model that can tell bicycles apart from motorcycles. The model is deployed and we use AWS Lambda functions to build supporting services, and AWS Step Functions to compose our model and services into an event-driven application. 

# Step One : Data Staging

- Extract the dataset from the [hosting website](https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz). 
- Explore the data, and transform it to the correct shape and format.
- As documented on the homepage of the hosting website, b'data' contains rows of 3073 unsigned integers, representing three channels (red, green, and blue) for one 32x32 pixel image per row. Each 1024 items in a row is a channel (red, green, then blue). Each 32 items in the channel are a row in the 32x32 image. Using python, we can stack these channels into a 32x32x3 array, and save it as a PNG file.
- For this project we just need to capture all the bicycles and motorcycles and save them. Scones Unlimited can use a model that tells these apart to route delivery drivers automatically.
- Construct a dataframe containing the training images (df_train) and a dataframe containing the testing images (df_test). The length of these dataframes are 1000 and 200 respectively.
- Create a folder called train to upload the training images and a test folder to upload the testing images.
- Upload the train and test folders to an S3 bucket.

# Step Two : Model Training

- For Image Classification, Sagemaker expects metadata e.g. in the form of TSV files with labels and filepaths. We can generate these using our Pandas DataFrames from earlier.
- Upload both manifest files.
- Use the image_uris function from the SageMaker SDK to retrieve the latest image-classification image.
- Create an Estimator for an estimator img_classifier_model that uses one instance of ml.p2.xlarge. Ensure to output to a specific S3 location.
- Define the inputs to the model and set the key hyperparameters.
- The image-classification image uses four input channels with very specific input parameters. Define these as well
- Train the model. My model achieved a validation accuracy of 86.4%.
- Deploy the trained model. Note down the model endpoint for later use.
- Instantiate a Predictor. Use the predictor to process the payload.

# Step Three : Lambda and Step Function Workflow
 - We have to write and deploy three Lambda functions, and then use the Step Functions visual editor to chain them together.
 - The first lambda function is responsible for data generation. The second one is responsible for image classification. And the third function is responsible for filtering out low-confidence inferences.

# Step Four : Testing and Evaluation
- Perform several Step Function invokations using data from the test dataset. This process should give you confidence that the workflow both succeeds AND fails as expected.
-  In addition, you will use the captured data from SageMaker Model Monitor to create a visualization to monitor the model.
-  I have created a histogram, scatter and line plot to visualize the results.

# Summary
I created an event-drivent ML workflow that can be incorporated into the Scones Unlimited production architecture. I also used the SageMaker Estimator API to deploy my SageMaker Model and Endpoint, and used AWS Lambda and Step Functions to orchestrate the ML workflow. Using SageMaker Model Monitor, I instrumented and observed my Endpoint, and at the end of the project I built several visualizations to help stakeholders understand the performance of the Endpoint over time.

# Relevant Pictures
## Accuracy of Model

![modelAccuracy](https://user-images.githubusercontent.com/67323371/145066456-e4b38ecf-588d-4505-8e8f-171a3aa64a4a.png)

## Step Functions Workflow

![stepfunctions_graph](https://user-images.githubusercontent.com/67323371/145066062-53beef43-4eab-4b58-a662-1f55e6077317.png)

## Scatter Plot

![scatterPlot](https://user-images.githubusercontent.com/67323371/145066140-61e035cc-9078-438b-b5e2-3e715d3f28cb.png)


