import json

cookies = {
    "x-zp-client-id": "cc9d2729-1ee2-4091-8e80-f40acb4bf3c9",
    "sensorsdata2015jssdkchannel": "%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D",
    "_uab_collina": "173417882581324716183876",
    "sts_deviceid": "193c5292637951-0082961a41037-4c657b58-1821369-193c52926381525",
    "ZP_OLD_FLAG": "false",
    "Hm_lvt_ec66c70e779981d9449c691e22a09d17": "1734220424",
    "locationInfo_search": "{%22code%22:%22%22}",
    "at": "a3cc80fa7e204261b46bd75b3bf3d458",
    "rt": "ef18d9f16a374123afefecfa3bcde1a4",
    "sts_sg": "1",
    "sts_chnlsid": "Unknown",
    "sensorsdata2015jssdkcross": "%7B%22distinct_id%22%3A%221175477940%22%2C%22first_id%22%3A%22193c51ce57ff66-0dd1db5698f7c88-4c657b58-1821369-193c51ce580271%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_utm_source%22%3A%22bingsem_b%22%2C%22%24latest_utm_medium%22%3A%22ocpc%22%2C%22%24latest_utm_campaign%22%3A%22youju02%22%2C%22%24latest_utm_content%22%3A%22jp%22%2C%22%24latest_utm_term%22%3A%2220016123%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkzYzUxY2U1N2ZmNjYtMGRkMWRiNTY5OGY3Yzg4LTRjNjU3YjU4LTE4MjEzNjktMTkzYzUxY2U1ODAyNzEiLCIkaWRlbnRpdHlfbG9naW5faWQiOiIxMTc1NDc3OTQwIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221175477940%22%7D%2C%22%24device_id%22%3A%22193c51ce57ff66-0dd1db5698f7c88-4c657b58-1821369-193c51ce580271%22%7D",
    "LastCity": "%E6%B8%A9%E5%B7%9E",
    "LastCity%5Fid": "655",
    "Hm_lvt_7fa4effa4233f03d11c7e2c710749600": "1734220435,1734311753",
    "HMACCOUNT": "D083F6484DD85AF7",
    "selectCity_search": "530",
    "Hm_lpvt_7fa4effa4233f03d11c7e2c710749600": "1734311812",
    "sts_sid": "193cd787b41a0-086969169363f6-4c657b58-1821369-193cd787b42186c",
    "sts_evtseq": "2",
    "FSSBBIl1UgzbN7NT": "5RT5FXbwIb.LqqqDsuUC17q_BpeBLmjdn9qUhhUS4diOtqIWipg_KByOS6DgrC7arvONjQDO4sNW0OPB1K0QcJWBUwb9J6xciQmVwVjJhY4uSvUbhQOkv_74vrVOrUKG9SsH_nmorPzmVNtjXHNU5CNZSFLQX_SbywfXTKihRRHp1PfHePyt4sTZxb07RXIcjVj7hQ9SobN1DkxWadd1VeVD5GMIiNl8C0eC0EMUgO9FQ1QXjkUuOZsHytuWGqn1r6QwB8WcqgfwoJotQQ3amHeRlrIr02pzeBN.Ss4wUNPZmuDXL2rMYtRZVgoF_zv7eLQVBUwvq22miCsYC.8MFvo"
}

platform_id = [
    ('智联招聘',0)
]

zhilian_region_code = [
    ('北京', 'jl530'),
    ('上海', 'jl538'),
    ('广州', 'jl763'),
    ('深圳', 'jl765'),
    ('天津', 'jl531'),
    ('重庆', 'jl532'),
    ('西安', 'jl854'),
    ('武汉', 'jl736'),
    ('成都', 'jl801'),
    ('杭州', 'jl653'),
    ('南京', 'jl635'),
    ('厦门', 'jl682')
]

# 获取职业码
def get_job_code(job) -> list:
    # 读入job.json文件
    job_codes = json.load(open('zhaopin/jobs.json', 'r', encoding='utf-8'))
    
    # 返回对应行业的job_code
    job_code = job_codes[job]
    return [(key, value) for key, value in job_code.items()]
