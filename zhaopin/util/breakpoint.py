from zhaopin import constant
import os
import json
from ..constant import zhilian_region_code,zhilian_job_code

class ZhilianBP:
    def __init__(self, filepath='D:\\01 代码\\01 Python\\zhaopin\\zhaopin\\output\\breakpoint.json'):
        self.filepath = filepath
        self.region_code = None
        self.job_code = None
        self.page = None

    def save_breakpoint(self, region_code, job_code, page):
        """保存断点信息到文件"""
        data = {
            'region_code': region_code,
            'job_code': job_code,
            'page': page
        }
        with open(self.filepath, 'w') as f:
            json.dump(data, f)

    def load_breakpoint(self):
        """从文件中加载断点信息"""
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                try:
                    data = json.load(f)
                    self.region_code = data.get('region_code')
                    self.job_code = data.get('job_code')
                    self.page = data.get('page')
                    return True
                except Exception as e:
                    print(f"断点加载错误: {e}")
                    return False
        else:
            # 创建新断点文件
            with open(self.filepath, 'w') as f:
                json.dump({'region_code': zhilian_region_code[0][1], 'job_code': zhilian_job_code[0][1], 'page': 1}, f)
            
        return True

    def clear_breakpoint(self):
        """清除断点文件"""
        if os.path.exists(self.filepath):
            os.remove(self.filepath)