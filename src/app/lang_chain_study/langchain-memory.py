from langgraph.store.memory import InMemoryStore

from src.inf.env.env_conf import G_Settings
from src.inf.llm.qwen import G_QwenLLMClient


# InMemoryStore saves data to an in-memory dictionary. Use a DB-backed store in production use.
store = InMemoryStore(index={"embed": G_QwenLLMClient.get_embedding_vector, "dims": G_Settings.qwen_api_embedding_dim}) 
user_id = "my-user"
application_context = "chitchat"
namespace = (user_id, application_context) 
store.put( 
    namespace,
    "a-memory",
    {
        "rules": [
            "User likes short, direct language",
            "User only speaks English & python",
        ],
        "my-key": "my-value",
    },
)
# get the "memory" by ID
item = store.get(namespace, "a-memory") 
# search for "memories" within this namespace, filtering on content equivalence, sorted by vector similarity
items = store.search( 
    namespace, filter={"my-key": "my-value"}, query="language preferences"
)
print(items)