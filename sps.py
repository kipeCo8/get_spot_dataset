import boto3
import csv
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import get_ec2_params

def get_spot_placement_score(region, instance_type):
    """指定されたリージョンとインスタンスタイプでスポットプレイスメントスコアを取得"""
    client = boto3.client('ec2', region_name=region)
    try:
        response = client.get_spot_placement_scores(
            InstanceTypes=[instance_type],
            TargetCapacity=1  # 必須パラメータ、1を指定
        )
        # 必要なスコアだけ返す
        if response['SpotPlacementScores']:
            return response['SpotPlacementScores'][0].get('Score', 'N/A')
        else:
            return 'N/A'
    except client.exceptions.ClientError as e:
        print(f"Error in region {region} for instance type {instance_type}: {e}")
        return 'N/A'

def save_to_csv(region, data, output_dir="sps_by_region"):
    """データをリージョンごとにCSVファイルに保存"""
    os.makedirs(output_dir, exist_ok=True)  # 保存先ディレクトリを作成
    file_path = os.path.join(output_dir, f"{region}_spot_scores.csv")
    fieldnames = ["Region", "Instance", "SPS"]

    # データをInstance列でソートして保存
    sorted_data = sorted(data, key=lambda x: x["Instance"])
    with open(file_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sorted_data)
    print(f"Data for region {region} has been written to {file_path}")

def main():
    # 利用可能なリージョンを取得
    regions = get_ec2_params.get_all_regions()

    print(f"利用可能なリージョン数：{len(regions)}")

    # 各リージョンごとにデータを取得して保存
    for region in regions:

        ### 対象のインスタンスタイプ
        instance_types = get_ec2_params.get_spot_instance_types(region)
        print(f"{region}でスポット利用可能なインスタンス数：{len(instance_types)}")

        print(f"Processing region: {region}")
        csv_data = []

        # 各インスタンスタイプについてスコアを取得
        for instance_type in instance_types:
            score = get_spot_placement_score(region, instance_type)
            csv_data.append({
                "Region": region,
                "Instance": instance_type,
                "SPS": score
            })

        # データをリージョンごとのCSVに保存
        save_to_csv(region, csv_data)

if __name__ == "__main__":
    try:
        main()
    except (NoCredentialsError, PartialCredentialsError):
        print("AWSの認証情報が設定されていません。")
