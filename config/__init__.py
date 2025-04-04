from utils import dir_path
import yaml

import os

# log = logger.infoLogger(__name__)
# 获取当前文件目录
file_path = os.path.dirname(os.path.abspath(__file__))

class SettingReader:
    def __init__(self):
        self.configs = {}
        self.models = {}
        self.registry = {}

        import utils.Io_util
        self.reader = utils.Io_util.IoUtil()

        # 初始化配置文件
        self._init_config()
        self._init_models()
        self._init_registry()

    def _init_config(self):
        """初始化配置文件，如果不存在则从模板创建"""
        config_file = os.path.join(file_path, 'config.yaml')
        template_file = os.path.join(file_path, 'template.yaml')

        try:
            # 如果配置文件不存在且模板文件存在，则复制模板
            if not os.path.exists(config_file) and os.path.exists(template_file):
                self.reader.copy_file(template_file, config_file)
                # 复制后立即读取新创建的配置文件
                self.configs = self.reader.read_yaml(config_file, 'utf-8')
            # 如果配置文件存在，直接读取
            elif os.path.exists(config_file):
                self.configs = self.reader.read_yaml(config_file, 'utf-8')
            # 如果既没有配置文件也没有模板文件
            else:
                # 模板不存在时创建空配置
                with open(config_file, 'w') as f:
                    yaml.safe_dump({}, f)
                self.configs = {}
        except Exception as e:
            print(f"配置文件操作出错: {str(e)}")
            try:
                # 尝试创建空配置文件
                with open(config_file, 'w') as f:
                    yaml.safe_dump({}, f)
                self.configs = {}
            except Exception as create_err:
                print(f"创建空配置文件失败: {str(create_err)}")
                self.configs = {}

    def _init_models(self):
        """初始化模型配置文件"""
        model_file = os.path.join(file_path, 'models.yaml')
        try:
            if os.path.exists(model_file):
                self.models = self.reader.read_yaml(model_file, 'utf-8')
            else:
                self.models = {}
        except Exception as e:
            self.models = {}

    def _init_registry(self):
        """初始化注册信息"""
        registry_file = os.path.join(file_path,'registry.yaml')
        try:
            if os.path.exists(registry_file):
                self.registry = self.reader.read_yaml(registry_file, 'utf-8')
            else:
                self.registry = {}
        except Exception as e:
            self.registry = {}

    def get_config(self):
        """获取配置信息
        Returns:
            dict: 配置文件的字典形式
        """
        return self.configs

    def get_model(self):
        """获取模型配置信息
        Returns:
            dict: 模型配置的字典形式
        """
        return self.models
    
    def set_config(self, config):
        """设置配置信息
        Args:
            config (dict): 新的配置信息
        """
        self.configs = config
        self._save_config()

    def _save_config(self):
        """保存配置信息到文件"""
        config_file = os.path.join(file_path, 'config.yaml')
        try:
            self.reader.write_yaml(config_file, self.configs)
        except Exception as e:
            print(f"保存配置文件出错: {str(e)}")

    def set_model(self, model):
        """设置模型配置信息
        Args:
            model (dict): 新的模型配置信息
        """
        self.models = model
        self._save_model()

    def _save_model(self):
        """保存模型配置信息到文件"""
        model_file = os.path.join(file_path, 'models.yaml')
        try:
            self.reader.write_yaml(model_file, self.models)
        except Exception as e:
            print(f"保存模型配置文件出错: {str(e)}")

    def get_registry(self):
        """获取注册信息
        Returns:
            dict: 注册信息的字典形式
        """
        return self.registry

    def set_registry(self, registry):
        """设置注册信息
        Args:
            registry (dict): 新的注册信息
        """
        self.registry = registry
        self._save_registry()

    def _save_registry(self):
        """保存注册信息到文件"""
        registry_file = os.path.join(file_path,'registry.yaml')
        try:
            self.reader.write_yaml(registry_file, self.registry)
        except Exception as e:
            print(f"保存注册信息文件出错: {str(e)}")
    
    
    def _reload_config(self):
        """重新加载配置信息"""
        self._init_config()

    def _reload_model(self):
        """重新加载模型配置信息"""
        self._init_models()

    def _reload_registry(self):
        """重新加载注册信息"""
        self._init_registry()

    def reload(self):
        """重新加载配置信息"""
        self._reload_config()
        self._reload_model()
        self._reload_registry()

# 实例化配置读取器
# setting = SettingReader()
# __all__ = ['setting']