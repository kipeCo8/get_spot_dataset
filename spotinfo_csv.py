import subprocess
import os
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import sps


# AWSの全リージョンリスト
regions = sps.get_all_regions()

# 保存先ディレクトリ
output_dir = "spot_prices_by_region_csv"
os.makedirs(output_dir, exist_ok=True)

# 各リージョンのSpot情報を取得
def fetch_spot_prices(region):
    try:
        # spotinfoコマンドを実行
        result = subprocess.run(
            ["spotinfo", "--region=" + region, "--sort=type", "--output=csv"],
            capture_output=True, text=True
        )
        # 結果をデバッグログとして表示
        if result.returncode != 0:
            print(f"エラー: {region} のSpot情報取得に失敗: {result.stderr.strip()}")
            return None

        # 出力が空の場合もエラーとして処理
        if not result.stdout.strip():
            print(f"エラー: {region} からの出力が空です")
            return None

        return result.stdout
    except Exception as e:
        print(f"例外発生: {region} のSpot情報取得に失敗: {e}")
        return None

# データをCSVファイルに保存
def save_to_csv(region, csv_data):
    # CSVファイルパス
    csv_file = os.path.join(output_dir, f"{region}_spot_prices.csv")
    try:
        with open(csv_file, "w") as f:
            f.write(csv_data)
        print(f"{region} のSpot情報を {csv_file} に保存しました。")
    except Exception as e:
        print(f"エラー: {region} のデータをCSVに保存できませんでした: {e}")

# 各リージョンごとに情報を取得してCSVに保存
for region in regions:
    print(f"{region}の情報を取得中...")
    csv_data = fetch_spot_prices(region)
    if csv_data:
        save_to_csv(region, csv_data)
    else:
        print(f"{region} の情報取得に失敗しました。")

print(f"すべてのリージョンの処理が完了しました。データは {output_dir} に保存されています。")
