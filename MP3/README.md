# 3.1. AWS Graph Creator Lambda Function:

### 1. Set up the DynamoDB Table:

- Go to the AWS Management Console and navigate to DynamoDB.
- Create a new table with attributes for source, destination, and distance.
- Make sure to configure the primary key appropriately (e.g., a composite key with source and destination).

### 2. Create the Lambda Function:

- Go to the AWS Management Console and navigate to Lambda.
- Create a new Lambda function with a Python runtime.
- Write the code to parse the input graph, compute shortest distances using BFS, and store the data in DynamoDB.
- Make sure to include the necessary IAM permissions for accessing DynamoDB.

### 3. Implement the Lambda Function:

### 4. Set up API Gateway:

- Go to the AWS Management Console and navigate to API Gateway.
- Create a new REST API with a POST method.
- Configure the integration type to be AWS Lambda and select the Lambda function created earlier.
- Deploy the API to a stage.

### Testing:

- Use an HTTP client like Postman to send a POST request to the API Gateway endpoint with the graph data in the body.
- Check the DynamoDB table to verify that the data has been stored correctly.

Remember to replace placeholders like 'YourDynamoDBTableName' with your actual DynamoDB table name. Also, ensure proper error handling and security measures are implemented as per your project requirements.