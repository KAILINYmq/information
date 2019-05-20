from qiniu import  Auth, put_data

secret_key = "yV4GmNBL0gQK-1Sn3o4jktGLFdFSrlywR2C-hvsW"
secret_key = "bixMURPL6tHjrb8QKVg2tm7n9k8C7va0eQ4MEoeW"
bucket_name = "ihome"

def storage(data):
    try:
        q = Auth(secret_key, secret_key)
        token = q.upload_token(bucket_name)
        ret, info = put_data(token, None, data)
    except Exception as e:
        raise e

    if info.status_code != 200:
        raise Exception("上传失败")
    return ret["key"]