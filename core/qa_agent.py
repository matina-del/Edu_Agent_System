from langchain_openai import ChatOpenAI
from knowledge_base.vector_store import KnowledgeBase
from user_profile.profile_manager import UserProfileManager

class AdaptiveLearningAgent:
    def __init__(self, knowledge_base: KnowledgeBase, profile_manager: UserProfileManager, question_bank: list):
        self.knowledge_base = knowledge_base
        self.profile_manager = profile_manager
        self.question_bank = question_bank
        
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7) 
    
    def explain_concept(self, concept: str, user_id: str) -> str:
        profile = self.profile_manager.get_or_create_profile(user_id)
        related = self.knowledge_base.retrieve(concept, top_k=2) # 提取相关知识
        
        # 修复了原来代码里的语法错误 r[content] -> r['content']
        context_str = "\n".join([r['content'] for r in related]) if related else "无本地知识库补充"
        
        prompt = f"""作为资深教育专家，请用通俗易懂的方式解释概念。
        针对学生：{profile.grade} 学生
        概念：{concept}
        参考资料：{context_str}
        要求：包含生活中的例子，分点说明，字数控制在300字左右。"""
        
        return self.llm.invoke(prompt).content