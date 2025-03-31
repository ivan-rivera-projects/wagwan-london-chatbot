# Wagwan London Chatbot: Installation & Deployment Instructions

## Overview

This document provides detailed instructions for setting up and deploying the Wagwan London chatbot application on AWS. The application is a serverless conversational AI built with AWS services including Amazon Lex, Lambda, Bedrock, S3, CloudFront, and Cognito.

## Prerequisites

Before you begin, ensure you have:

1. **AWS Account** with administrator access
2. **AWS CLI** installed and configured with appropriate credentials
3. **Basic knowledge** of AWS services and serverless architecture
4. **Domain name** (optional but recommended for production)
5. **GitHub account** for code repository access

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/ivan-rivera-projects/wagwan-london-chatbot.git
cd wagwan-london-chatbot
```

### 2. Set Up Amazon Cognito Identity Pool

1. Sign in to the AWS Management Console and navigate to Amazon Cognito
2. Select "Identity Pools" and click "Create new identity pool"
3. Configure your identity pool:
   - Pool name: `WagwanLondonIdentityPool`
   - Enable unauthenticated access
   - Configure basic IAM roles
4. Note your Identity Pool ID (format: `us-east-1:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

### 3. Configure IAM Permissions

1. Navigate to the IAM Console
2. Select the unauthenticated role created with your Cognito Identity Pool
3. Attach the following managed policies:
   - `AmazonLexRunBotsOnly`
4. Create a custom policy with the following permissions:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "lex:RecognizeText",
           "lex:RecognizeUtterance"
         ],
         "Resource": "arn:aws:lex:us-east-1:*:bot-alias/*"
       }
     ]
   }
   ```
5. Attach this custom policy to the unauthenticated role

### 4. Create Amazon Lex Chatbot

1. Navigate to Amazon Lex in the AWS Console
2. Create a new bot:
   - Bot name: `WagwanLondonBot`
   - Language: English (GB)
   - Create a new service role
3. Create an intent named `WagwanConversation`
   - Add sample utterances like:
     - "Hello"
     - "How are you"
     - "What's up"
     - "Tell me about London"
4. Configure your dialog and create the bot
5. Create a bot alias (e.g., `Production`)
6. Note your Bot ID and Bot Alias ID

### 5. Deploy Lambda Functions

1. Navigate to AWS Lambda in the console
2. Create three new Lambda functions:
   - `production_lambda_function`
   - `lambda_concise_convo`
   - `lambda_clause3`
3. For each function:
   - Runtime: Python 3.10+
   - Upload the corresponding Python file from the repository
   - Set the handler to `lambda_function.lambda_handler`
   - Configure environment variables if needed
4. Set permissions to allow Lex to invoke the functions:
   - Add a trigger from Amazon Lex V2
   - Select your Lex bot and alias

### 6. Configure Amazon Bedrock Access

1. Navigate to Amazon Bedrock in the AWS console
2. Request access to Claude models (both Haiku and Sonnet)
3. Create a model access role with appropriate permissions
4. Update your Lambda execution role to include Bedrock invocation permissions:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "bedrock:InvokeModel"
         ],
         "Resource": [
           "arn:aws:bedrock:us-east-1::model/anthropic.claude-3-haiku-*",
           "arn:aws:bedrock:us-east-1::model/anthropic.claude-3-5-haiku-*"
         ]
       }
     ]
   }
   ```

### 7. Deploy the Frontend

1. Create an S3 bucket:
   ```bash
   aws s3 mb s3://wagwan-london-website
   ```

2. Enable static website hosting on the bucket:
   ```bash
   aws s3 website s3://wagwan-london-website --index-document index.html
   ```

3. Update the `html/index.html` file:
   - Replace the Cognito Identity Pool ID with yours
   - Replace the Lex Bot ID and Alias ID with yours

4. Upload the website files:
   ```bash
   aws s3 cp html/ s3://wagwan-london-website/ --recursive
   ```

5. For production deployments, set up CloudFront:
   - Origin: Your S3 bucket
   - Behaviors: Redirect HTTP to HTTPS
   - Alternate domain names: Your custom domain (optional)
   - SSL Certificate: Generate or import for your domain (optional)

### 8. Configure CloudWatch Logging

1. Ensure CloudWatch logging is enabled for all Lambda functions
2. Set up CloudWatch Alarms for monitoring:
   - Lambda errors and timeouts
   - Lex failed conversations
   - Bedrock model invocation errors

### 9. Test the Deployment

1. Navigate to your S3 website URL or CloudFront distribution domain
2. Test the chatbot with various inputs
3. Check CloudWatch logs for any errors or issues

## Troubleshooting

### Common Issues and Solutions

1. **CORS Issues**:
   - Check S3 bucket CORS configuration
   - Ensure CloudFront is properly configured

2. **Lambda Execution Errors**:
   - Check CloudWatch logs for detailed error messages
   - Verify IAM permissions for Lambda execution roles

3. **Lex Integration Issues**:
   - Ensure Lex has permission to invoke Lambda
   - Check intent configuration and sample utterances

4. **Bedrock Access Problems**:
   - Confirm model access has been approved
   - Verify IAM permissions for Bedrock invocation

## Security Considerations

1. **Identity and Access Management**:
   - Follow principle of least privilege for all IAM roles
   - Regularly review and rotate credentials

2. **Frontend Security**:
   - Enable HTTPS with CloudFront
   - Implement appropriate CORS policies

3. **Monitoring and Alerting**:
   - Set up CloudWatch Alarms for unusual activity
   - Enable AWS CloudTrail for API activity monitoring

## Maintenance and Updates

### Updating the Chatbot

1. **Lambda Functions**:
   - Update code in the repository
   - Redeploy to Lambda using AWS Console or CLI

2. **Lex Bot**:
   - Make changes in the Lex console
   - Build and publish a new version

3. **Frontend**:
   - Update HTML/CSS/JS files
   - Redeploy to S3 and invalidate CloudFront cache if needed

### Monitoring Costs

1. Set up AWS Budgets to track costs
2. Monitor usage of:
   - Lambda invocations
   - Lex conversations
   - Bedrock model calls
   - S3 storage and data transfer
   - CloudFront data transfer

## Support

For additional assistance:
- Refer to the AWS documentation for specific services
- Check the GitHub repository for updates and issues
- Contact the project maintainer at [iam-ivan.com](https://iam-ivan.com)

---

© 2025 Wagwan London Chatbot | Created by Ivan Rivera 