import boto3

def get_spot_instance_types(region):
    ec2_client = boto3.client('ec2', region_name=region)
    spot_instance_types = []
    next_token = None

    while True:
        # describe_instance_types を呼び出し
        if next_token:
            response = ec2_client.describe_instance_types(NextToken=next_token)
        else:
            response = ec2_client.describe_instance_types()

        # スポット利用可能なインスタンスタイプをフィルタリング
        spot_instance_types.extend([
            instance["InstanceType"]
            for instance in response["InstanceTypes"]
            if "spot" in instance.get("SupportedUsageClasses", [])
        ])

        # 次のページがある場合はトークンを更新
        next_token = response.get('NextToken')
        if not next_token:
            break

    return spot_instance_types

def get_all_regions():
    """利用可能なAWSリージョンのリストを取得"""
    ec2_client = boto3.client('ec2')
    regions = ec2_client.describe_regions()
    return [region['RegionName'] for region in regions['Regions']]

# # スポット利用可能なインスタンスタイプを取得
# spot_instance_types = sorted(get_spot_instance_types('ap-northeast-1'))


# # 結果を表示
# print(spot_instance_types)
# print(f"スポット利用可能なインスタンスタイプ数: {len(spot_instance_types)}")


    


