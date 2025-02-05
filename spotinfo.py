import subprocess
import json
import os

# AWSの全リージョンリスト
regions = [
    "us-east-1", "us-west-1", "us-west-2", "eu-west-1", "eu-central-1",
    "ap-southeast-1", "ap-southeast-2", "ap-northeast-1", "ap-northeast-2"
]

# 保存先ディレクトリ
output_dir = "spot_prices_by_region"
os.makedirs(output_dir, exist_ok=True)

# 各リージョンのSpot情報を取得してJSON形式で保存
def fetch_spot_prices(region):
    try:
        # spotinfoコマンドを実行
        result = subprocess.run(
            ["spotinfo", "--region=" + region, "--sort=type", "--output=json"],
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

        # JSON形式でパース
        try:
            data = json.loads(result.stdout)
            return data
        except json.JSONDecodeError:
            print(f"エラー: {region} の出力がJSON形式ではありません: {result.stdout.strip()}")
            return None
    except Exception as e:
        print(f"例外発生: {region} のSpot情報取得に失敗: {e}")
        return None

# 各リージョンごとに情報を取得して個別に保存
for region in regions:
    print(f"{region}の情報を取得中...")
    spot_data = fetch_spot_prices(region)
    if spot_data:
        region_file = os.path.join(output_dir, f"{region}_spot_prices.json")
        with open(region_file, "w") as f:
            json.dump(spot_data, f, indent=4)
        print(f"{region} のSpot情報を {region_file} に保存しました。")
    else:
        print(f"{region} の情報取得に失敗しました。")

print(f"すべてのリージョンの処理が完了しました。データは {output_dir} に保存されています。")
