from qiniu import  Auth, put_data

access_key = "KGfFR0DYOXUOpGL8XVrbt0V4bzUAB87Stt7pNhIu"
secret_key = "Y0K8155cH60N6E0OIuHs4ixxmL_I4DFjU5wD9vtS"
bucket_name = "ihome"

def storage(data):
    try:
        q = Auth(access_key, secret_key)
        token = q.upload_token(bucket_name)
        ret, info = put_data(token, None, data)
        print(ret, info)
    except Exception as e:
        raise e

    if info.status_code != 200:
        raise Exception("上传失败")
    return ret["key"]