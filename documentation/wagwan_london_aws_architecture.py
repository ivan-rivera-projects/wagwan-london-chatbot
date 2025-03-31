from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.storage import S3
from diagrams.aws.network import CloudFront
from diagrams.aws.ml import Sagemaker, Comprehend
from diagrams.aws.security import Cognito
from diagrams.aws.integration import Eventbridge
from diagrams.aws.management import Cloudwatch
from diagrams.aws.mobile import APIGateway
from diagrams.onprem.client import User
from diagrams.generic.compute import Rack
from diagrams.custom import Custom
from diagrams.aws.general import General

def create_wagwan_architecture_diagram():
    # Set up the diagram with a white background
    graph_attr = {
        "fontsize": "30",
        "bgcolor": "white",
        "margin": "0",
        "pad": "1.0"
    }
    
    with Diagram("Wagwan.London AWS Architecture", show=False, direction="LR", 
                 graph_attr=graph_attr, filename="wagwan_london_architecture"):
        
        # Create user node
        user = User("End User")
        
        # Frontend cluster
        with Cluster("Frontend"):
            s3 = S3("Static Website Hosting")
            cloudfront = CloudFront("Content Delivery")
        
        # Backend processing cluster
        with Cluster("Backend Processing"):
            # Using APIGateway to represent Amazon Lex
            lex = APIGateway("Amazon Lex v2\nChatbot Interface")
            
            with Cluster("Lambda Functions"):
                lambda_prod = Lambda("production_lambda")
                lambda_concise = Lambda("concise_convo_lambda")
                lambda_clause3 = Lambda("lambda_clause3")
            
            # Custom icon for Amazon Bedrock (which isn't in the diagrams library)
            # Using SageMaker as a placeholder with custom label
            bedrock = Rack("Amazon Bedrock\nClaude 3 Models")
        
        # Security & Monitoring cluster
        with Cluster("Security & Monitoring"):
            cognito = Cognito("Identity Pool")
            cloudwatch = Cloudwatch("Logging & Monitoring")
        
        # Define connections
        user >> Edge(color="black") >> cloudfront
        cloudfront >> Edge(color="black") >> s3
        user >> Edge(color="blue", style="dashed") >> lex
        
        lex >> Edge(color="blue") >> lambda_prod
        lex >> Edge(color="blue") >> lambda_concise
        lex >> Edge(color="blue") >> lambda_clause3
        
        lambda_prod >> Edge(color="red") >> bedrock
        lambda_concise >> Edge(color="red") >> bedrock
        lambda_clause3 >> Edge(color="red") >> bedrock
        
        lex >> Edge(color="green", style="dotted") >> cognito
        
        lambda_prod >> Edge(color="orange", style="dotted") >> cloudwatch
        lambda_concise >> Edge(color="orange", style="dotted") >> cloudwatch
        lambda_clause3 >> Edge(color="orange", style="dotted") >> cloudwatch
        bedrock >> Edge(color="orange", style="dotted") >> cloudwatch
        
        # Return path
        bedrock >> Edge(color="purple", style="dashed") >> lambda_prod
        bedrock >> Edge(color="purple", style="dashed") >> lambda_concise
        bedrock >> Edge(color="purple", style="dashed") >> lambda_clause3
        lambda_prod >> Edge(color="purple", style="dashed") >> lex
        lambda_concise >> Edge(color="purple", style="dashed") >> lex
        lambda_clause3 >> Edge(color="purple", style="dashed") >> lex
        lex >> Edge(color="purple", style="dashed") >> user

if __name__ == "__main__":
    create_wagwan_architecture_diagram()