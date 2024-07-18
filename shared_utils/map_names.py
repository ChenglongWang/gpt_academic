import re
from toolbox import get_conf

mapping_dic = get_conf("MODEL_NAME_MAPPING")

rev_mapping_dic = {}
for k, v in mapping_dic.items():
    rev_mapping_dic[v] = k

def map_model_to_friendly_name(m):
    if m in mapping_dic:
        return mapping_dic[m]
    return m

def map_models_to_friendly_names(models):
    return [map_model_to_friendly_name(m) for m in models]

def map_friendly_names_to_model(m):
    if m in rev_mapping_dic:
        return rev_mapping_dic[m]
    return m

def read_one_api_model_name(model: str):
    """return real model name and max_token.
    """
    max_token_pattern = r"\(max_token=(\d+)\)"
    match = re.search(max_token_pattern, model)
    if match:
        max_token_tmp = match.group(1)  # 获取 max_token 的值
        max_token_tmp = int(max_token_tmp)
        model = re.sub(max_token_pattern, "", model)  # 从原字符串中删除 "(max_token=...)"
    else:
        max_token_tmp = 4096
    return model, max_token_tmp