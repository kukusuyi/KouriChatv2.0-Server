"""
    # 动态模块加载
"""
import importlib
import logging
from typing import Dict, Any

from config import SettingReader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("HandlerRegistry")
class HandlerRegistry:
    def __init__(self):
        logger.info("HandlerRegistry 初始化......")
        self.registry = SettingReader().get_registry()
        self.modules: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self):
        base_module = self.registry.get("modules").get("base")
        for module_name, module_info in base_module.items():
            self._load_modules(module_name,module_info['path'])
        system_module = self.registry.get("modules").get("system")
        for module_name, module_info in system_module.items():
            if module_info.get('value', False):
                self._load_modules(module_name,module_info['path'])
        user_module = self.registry.get("modules").get("user")
        for module_name, module_info in user_module.items():
            if module_info.get('value', False):
                self._load_modules(module_name,module_info['path'])

    # def load_handlers(self): Processor
    def _load_modules(self, module_name: str, module_path: str):
        """动态加载模块并且实例化处理器
            - module_name : 模块名称
            - module_path : 模块路径
        """
        processor_class_name = ""
        try:
            import_path = module_path.replace("/", ".")
            module = importlib.import_module(import_path)

            # 构造 module name
            processor_class_name = f"{module_name}Processor"
            processor_class = getattr(module, processor_class_name)
            self.modules[module_name] = processor_class()
            logger.info(f"成功导入模块 {processor_class_name}")
        except ImportError as e:
            logger.error(f"从{module_path}导入模块{module_name}失败:{e}")
        except AttributeError as e:
            logger.error(f"在路径{module_path}没有找到类{processor_class_name}:{e}")
        except Exception as e:
            print(f"加载模块 {module_name}失败: {e}")


if __name__ == "__main__":
    handler = HandlerRegistry()
    example = handler.modules['memory']
    try:
        example.process_client_message("hello")
    finally:
        example.close()


    
