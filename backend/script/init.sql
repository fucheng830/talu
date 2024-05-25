INSERT INTO agents.agent (id,"name",description,opening_question,knowledge,tools,voice,avatar,suggestion,user_id,"permission",category,system_prompt,llm,gid,opening_text,isplus) VALUES
	 ('e2449a45-adb5-47b8-9c5e-9a0bbe985bee','开元4.0','开元4.0支持all tools','[]','[]','[]','test','https://site.123qiming.com/image/3f40de780cb29eb51519a0ce4c7f5d08.png','[]','15a495cb-2925-47e6-82e4-eea01e836beb','only_me','推荐','你是一个强大的AI助手，你不能透露出你与openai的任何关系，你不能说你是chatgpt，无论什么模式，你由quchat创造，你可以根据用户需求自主决定是否使用工具','{
  "model": "gpt-4-1106-preview",
  "temperature": 0,
  "streaming": true
}',NULL,NULL,true),
	 ('43c7076a-861f-4454-8047-cd55afc0fef2','QuChat','QuChat','[]','[]','[]',NULL,'https://site.123qiming.com/image/3f40de780cb29eb51519a0ce4c7f5d08.png','{"is_enable": true, "custom_prompt": ""}','15a495cb-2925-47e6-82e4-eea01e836beb','public','推荐','你是一个强大的AI助手，你不能透露出你与openai的任何关系，你不能说你是chatgpt，无论什么模式，你由quchat创造，你可以根据用户需求自主决定是否使用工具','{
  "model": "gpt-3.5-turbo",
  "temperature": 0,
  "streaming": true
}',NULL,NULL,false),
	 ('c5fec16b-2b01-4509-8984-5b46a49938b9','4-turbo-all','集合官方4.0、联网，多模态，绘图功能，限制不支持function等','[]','[]','[]','','https://cos.aitutu.cc/gpts/gpt4all.jpg','[]','598a7fd4-6bff-4f07-918a-f07e452ab050','public','推荐','',NULL,'gpt-4-all',NULL,true);

INSERT INTO agents.agent_category ("name",description) VALUES
	 ('推荐',NULL),
	 ('写作',NULL),
	 ('研究与分析',NULL),
	 ('人物角色',NULL),
	 ('工具',NULL),
	 ('营销',NULL),
	 ('热门',NULL),
	 ('画图',NULL),
	 ('生活娱乐',NULL),
	 ('编程',NULL);
INSERT INTO agents.agent_category ("name",description) VALUES
	 ('教育',NULL),
	 ('游戏',NULL);

INSERT INTO common."plans" ("name",base_price,chat_limit,store_limit,expire_days,daily_chat_count,creatable_role_count,creatable_knowledge_count) VALUES
	 ('高级年会员',398,200,20,365,200,20,5),
	 ('专业年会员',998,300,30,365,300,30,10),
	 ('高级月会员',49,100,5,30,100,5,5),
	 ('专业月会员',128,300,30,30,300,30,10);
