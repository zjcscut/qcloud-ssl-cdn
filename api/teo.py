import json
from datetime import datetime
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
# 导入 cdn 产品模块的 models
from tencentcloud.teo.v20220901 import models

from api.get_client_profile import get_client_instance


def get_teo_client_instance(id, key):
    """
    获取teo的实例，用于后面对teo的各种操作
    """
    client = get_client_instance(id, key, "teo")
    return client


def get_teo_zones_list(client):
    """
    获取所有teo站点列表，取得zoneId用于接下来的操作
    """
    try:
        req = models.DescribeZonesRequest()
        params = {}
        req.from_json_string(json.dumps(params))

        resp = client.DescribeZones(req)
        print(resp.to_json_string())

    except TencentCloudSDKException as err:
        print(err)
        return []


def get_teo_domains_list(client, zoneid):
    """
    获取所有teo加速域名列表，传参zoneId
    """
    try:
        req = models.DescribeAccelerationDomainsRequest()
        params = {
            "ZoneId": f"{zoneid}"
        }
        req.from_json_string(json.dumps(params))

        resp = client.DescribeAccelerationDomains(req)
        # print(resp.to_json_string())
        print(f"获取所有{zoneid}下加速域名列表完成")
        return resp.AccelerationDomains

    except TencentCloudSDKException as err:
        print(err)
        return []


def update_teo_ssl(client, zoneid, hostname, cert_id):
    '''为指定域名的teo更换SSL证书
    '''
    try:
        req = models.ModifyHostsCertificateRequest()
        params = {
            "ZoneId": zoneid,
            "Hosts": [f"{hostname}"],
            "Mode": "sslcert",
            "ServerCertInfo": [
                {
                    "CertId": f"{cert_id}"
                }
            ]
        }
        req.from_json_string(json.dumps(params))

        resp = client.ModifyHostsCertificate(req)
        print(resp.to_json_string())
        print("成功更新域名为{0}的CDN的ssl证书为{1}".format(hostname, cert_id))

    except TencentCloudSDKException as err:
        print(err)
        exit("为CDN设置SSL证书{}出错".format(cert_id))
