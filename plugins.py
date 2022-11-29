import os
import tinydb
from pydantic import BaseModel


class Plugin(BaseModel):
    executable: str | None = ''
    id: int | None = 0
    params: str | None = ''
    
    def as_dict(self):
        return dict(self)
    
    @classmethod
    def from_doc(cls, data: tinydb.table.Document):
        plugin = cls()
        plugin.__dict__.update(data)
        plugin.id = data.doc_id
        return plugin
    
class PluginDb:
    def __init__(self, db_file:str=None):
        self.file = db_file or 'C:\\Users\\e433679\\Documents\\Project_Manager\\pm_web_plugins.json'
        self.db = tinydb.TinyDB(self.file)
        self.plugins = self.db.table("plugins")
        # self.tags = self.db.table('tags')
        
    def insert_plugin(self, plugin: Plugin)->tuple[bool, dict]:
        try:
            id = self.plugins.insert(plugin.as_dict())
            # plugin.id = id
            new_plugin = Plugin.from_doc(self.plugins.get(doc_id=id))
            print(new_plugin)
        except:
            return False, {}
        return True, new_plugin
        
    def all_plugins(self, recent_first:bool=True):
        plugin_docs = self.plugins.all()
        plugins = [Plugin.from_doc(doc) for doc in plugin_docs]
        if recent_first:
            plugins.reverse()
        return plugins
    
    def update_plugin(self, plugin:Plugin)->bool:
        try:
            self.plugins.update(plugin.as_dict(), doc_ids=[plugin.id])
        except KeyError:
            return False
        return True
    
    def remove_plugins(self, plugin_ids)->bool:
        try:
            self.plugins.remove(doc_ids=plugin_ids)
        except:
            return False
        return True
    
db = PluginDb('db/plugindb.json')
plugin = Plugin.parse_obj({'executable':'test'})
print(plugin)
status, plugin = db.insert_plugin(plugin)
print(status, plugin)
plugins = db.all_plugins()
print(plugins)