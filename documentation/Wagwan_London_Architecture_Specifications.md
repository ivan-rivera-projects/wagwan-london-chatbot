# Wagwan London: Conversational AI Platform Architecture and Specifications

## Executive Summary

Wagwan London is an innovative conversational AI platform that embodies authentic South London cultural dialect and personality. Built on a serverless AWS architecture, the platform delivers a unique, culturally immersive chatbot experience with minimal operational overhead and high scalability.

This document outlines the complete architecture, technical specifications, and design decisions that form the foundation of the Wagwan London platform.

![AWS Architecture Diagram](../wagwan_london_architecture.png)

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Components](#architecture-components)
3. [Data Flow](#data-flow)
4. [Technical Specifications](#technical-specifications)
5. [Security Architecture](#security-architecture)
6. [Monitoring and Logging](#monitoring-and-logging)
7. [Performance Considerations](#performance-considerations)
8. [Scalability and Reliability](#scalability-and-reliability)
9. [Cost Optimization](#cost-optimization)
10. [Limitations and Constraints](#limitations-and-constraints)
11. [Future Enhancements](#future-enhancements)

## System Overview

Wagwan London is a cloud-native conversational AI that leverages AWS's serverless and AI/ML services to create a culturally authentic chatbot with the personality of South London youth. The application combines:

- Natural language processing through Amazon Lex
- Advanced AI generation via Amazon Bedrock with Claude models
- Serverless compute with AWS Lambda
- Static website hosting with Amazon S3 and CloudFront
- Identity management with Amazon Cognito

The platform operates entirely serverless, ensuring high availability, automatic scaling, and cost efficiency.

## Architecture Components

### Frontend Layer

| Component | AWS Service | Purpose |
|-----------|-------------|---------|
| Static Web Assets | Amazon S3 | Hosts HTML, CSS, JavaScript, and images |
| Content Delivery | Amazon CloudFront | Global content delivery with edge caching |
| Security | HTTPS/TLS | Secure communication with clients |
| User Interface | HTML/CSS/JavaScript | Responsive chat interface |

### Identity and Security Layer

| Component | AWS Service | Purpose |
|-----------|-------------|---------|
| User Authentication | Amazon Cognito | Anonymous user access management |
| API Authorization | IAM Roles | Fine-grained access control to AWS services |
| Encryption | AWS KMS | Data encryption at rest and in transit |

### Conversation Processing Layer

| Component | AWS Service | Purpose |
|-----------|-------------|---------|
| Intent Recognition | Amazon Lex V2 | Natural language understanding |
| Conversation State | Lex Session Attributes | Maintains conversation context |
| Bot Aliases | Lex Bot Aliases | Manages different versions of the chatbot |

### Business Logic Layer

| Component | AWS Service | Purpose |
|-----------|-------------|---------|
| Primary Function | AWS Lambda (`production_lambda_function.py`) | Main chatbot logic |
| Concise Response Function | AWS Lambda (`Lambda_consiceconvo_wagwan_function.py`) | Alternative shorter response style |
| Clause 3 Function | AWS Lambda (`lambda_function_clause3.py`) | Alternative personality variant |

### AI Generation Layer

| Component | AWS Service | Purpose |
|-----------|-------------|---------|
| LLM Integration | Amazon Bedrock | Access to foundation models |
| Primary Model | Claude 3 Haiku | Efficient, cost-effective responses |
| Alternative Model | Claude 3.5 Haiku | Enhanced capabilities for specific use cases |

### Monitoring and Logging Layer

| Component | AWS Service | Purpose |
|-----------|-------------|---------|
| Logs | Amazon CloudWatch Logs | Centralized logging |
| Metrics | CloudWatch Metrics | Performance monitoring |
| API Tracking | AWS CloudTrail | Security and compliance auditing |

## Data Flow

1. **User Interaction**:
   - User accesses the website hosted on S3/CloudFront
   - Frontend JavaScript loads and initializes the AWS SDK
   - User enters text in the chat interface

2. **Authentication Flow**:
   - AWS SDK obtains credentials from Cognito Identity Pool
   - Frontend receives temporary AWS credentials
   - These credentials limit user actions to only Lex invocation

3. **Conversation Processing**:
   - User message is sent to Amazon Lex V2
   - Lex processes the input and identifies intents
   - Lex invokes the appropriate Lambda function

4. **Business Logic**:
   - Lambda function receives the input and session data
   - Function constructs an appropriate system prompt
   - Function calls Amazon Bedrock with this prompt

5. **AI Generation**:
   - Bedrock processes the request using the Claude model
   - Claude generates a response based on the system prompt and user input
   - Response maintains the South London personality

6. **Response Delivery**:
   - Bedrock returns the generated text to Lambda
   - Lambda function processes and formats the response
   - Response flows back through Lex to the frontend
   - Frontend displays the response to the user

7. **Monitoring**:
   - Each component logs activities to CloudWatch
   - CloudTrail records API calls for auditing
   - Metrics are collected for performance monitoring

## Technical Specifications

### Frontend Specifications

- **Framework**: Vanilla JavaScript
- **Responsive Design**: Mobile-first approach with adaptive layouts
- **AWS SDK Version**: 2.1000.0
- **Browser Compatibility**: Modern browsers (Chrome, Firefox, Safari, Edge)
- **Assets**: 
  - Static HTML (5.6KB)
  - Optimized images
  - Inline CSS and JavaScript

### Backend Specifications

#### Amazon Lex Configuration

- **Bot Version**: Lex V2
- **Primary Language**: English (GB)
- **Fallback Intent**: Configured to handle unknown inputs
- **Session Timeout**: 5 minutes
- **Utterance Storage**: Enabled for training

#### Lambda Functions

- **Runtime**: Python 3.10+
- **Memory Allocation**: 128MB
- **Timeout**: 15 seconds
- **Concurrency**: Unreserved (auto-scaling)
- **Environment Variables**: None (hardcoded configurations)
- **Handler**: `lambda_function.lambda_handler`

#### Bedrock Configuration

- **Primary Model**: `anthropic.claude-3-haiku-20240307-v1:0`
- **Alternative Model**: `anthropic.claude-3-5-haiku-20240620-v1:0`
- **Parameters**:
  - Temperature: 0.7 (balanced creativity)
  - Max Tokens: 150 (production) / 100 (concise)
  - Anthropic API Version: `bedrock-2023-05-31`

### System Prompts

The system prompts are carefully crafted to ensure the AI generates responses with an authentic South London youth dialect and personality:

- **Primary Prompt**: 18-year-old South Londoner with Jamaican heritage
- **Concise Prompt**: Optimized for shorter, more direct responses
- **Response Length Guidelines**: 1-5 sentences based on query complexity
- **Cultural Elements**: Modern London slang, direct communication style, authentic rhetorical devices

## Security Architecture

### Identity and Access Management

- **IAM Roles**: Follows principle of least privilege
- **Cognito**: Unauthenticated identities with limited permissions
- **Cross-Origin Resource Sharing (CORS)**: Properly configured on S3 bucket

### Data Protection

- **Client-Side Security**: No sensitive data stored in browser
- **Transmission Security**: All API calls made over HTTPS
- **Input Validation**: Client and server-side validation to prevent injection attacks

### Compliance Considerations

- **Data Privacy**: No PII or sensitive user data collected or stored
- **Logging Controls**: CloudWatch logs configured to exclude sensitive information
- **Geographic Restrictions**: None (globally available)

## Monitoring and Logging

### CloudWatch Setup

- **Log Retention**: 30 days
- **Log Insights**: Enabled for error analysis
- **Metrics Collected**:
  - Lambda invocation count and duration
  - Lex conversation success/failure rates
  - Bedrock model invocation statistics

### Alerting

- **Error Rate Thresholds**: Alerts on sustained error rates > 5%
- **Lambda Failures**: Notification on 3+ consecutive failures
- **Lex Misunderstanding Rate**: Alerts when exceeding 15%

## Performance Considerations

### Latency Optimization

- **CloudFront Caching**: Static assets cached at edge locations
- **Lambda Optimization**: Cold start minimization
- **Response Size**: Kept minimal to reduce transmission time
- **Parallel Processing**: Not implemented (sequential flow)

### Resource Utilization

- **Lambda Memory**: Configured based on profile testing
- **Bedrock Token Usage**: Optimized with max_tokens parameter
- **Client-Side Resources**: Minimal JavaScript footprint

## Scalability and Reliability

### Auto-Scaling Characteristics

- **Lambda**: Auto-scales based on demand
- **S3 & CloudFront**: Inherently scalable for static content
- **Lex & Bedrock**: Managed services with built-in scaling

### Failure Handling

- **Error Recovery**: Graceful error messages in case of service disruption
- **Retry Logic**: Implemented for transient failures
- **Degraded Mode**: No explicit fallback; relies on service availability

### Multi-Region Considerations

- **Current Deployment**: US East 1 (N. Virginia)
- **Region Dependencies**: Bedrock model availability constrains regions
- **Disaster Recovery**: Not implemented (stateless application)

## Cost Optimization

### Service Cost Breakdown

| AWS Service | Cost Factors | Optimization Strategy |
|-------------|--------------|------------------------|
| Lambda | Invocations, Duration | Minimal memory allocation, code efficiency |
| Lex | Requests | Optimized session handling |
| Bedrock | Model type, Token count | Token limit constraints, model selection |
| S3 | Storage, Requests | Minimal assets, efficient caching |
| CloudFront | Data Transfer | Edge caching, content optimization |
| CloudWatch | Log storage, API calls | Selective logging, log retention policies |

### Reserved Capacity

- No reserved capacity implemented (pay-per-use model)

## Limitations and Constraints

### Technical Limitations

- **Response Time**: 1-3 second average response generation time
- **Conversation Memory**: Limited by Lex session attributes (4KB)
- **Input Size**: Maximum 1024 characters per user message
- **Regional Availability**: Limited by Bedrock model availability

### Functional Constraints

- **Language Support**: English only (with South London dialect)
- **Multi-Turn Complexity**: Limited contextual understanding across multiple exchanges
- **Offline Operation**: Not supported (requires internet connection)

## Future Enhancements

### Short-Term Roadmap

- Voice interface using Amazon Polly
- Enhanced conversation memory using DynamoDB
- User preference storage for personalization

### Long-Term Vision

- Multi-language support with localized cultural adaptations
- Sentiment analysis for adaptive responses
- Integration with social media platforms
- Mobile application clients

---

*This document is confidential and proprietary to Wagwan London. It contains architectural and technical specifications intended for development and operational teams.*

© 2025 Wagwan London | Created by Ivan Rivera 