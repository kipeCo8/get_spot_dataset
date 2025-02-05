import boto3

def get_instance_types_by_region():
    # すべてのリージョンを取得
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

    # 各リージョンごとにスポット利用可能なインスタンスタイプを取得
    region_instance_types = {}
    for region in regions:
        print(f"Processing region: {region}")
        regional_client = boto3.client('ec2', region_name=region)
        next_token = None
        spot_instance_types = []

        while True:
            if next_token:
                response = regional_client.describe_instance_types(NextToken=next_token)
            else:
                response = regional_client.describe_instance_types()

            # スポット利用可能なインスタンスタイプをフィルタリング
            spot_instance_types.extend([
                instance["InstanceType"]
                for instance in response["InstanceTypes"]
                if "spot" in instance.get("SupportedUsageClasses", [])
            ])

            # 次のページがある場合トークンを更新
            next_token = response.get('NextToken')
            if not next_token:
                break

        # 結果を保存
        region_instance_types[region] = spot_instance_types

    return region_instance_types


# 各リージョンごとの結果を取得
result = get_instance_types_by_region()

# 各リージョンごとのインスタンスタイプを表示
for region, instance_types in result.items():
    print(f"Region: {region}, Spot Instance Types: {len(instance_types)}")
    #print(instance_types)
