import pytest
import boto3

def get_unhealthy_target_groups(region_name):
    elbv2_client = boto3.client('elbv2', region_name=region_name)

    response = elbv2_client.describe_load_balancers()
    load_balancer_arns = [lb['LoadBalancerArn'] for lb in response['LoadBalancers']]

    unhealthy_target_groups = []

    for lb_arn in load_balancer_arns:
        response = elbv2_client.describe_target_groups(
            LoadBalancerArn=lb_arn
        )
        target_groups = response['TargetGroups']

        for target_group in target_groups:
            response = elbv2_client.describe_target_health(
                TargetGroupArn=target_group['TargetGroupArn']
            )
            target_health_descriptions = response['TargetHealthDescriptions']

            for target_health in target_health_descriptions:
                if target_health['TargetHealth']['State'] != 'healthy':
                    target_group_arn = target_group['TargetGroupArn']
                    unhealthy_target_groups.append(target_group_arn)

    return unhealthy_target_groups

def test_print_unhealthy_target_groups():
    region_name = 'us-east-1' 
    unhealthy_target_groups = get_unhealthy_target_groups(region_name)

    for target_group_arn in unhealthy_target_groups:
        print(f"Unhealthy Target Group: {target_group_arn}")
        