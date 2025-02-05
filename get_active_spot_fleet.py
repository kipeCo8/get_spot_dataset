import boto3

def get_active_spot_fleet():
    # boto3クライアントを初期化
    ec2_client = boto3.client('ec2')

    active_spot_fleet_ids = []
    next_token = None   #ページング

    try:
        while True:
            # describe_spot_fleet_requests 呼び出し
            if next_token:
                response = ec2_client.describe_spot_fleet_requests(
                    MaxResults=10,
                    NextToken=next_token
                )
            else:
                response = ec2_client.describe_spot_fleet_requests(MaxResults=10)

            # SpotFleetRequestState が "active" のものをフィルタリング
            for request in response.get("SpotFleetRequestConfigs", []):
                if request.get("SpotFleetRequestState") == "active":
                    active_spot_fleet_ids.append(request["SpotFleetRequestId"])
            
            # 次のページがない場合ループ終了
            next_token = response.get("NextToken")
            if not next_token:
                break

        # 結果の表示と返却
        if active_spot_fleet_ids:
            print("Active Spot Fleet IDs:", active_spot_fleet_ids)
        else:
            print("No active Spot Fleet Requests found")


    except Exception as e:
        print("An error occurred:", str(e))
        raise
    
    return active_spot_fleet_ids
